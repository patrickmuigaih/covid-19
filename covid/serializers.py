from rest_framework import serializers


class RegionSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    avgAge = serializers.DecimalField(max_digits=5, decimal_places=2)
    avgDailyIncomePopulation = serializers.DecimalField(
        max_digits=5, decimal_places=2)
    avgDailyIncomeInUSD = serializers.DecimalField(
        max_digits=10, decimal_places=2)


class EstimatorSerializer(serializers.Serializer):
    region = RegionSerializer(many=False, required=True)
    periodType = serializers.ChoiceField(
        choices=(('days', 'days',), ('weeks', 'weeks',), ('months', 'months'))
    )
    timeToElapse = serializers.IntegerField()
    reportedCases = serializers.IntegerField()
    population = serializers.IntegerField()
    totalHospitalBeds = serializers.IntegerField()
