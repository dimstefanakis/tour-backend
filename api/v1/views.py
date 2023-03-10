from django.db.models import Q, Count, Case, When, IntegerField
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from guide.models import Guide, ResponseStatus
from destination.models import Destination, Location, Vessel
from tour.models import Tour, TourLocation
from . import serializers


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_guides(request):
    guides = Guide.objects.all()
    serializer = serializers.GuideSerializer(guides, many=True)
    return Response(serializer.data)


@api_view(['GET', 'PATCH', 'DELETE'])
@permission_classes([AllowAny])
def get_guide(request, pk):
    guide = Guide.objects.get(id=pk)
    if request.method == 'GET':
        serializer = serializers.GuideSerializer(guide)
        return Response(serializer.data)
    elif request.method == 'PATCH':
        serializer = serializers.GuideSerializer(
            instance=guide, data=request.data)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data)
    elif request.method == 'DELETE':
        guide.delete()
        return Response('Guide was deleted')


@api_view(['POST'])
@permission_classes([AllowAny])
def create_guide(request):
    serializer = serializers.GuideSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)


@api_view(['PATCH'])
@permission_classes([AllowAny])
def update_guide(request, pk):
    guide = Guide.objects.get(id=pk)
    serializer = serializers.GuideSerializer(instance=guide, data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)


@api_view(['DELETE'])
@permission_classes([AllowAny])
def delete_guide(request, pk):
    guide = Guide.objects.get(id=pk)
    guide.delete()
    return Response('Guide was deleted')


@api_view(['POST'])
@permission_classes([AllowAny])
def get_guide_availability_by_day(request, pk):
    guide = Guide.objects.get(id=pk)
    day = request.data.get('day', None)
    if day is None:
        return Response({'error': 'day parameter is required'})
    response_statuses = ResponseStatus.objects.filter(guide=guide,
                                                      day=day).first()
    serializer = serializers.ResponseStatusSerializer(response_statuses)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([AllowAny])
