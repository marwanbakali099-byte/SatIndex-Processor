from rest_framework import serializers
from .models import TraitementImage

class TraitementImageSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = TraitementImage
        fields = '__all__'