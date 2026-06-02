from django.shortcuts import render
from drf_spectacular.utils import extend_schema
from users.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.decorators import action
from django.db.models import Count, Q, ExpressionWrapper,fields,Sum,F
from django.db.models.functions import Coalesce
from users.models import User
from decimal import Decimal
from contracts.models import FreelancerContract, EmployerContract
from timetracking.models import TimeLog
from .serializers import PlatformReportSerializer


# Create your views here.
@extend_schema(
    summary="Retrieve administrative platform summary report",
    description="Aggregates platform-wide hours tracked, user demographics, age parameters, and budget distributions.",
    responses={
        200: PlatformReportSerializer
    },
)

class ReportsViewSet(viewsets.ViewSet):

    permission_classes = [IsAdminUser]
    serializer_class = [PlatformReportSerializer]

    @action(detail=False, methods={"get"}, url_path="user-reports")
    def get_repots(self, request):
        completed_logs = TimeLog.objects.filter(end_time__isnull=False)
        duration_expression = ExpressionWrapper(
            F('end_time') - F('start_time'),
            output_field=fields.DurationField()
        )

        global_stats = completed_logs.annotate(
            calculated_duration=duration_expression
        ).aggregate(
            total_logs_payout=Coalesce(Sum("payment"), Decimal("0.00")),
            total_duration_timedelta=Sum("calculated_duration"),
        )

        global_seconds = global_stats["total_duration_timedelta"].total_seconds() if global_stats["total_duration_timedelta"] else 0
        global_hours = round(Decimal(global_seconds) / Decimal("3600.00"),2)

        freelancer_logs = completed_logs.filter(user__contract__freelancercontract__isnull=False).annotate(
            calculated_duration=duration_expression
        )
        avarage_age = User.objects.aggregate(average_age=Coalesce(Sum('age') / Count('id'), 0))['average_age']
        global_status = User.objects.aggregate(
            total_users=Count("id"),
            total_men=Count("id", filter=Q(gender="male")),
            total_women=Count("id", filter=Q(gender="female")),
            total_unspecified=Count(
                "id", filter=Q(gender="other") | Q(gender__isnull=True)
            ),
            
        )

        freelancer_stats = freelancer_logs.aggregate(
            total_payout=Coalesce(Sum('payment'), Decimal('0.00')),
            total_time=Sum('calculated_duration'),
            
            men_count=Count('user', distinct=True, filter=Q(user__gender='male')),
            women_count=Count('user', distinct=True, filter=Q(user__gender='female'))
        )

        fl_total_hours = round(Decimal(freelancer_stats["total_time"].total_seconds() if freelancer_stats["total_time"] else 0) / Decimal("3600.00"), 2)
        employer_logs = completed_logs.filter(user__contract__employercontract__isnull=False).annotate(
            calculated_duration=duration_expression
        )
        employer_stats =employer_logs.aggregate(
            total_payout=Coalesce(Sum('payment'), Decimal('0.00')),
            total_time=Sum('calculated_duration'),
            
            men_count=Count('user', distinct=True, filter=Q(user__gender='male')),
            women_count=Count('user', distinct=True, filter=Q(user__gender='female'))
        )

        emp_total_hours = round(Decimal(employer_stats["total_time"].total_seconds() if employer_stats["total_time"] else 0) / Decimal("3600.00"), 2)


        dashboard_payload = {
            "platform_wide_totals": {
                "total_completed_hours": global_hours,
                "total_processed_payouts": global_stats["total_logs_payout"],
            },
            "global_overview": {
                "total_registered_accounts": global_status["total_users"],
                "all_men": global_status["total_men"],
                "all_women": global_status["total_women"],
                "unspecified_gender": global_status["total_unspecified"],
                "average_age": round(avarage_age, 2) if avarage_age else None,
            },
            "freelancer_reports": {
                "total_hours_tracked": fl_total_hours,
                "total_payout_processed": freelancer_stats["total_payout"],
                "total_active_contracts": freelancer_stats["men_count"] + freelancer_stats["women_count"],
                "men_count": freelancer_stats["men_count"],
                "women_count": freelancer_stats["women_count"],
            },
            "employer_reports": {
                "total_hours_tracked": emp_total_hours,
                "total_costs_accumulated": employer_stats["total_payout"],
                "total_active_contracts": employer_stats["men_count"] + employer_stats["women_count"],
                "men_count": employer_stats["men_count"],
                "women_count": employer_stats["women_count"],
            },
        }

        serializer = PlatformReportSerializer(data=dashboard_payload)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data, status=status.HTTP_200_OK)
