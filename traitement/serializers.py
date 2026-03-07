from rest_framework import serializers
from .models import TraitementImage, ComparaisonNDVI

class TraitementImageSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = TraitementImage
        fields = '__all__'

class ComparaisonNDVISerializer(serializers.ModelSerializer):

    class Meta:
        model = ComparaisonNDVI
        fields = '__all__'