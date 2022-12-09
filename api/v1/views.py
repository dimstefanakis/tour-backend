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
