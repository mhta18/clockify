from rest_framework import serializers

class PlatformWideTotalsSerializer(serializers.Serializer):
    total_completed_hours = serializers.DecimalField(max_digits=10, decimal_places=2)
    total_processed_payouts = serializers.DecimalField(max_digits=12, decimal_places=2)

class GlobalOverviewSerializer(serializers.Serializer):
    total_registered_accounts = serializers.IntegerField()
    all_men = serializers.IntegerField()
    all_women = serializers.IntegerField()
    unspecified_gender = serializers.IntegerField()
    average_age = serializers.DecimalField(max_digits=10, decimal_places=2, allow_null=True)


class FreelancerReportSerializer(serializers.Serializer):
    total_hours_tracked = serializers.DecimalField(max_digits=10, decimal_places=2)
    total_payout_processed = serializers.DecimalField(
        max_digits=12, decimal_places=2
    ) 
    total_active_contracts = serializers.IntegerField()
    men_count = serializers.IntegerField()
    women_count = serializers.IntegerField()
    other_count = serializers.IntegerField()


class EmployerReportSerializer(serializers.Serializer):
    total_hours_tracked = serializers.DecimalField(max_digits=10, decimal_places=2)
    total_costs_accumulated = serializers.DecimalField(
        max_digits=12, decimal_places=2
    )  
    total_active_contracts = serializers.IntegerField()
    men_count = serializers.IntegerField()
    women_count = serializers.IntegerField()
    other_count = serializers.IntegerField()


class PlatformReportSerializer(serializers.Serializer):
    platform_wide_totals = PlatformWideTotalsSerializer()
    global_overview = GlobalOverviewSerializer()
    freelancer_reports = FreelancerReportSerializer()
    employer_reports = EmployerReportSerializer()
