from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from guide.models import Guide, ResponseStatus
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


@api_view(['GET'])
@permission_classes([AllowAny])
def get_guide_availability_by_day(request, pk):
    guide = Guide.objects.get(id=pk)
    day = request.GET.get('day', None)
    if day is None:
        return Response({'error': 'day parameter is required'})
    response_statuses = ResponseStatus.objects.filter(guide=guide,
                                                      day=day).first()
    serializer = serializers.ResponseStatusSerializer(response_statuses)
    return Response(serializer.data)


# status=ResponseStatus.STATUS.YES

@api_view(['POST'])
@permission_classes([AllowAny])
def create_guide_availability(request, pk):
    guide = Guide.objects.get(id=pk)
    serializer = serializers.ResponseStatusSerializer(
        data=request.data, pk=guide)
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
    response_statuses = ResponseStatus.objects.filter(guide=guide,
                                                      status=ResponseStatus.STATUS.YES)
    serializer = serializers.ResponseStatusSerializer(
        response_statuses, many=True)
    return Response(serializer.data)
