from rest_framework import serializers
from guide.models import Guide, ResponseStatus
from destination.models import Destination
from tour.models import Tour, TourName


class GuideWithoutToursSerializer(serializers.ModelSerializer):

    class Meta:
        model = Guide
        fields = ('id', 'name', 'phone', 'notes', 'fee')


class TourNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = TourName
        fields = ('id', 'name')


class TourSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    guide = GuideWithoutToursSerializer()
    sum = serializers.SerializerMethodField()

    def get_name(self, tour):
        return str(tour)

    def get_sum(self, tour):
        return tour.guide.fee + tour.supplementary_fee

    class Meta:
        model = Tour
        fields = ('id', 'name', 'day', 'destination',
                  'guide', 'supplementary_fee', 'sum')


class GuideSerializer(serializers.ModelSerializer):
    tours = serializers.SerializerMethodField()
    total = serializers.SerializerMethodField()

    def get_total(self, guide):
        return sum([tour.guide.fee + tour.supplementary_fee for tour in guide.tours.all()])

    def get_tours(self, guide):
        serializer = TourSerializer(guide.tours.all(), many=True)
        return serializer.data

    class Meta:
        model = Guide
        fields = ('id', 'name', 'phone', 'notes', 'tours', 'fee', 'total')


class ResponseStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResponseStatus
        fields = ('id', 'day', 'guide', 'status')


class DestinationSerializer(serializers.ModelSerializer):
    vessel = serializers.StringRelatedField()
    location = serializers.StringRelatedField()
    name = serializers.SerializerMethodField()

    def get_name(self, destination):
        return str(destination)

    class Meta:
        model = Destination
        fields = ('id', 'name', 'location', 'vessel', 'eta', 'etd')