def get_available_guides_by_day(request):
    day = request.data.get('day', None)
    if day is None:
        return Response({'error': 'day parameter is required'})
    guides = Guide.objects.filter(
        responses__day=day, responses__status=ResponseStatus.STATUS.YES).annotate(
    )

    serializer = serializers.GuideSerializer(guides, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([AllowAny])
def get_available_guides_for_location(request):
    day = request.data.get('day', None)
    location = TourLocation.objects.get(
        pk=request.data.get('location', None))
    tour = request.data.get('tour', None)
    if day is None:
        return Response({'error': 'day parameter is required'})

    guides = Guide.objects.filter(
        responses__day=day, responses__status=ResponseStatus.STATUS.YES).annotate(
        num_tours=Count('tours')
    ).annotate(
        num_tours=Count(
            Case(
                When(
                    Q(tours__day=day) &
                    Q(tours__destination__location__tour_locations__in=[
                      location]),
                    then=1
                ),
                output_field=IntegerField(),
            )
        )
    ).exclude(
        Q(num_tours__gte=2)
    )

    if tour:
        tour = Tour.objects.get(pk=tour)
        selected_guide = tour.guide
        if selected_guide not in guides:
            guides |= Guide.objects.filter(pk=selected_guide.pk)
    serializer = serializers.GuideSerializer(guides.distinct(), many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([AllowAny])
def get_confirmed_guides_by_date(request):
    date = request.data.get('date', None)
    if date is None:
        return Response({'error': 'date parameter is required'})
    # get tours for the date by this guide
    tours = Tour.objects.filter(day=date)
    # get guides for these tours
    guides = Guide.objects.filter(tours__in=tours)
    serializer = serializers.GuideWithTourByDaySerializer(
        guides.distinct('id'), many=True, context={'tours': tours})
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([AllowAny])
def create_guide_availability(request, pk):
    guide = Guide.objects.get(id=pk)
    serializer = serializers.ResponseStatusSerializer(
        data=request.data, pk=guide)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([AllowAny])
def create_guide_availability_multiple_dates(request, pk):
    guide = Guide.objects.get(id=pk)
    dates = request.data.get('dates', None)
    status = request.data.get('status', None)
    if dates is None or len(dates) == 0:
        return Response({'error': 'dates parameter is required'})
    for date in dates:
        serializer = serializers.ResponseStatusSerializer(
            data={'day': date, 'status': status, 'guide': guide.id})
        if serializer.is_valid():
            serializer.save()
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([AllowAny])
def get_guide_availability_between_dates(request, pk):
    guide = Guide.objects.get(id=pk)
    start_date = request.GET.get('start_date', None)
    end_date = request.GET.get('end_date', None)
    if start_date is None or end_date is None:
        return Response({'error': 'start_date and end_date parameters are required'})
    response_statuses = ResponseStatus.objects.filter(
        day__range=[start_date, end_date], guide=guide, status=ResponseStatus.STATUS.YES)
    serializer = serializers.ResponseStatusSerializer(
        response_statuses, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([AllowAny])
def get_guide_availability(request, pk):
    guide = Guide.objects.get(id=pk)
    response_statuses = ResponseStatus.objects.filter(
        guide=guide).order_by('day', '-created_at').distinct('day')
    serializer = serializers.ResponseStatusSerializer(
        response_statuses, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([AllowAny])
def get_guides_with_tours_by_month(request, pk):
    guide = Guide.objects.get(id=pk)
    month = request.data.get('month', None)
    if month is None:
        return Response({'error': 'month parameter is required'})
    serializer = serializers.GuideSerializer(guide, context={'month': month})
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([AllowAny])
def get_destinations(request):
    destinations = Destination.objects.all()
    serializer = serializers.DestinationSerializer(destinations, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([AllowAny])
def create_destination(request):
    location = request.data.pop('location', None)
    vessel = request.data.get('vessel', None)
    if location is not None and vessel is not None:
        created_location, location_created = Location.objects.get_or_create(
            name=location)
        created_vessel, vessel_created = Vessel.objects.get_or_create(
            name=vessel)
        serializer = serializers.DestinationSerializer(data=request.data)
        if serializer.is_valid():
            created_destination = serializer.save()
            created_destination.location = created_location
            created_destination.vessel = created_vessel
            created_destination.save()
            return Response(serializer.data)
    else:
        return Response({'error': 'location and vessel parameters are required'})
    return Response(serializer.errors)


@api_view(['POST'])
@permission_classes([AllowAny])
def get_destinations_by_date(request):
    date = request.data.get('date', None)
    if date is None:
        return Response({'error': 'date parameter is required'})
    destinations = Destination.objects.filter(eta__date=date)
    serializer = serializers.DestinationSerializer(destinations, many=True)
    return Response(serializer.data)


@api_view(['PATCH'])
@permission_classes([AllowAny])
def update_destination(request, pk):
    destination = Destination.objects.get(id=pk)
    serializer = serializers.DestinationSerializer(
        instance=destination, data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([AllowAny])
def get_tours(request):
    tours = Tour.objects.all()
    serializer = serializers.TourSerializer(tours, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([AllowAny])
def get_tours_by_destination(request, pk):
    destination = Destination.objects.get(id=pk)
    tours = Tour.objects.filter(destination=destination)
    serializer = serializers.TourSerializer(tours, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([AllowAny])
def get_tours_by_destination_and_day(request, pk):
    destination = Destination.objects.get(id=pk)
    day = request.data.get('day', None)
    if day is None:
        return Response({'error': 'day parameter is required'})
    tours = Tour.objects.filter(destination=destination, day=day)
    serializer = serializers.TourSerializer(tours, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([AllowAny])
def create_tour(request):
    destination = Destination.objects.get(
        id=request.data.get('destination', None))
    guide = Guide.objects.get(id=request.data.get('guide', None))
    tour_location = TourLocation.objects.get(
        id=request.data.get('location', None))
    tour_time = request.data.get('tour_time', None)
    date = request.data.get('date', None)
    if destination is None or guide is None or tour_location is None or tour_time is None or date is None:
        return Response({'error': 'destination, guide, location, tour_time and date parameters are required'})
    tour = Tour.objects.create(
        destination=destination, guide=guide, tour_location=tour_location, day=date, tour_time=tour_time)
    serializer = serializers.TourSerializer(tour)
    return Response(serializer.data)


@api_view(['PATCH'])
@permission_classes([AllowAny])
def update_tour(request, pk):
    tour = Tour.objects.get(id=pk)
    serializer = serializers.TourSerializer(
        instance=tour, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
    else:
        return Response(serializer.errors)
    return Response(serializer.data)


@api_view(['DELETE'])
@permission_classes([AllowAny])
def delete_tour(request, pk):
    tour = Tour.objects.get(id=pk)
    tour.delete()
    return Response({'message': 'Tour deleted successfully'})


@api_view(['GET'])
@permission_classes([AllowAny])
def get_locations(request):
    locations = TourLocation.objects.all()
    serializer = serializers.TourLocationSerializer(locations, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([AllowAny])
def assign_guide_to_tour(request, pk):
    tour = Tour.objects.get(id=pk)
    location = TourLocation.objects.get(id=request.data.get('location', None))
    guide = Guide.objects.get(id=request.data.get('guide', None))
    tour_time = request.data.get('tour_time', None)
    if location is None or guide is None or tour_time is None:
        return Response({'error': 'location, guide and tour_time parameters are required'})
    tour.tour_location = location
    tour.tour_time = tour_time
    tour.guide = guide
    tour.save()
    serializer = serializers.TourSerializer(tour)
    return Response(serializer.data)
