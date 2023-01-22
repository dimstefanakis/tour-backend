from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from guide.models import Guide, ResponseStatus
from destination.models import Destination, Location
from tour.models import Tour
from . import serializers


@api_view(['GET'])
@permission_classes([AllowAny])
def get_guides(request):
    guides = Guide.objects.all()
    serializer = serializers.GuideSerializer(guides, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([AllowAny])
def get_guide(request, pk):
    guide = Guide.objects.get(id=pk)
    serializer = serializers.GuideSerializer(guide, many=False)
    return Response(serializer.data)


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
        responses__day=day, responses__status=ResponseStatus.STATUS.YES)
    serializer = serializers.GuideSerializer(guides, many=True)
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
def get_destinations_by_date(request):
    date = request.data.get('date', None)
    if date is None:
        return Response({'error': 'date parameter is required'})
    destinations = Destination.objects.filter(eta__lte=date, etd__gte=date)
    serializer = serializers.DestinationSerializer(destinations, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([AllowAny])
@parser_classes([MultiPartParser, FormParser])
def create_destination(request):
    serializer = serializers.DestinationSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
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
    location = Location.objects.get(id=request.data.get('location', None))
    date = request.data.get('date', None)
    if destination is None or guide is None or location is None:
        return Response({'error': 'destination, guide and location parameters are required'})
    tour = Tour.objects.create(
        destination=destination, guide=guide, location=location, day=date)
    serializer = serializers.TourSerializer(tour)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([AllowAny])
def get_locations(request):
    locations = Location.objects.all()
    serializer = serializers.LocationSerializer(locations, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([AllowAny])
def assign_guide_to_tour(request, pk):
    tour = Tour.objects.get(id=pk)
    location = Location.objects.get(id=request.data.get('location', None))
    guide = Guide.objects.get(id=request.data.get('guide', None))
    if location is None or guide is None:
        return Response({'error': 'location and guide parameters are required'})
    tour.location = location
    tour.guide = guide
    tour.save()
    serializer = serializers.TourSerializer(tour)
    return Response(serializer.data)
