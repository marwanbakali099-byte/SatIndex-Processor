from django.shortcuts import render
from .serializers import TraitementImageSerializer
from .models import TraitementImage
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView, Response
from django.shortcuts import get_object_or_404
from rest_framework import status
import rasterio
import numpy as np
import os
from django.conf import settings

# les methode crude de modèle Traitement Image
class TraitementImage_ViewSet(ModelViewSet):
    queryset = TraitementImage.objects.all()
    serializer_class = TraitementImageSerializer

# Calcule NDVI
class Ndvi(APIView):
    def put(self,request,id_trait):
        traitment = get_object_or_404(TraitementImage,id=id_trait)
        filename = f"ndvi_{id_trait}.tiff"
        relative_path = os.path.join("sat/result/NDVI", filename)
        full_path_out = os.path.join(settings.MEDIA_ROOT, relative_path)
        # Créer le dossier s'il n'existe pas
        os.makedirs(os.path.dirname(full_path_out), exist_ok=True)
        with rasterio.open(traitment.bande_1.path) as band_1:
            with rasterio.open(traitment.bande_4.path) as band_4:

                # Conversion en float32 pour avoir les chiffres après la virgule
                red = band_1.read(1).astype('float32')
                pir = band_4.read(1).astype('float32')  
                # calcule NDVI
                ndvi = (pir-red)/(pir+red+1e-10)
                moy_ndvi = float(np.nanmean(ndvi))
                traitment.moyen_ndvi = moy_ndvi
                std_ndvi = float(np.nanstd(ndvi))
                traitment.standard_deviation = std_ndvi
                # On remplace les valeurs invalides (NaN) par 0
                ndvi = np.nan_to_num(ndvi)
                # Méta-données de l'image satellite
                meta = band_1.meta
                meta.update(dtype='float32', count=1, driver='GTiff')
                # 4. Enregistrer
                with rasterio.open(full_path_out, 'w', **meta) as dst:
                    dst.write(ndvi, 1)
        traitment.ndvi_img = relative_path
        traitment.save()
        # 4. Retourner la réponse via le Serializer
        serializer = TraitementImageSerializer(traitment)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
