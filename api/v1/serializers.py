from rest_framework import serializers
from guide.models import Guide, ResponseStatus
from destination.models import Destination, Location
from tour.models import Tour, TourName, TourLocation


class TourLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = TourLocation
        fields = ('id', 'name')


class LocationSerializer(serializers.ModelSerializer):
    tour_locations = serializers.SerializerMethodField()

    def get_tour_locations(self, location):
        serializer = TourLocationSerializer(
            location.tour_locations.all(), many=True)
        return serializer.data

    class Meta:
        model = Location
        fields = ('id', 'name', 'tour_locations')


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
    location = LocationSerializer()
    tour_location = TourLocationSerializer()

    def get_name(self, tour):
        return str(tour)

    def get_sum(self, tour):
        return tour.fee + tour.supplementary_fee

    class Meta:
        model = Tour
        fields = ('id', 'name', 'day', 'tour_time', 'destination', 'location', 'tour_location',
                  'guide', 'fee', 'supplementary_fee', 'sum')


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


class GuideWithTourByDaySerializer(serializers.ModelSerializer):
    tours = serializers.SerializerMethodField()
    total = serializers.SerializerMethodField()

    def get_total(self, guide):
        return sum([tour.guide.fee + tour.supplementary_fee for tour in guide.tours.all()])

    def get_tours(self, guide):
        tours = self.context.get('tours', None)
        serializer = TourSerializer(tours, many=True)
        return serializer.data

    class Meta:
        model = Guide
        fields = ('id', 'name', 'phone', 'notes', 'tours', 'fee', 'total')


class GuideWithDataByMonthSerializer(serializers.ModelSerializer):
    tours = serializers.SerializerMethodField()
    total = serializers.SerializerMethodField()

    def get_total(self, guide):
        context = self.context
        month = context.get('month', None)
        if month is None:
            return 0
        return sum([tour.guide.fee + tour.supplementary_fee for tour in guide.tours.filter(day__month=month)])

    def get_tours(self, guide):
        context = self.context
        month = context.get('month', None)
        if month is None:
            return []
        serializer = TourSerializer(
            guide.tours.filter(day__month=month), many=True)
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
    location = LocationSerializer(required=False)
    name = serializers.SerializerMethodField()

    def get_name(self, destination):
        return str(destination)

    class Meta:
        model = Destination
        fields = ('id', 'name', 'file_name',
                  'location', 'vessel', 'eta')
