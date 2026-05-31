from django.shortcuts import render
from users.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.decorators import action
from django.db.models import Count, Q
from users.models import User
from contracts.models import FreelancerContract, EmployerContract
from timetracking.models import TimeLog
# Create your views here.


class ReportsViewSet(viewsets.ViewSet):

    permission_classes = [IsAdminUser]

    @action(detail=False, methods={"get"}, url_path="user-reports")
    def get_repots(self, request):
        global_status = User.objects.aggregate(
            total_users=Count("id"),
            total_men=Count("id", filter=Q(gender="male")),
            total_women=Count("id", filter=Q(gender="female")),
            total_unspecified=Count(
                "id", filter=Q(gender="other") | Q(gender__is_null=True)
            ),
        )

        freelancer_status = FreelancerContract.objects.aggregate(
            total_frelancer=Count("id"),
            men=Count("id", filter=Q(contract_ptr__user__gender="male")),
            women=Count("id", filter=Q(contract_ptr__user__gender="female")),
        )

        employer_status = EmployerContract.objects.aggregate(
            total_employer=Count("id"),
            men=Count("id", filter=Q(contract_ptr__user__gender="male")),
            women=Count("id", filter=Q(contract_ptr__user__gender="female")),
        )

        freelancer_logs =TimeLog.objects.filter(user__contract__frelancercontract__isnull=False)



        dashboard_payload = {
            "global_overview": {
                "total_registered_accounts": global_status["total_users"],
                "all_men": global_status["total_men"],
                "all_women": global_status["total_women"],
                "unspecified_gender": global_status["total_unspecified"],
            },
            "freelancer_metrics": {
                "total_active_contracts": freelancer_status["total_freelancers"],
                "men_count": freelancer_status["men"],
                "women_count": freelancer_status["women"],
            },
            "employer_metrics": {
                "total_active_contracts": employer_status["total_employers"],
                "men_count": employer_status["men"],
                "women_count": employer_status["women"],
            },
        }
        return Response(dashboard_payload, status=status.HTTP_200_OK)
