from rest_framework import serializers
from guide.models import Guide, ResponseStatus

class GuideSerializer(serializers.ModelSerializer):
    class Meta:
        model = Guide
        fields = ('id', 'name', 'phone', 'notes')
