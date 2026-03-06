from rest_framework import serializers
from .models import TraitementImage

class TraitementImageSerializer(serializers.Serializer):
    surfaces_clas = serializers.SerializerMethodField()
    class Meta:
        model = TraitementImage
        fields = '__all__'
    def get_surfaces_clas(self,obj):
        pass