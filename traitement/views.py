from django.http import HttpResponse
from django.shortcuts import render
from .serializers import TraitementImageSerializer ,ComparaisonNDVISerializer
from .models import TraitementImage, ComparaisonNDVI
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView, Response
from django.shortcuts import get_object_or_404
from rest_framework import status
import rasterio
import numpy as np
import os
from django.conf import settings
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from io import BytesIO

# les methode crude de modèle Traitement Image
class TraitementImage_ViewSet(ModelViewSet):
    queryset = TraitementImage.objects.all()
    serializer_class = TraitementImageSerializer

# les methode crude de modèle Comparaison
class ComparaisonNDVI_ViewSet(ModelViewSet):
    queryset = ComparaisonNDVI.objects.all()
    serializer_class = ComparaisonNDVISerializer

# Calcule NDVI
class Ndvi(APIView):
    def get(self,request,id_trait):
        traitement = get_object_or_404(TraitementImage,id=id_trait)

        folder_path = "sat/result"

        filename_ndvi = f"ndvi_{id_trait}.tiff"
        filename_class = f"class_{id_trait}.tiff"
        filename_rgb = f"rgb_{id_trait}.tiff"

        rel_path_ndvi = os.path.join(folder_path, filename_ndvi)
        rel_path_class = os.path.join(folder_path, filename_class)
        rel_path_rgb = os.path.join(folder_path, filename_rgb)

        full_path_out = os.path.join(settings.MEDIA_ROOT, rel_path_ndvi)
        class_path_out = os.path.join(settings.MEDIA_ROOT, rel_path_class)
        rgb_path_out = os.path.join(settings.MEDIA_ROOT, rel_path_rgb)


        # Créer le dossier s'il n'existe pas
        os.makedirs(os.path.dirname(full_path_out), exist_ok=True)
        with rasterio.open(traitement.bande_1.path) as band_1:
            with rasterio.open(traitement.bande_4.path) as band_4:

                # Conversion en float32 pour avoir les chiffres après la virgule
                red = band_1.read(1).astype('float32')
                pir = band_4.read(1).astype('float32')  
                # calcule NDVI
                ndvi = (pir-red)/(pir+red+1e-10)
                # affecter moyenne NDVI
                moy_ndvi = float(np.nanmean(ndvi))
                traitement.moyen_ndvi = moy_ndvi
                # affecter standard deviation
                std_ndvi = float(np.nanstd(ndvi))
                traitement.standard_deviation = std_ndvi
                # On remplace les valeurs invalides (NaN) par 0
                ndvi = np.nan_to_num(ndvi)
                # Méta-données de l'image satellite
                meta = band_1.meta
                meta.update(dtype='float32', count=1, driver='GTiff')
                # 4. Enregistrer
                with rasterio.open(full_path_out, 'w', **meta) as dst:
                    dst.write(ndvi, 1)
                # classification de NDVI
                #Création d'une nouvelle image de la même taille de NDVI et remplir par des zeros
                classification = np.zeros_like(ndvi)
                # classe (Végétation) Tous les pixels où le NDVI est supérieur à 0.3 reçoivent la valeur 1
                classification[ndvi>=0.3] = 1
                # class Light vegetation
                classification[(ndvi>=0.1)&(ndvi<0.3)] = 2
                # classe (urbain/ sol nu) Tous les pexels où le NDVI est inférieur à 0.1 et supérieur à 0 reçoivent la valeur 2
                classification[(ndvi<0.1)&(ndvi>0)] = 3
                # classe (eau/ mer) 
                classification[ndvi<=0] = 4
                with rasterio.open(class_path_out,'w',**meta) as cls:
                    cls.write(classification,1)
                # surfaces de classification
                res_x,res_y = band_1.res
                nb_pixels_vegetation = np.sum(classification==1)
                nb_pixels_Light_vegetation = np.sum(classification==2)
                nb_pixels_urbain_sol_nu = np.sum(classification==3)
                nb_pixels_eau = np.sum(classification==4)
                # les surface de chaque classification de végétation
                surface_vegetation = (nb_pixels_vegetation*abs(res_x*res_y))/1000000 # par km²
                surface_urbain_sol_nu = (nb_pixels_urbain_sol_nu*abs(res_x*res_y))/1000000
                surface_Light_vegetation = (nb_pixels_Light_vegetation*abs(res_x*res_y))/1000000
                surface_eau = (nb_pixels_eau*res_x*res_y)/1000000
                surfaces = {
                    'surface_vegetation':surface_vegetation,
                    'surface_urbain_sol_nu':surface_urbain_sol_nu,
                    'surface_Light_vegetation':surface_Light_vegetation,
                    'surface_eau':surface_eau
                }
                # généré l'image par true color
                with rasterio.open(traitement.bande_2.path) as bande_2:
                    with rasterio.open(traitement.bande_3.path) as bande_3 :
                        green = bande_2.read(1) 
                        blue = bande_3.read(1) 
                        meta_rgb = meta.copy()
                        meta_rgb.update(count=3)
                        with rasterio.open(rgb_path_out, 'w', **meta_rgb) as bgr:
                            bgr.write(red,1)
                            bgr.write(green,2)
                            bgr.write(blue,3)
        # affecter image indvi à DB
        traitement.ndvi_img = rel_path_ndvi
        traitement.class_ndvi = rel_path_class
        traitement.surfaces_clas = surfaces
        traitement.true_color_img = rel_path_rgb
        traitement.save()
        # 4. Retourner la réponse via le Serializer
        serializer = TraitementImageSerializer(traitement)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

class ComparaisonNDVI_View(APIView):
    def get(self,request,id_anciennne,id_recente):
        traitement_img_1 = get_object_or_404(TraitementImage,id=id_anciennne)
        traitement_img_2 = get_object_or_404(TraitementImage,id=id_recente)
        date_traitement_1 = traitement_img_1.date_traitement
        date_traitement_2 = traitement_img_2.date_traitement
        
        diff_date = float((date_traitement_2-date_traitement_1).days)
        
        file_path = 'sat/result'
        
        fieldname_diff_ndvi = f"ndvi_{id_anciennne}&{id_recente}.tiff"
        
        rel_path_diff_ndvi = os.path.join(file_path,fieldname_diff_ndvi)
        
        full_path_out_diff = os.path.join(settings.MEDIA_ROOT, rel_path_diff_ndvi)

        with rasterio.open(traitement_img_1.ndvi_img.path) as ancienne :
            with rasterio.open(traitement_img_2.ndvi_img.path) as recente :
                ancienne_ndvi = ancienne.read(1)
                recente_ndvi = recente.read(1)
                diff_ndvi = recente_ndvi - ancienne_ndvi
                diff_ndvi = np.nan_to_num(diff_ndvi) 
                meta = recente.meta
                meta.update(dtype='float32', count=1, driver='GTiff')
                with rasterio.open(full_path_out_diff,'w',**meta) as diff:
                    diff.write(diff_ndvi,1)
                diff_surf = {
                    'surface_vegetation':traitement_img_2.surfaces_clas['surface_vegetation']-traitement_img_1.surfaces_clas['surface_vegetation'],
                    'surface_urbain_sol_nu':traitement_img_2.surfaces_clas['surface_urbain_sol_nu']-traitement_img_1.surfaces_clas['surface_urbain_sol_nu'],
                    'surface_Light_vegetation':traitement_img_2.surfaces_clas['surface_Light_vegetation']-traitement_img_1.surfaces_clas['surface_Light_vegetation'],
                    'surface_eau':traitement_img_2.surfaces_clas['surface_eau']-traitement_img_1.surfaces_clas['surface_eau']
                }
                comparaison = ComparaisonNDVI.objects.create(
                    id_img_ancienne = traitement_img_1,
                    id_img_recente = traitement_img_2,
                    diff_date = diff_date,
                    diff_img = rel_path_diff_ndvi,
                    diff_surface_class = diff_surf
                )
                return Response({"status": "success","message": "La comparaison a été générée avec succès","data": {"id": comparaison.id,"diff_date_days": diff_date,"resultats_surfaces": diff_surf,"image_url": rel_path_diff_ndvi}}, status=status.HTTP_201_CREATED)

class GenerateRapport(APIView):
    def get(self,request,id_ancienne,id_recente):
        comparaison = get_object_or_404(ComparaisonNDVI,id_img_ancienne=id_ancienne,id_img_recente=id_recente)
        # 2. Préparation du buffer PDF
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4)
        elements = []
        styles = getSampleStyleSheet()
        
        # --- TITRE DU RAPPORT ---
        title = f"Rapport d'Analyse de Changement NDVI"
        elements.append(Paragraph(title, styles['Title']))
        elements.append(Spacer(1, 12))
        
        # --- INFORMATIONS GÉNÉRALES ---
        info_text = f"""
        <b>ID Comparaison :</b> {comparaison.id}<br/>
        <b>Période entre les captures :</b> {comparaison.diff_date} jours<br/>
        <b>Date de génération :</b> {comparaison.date_comparaison.strftime('%d/%m/%Y %H:%M')}
        """
        elements.append(Paragraph(info_text, styles['Normal']))
        elements.append(Spacer(1, 20))

        # --- INSERTION DE L'IMAGE DE DIFFÉRENCE ---
        elements.append(Paragraph("<b>Carte de Différence NDVI :</b>", styles['Heading2']))
        if comparaison.diff_img:
            img_path = comparaison.diff_img.path
            # Ajuster la taille pour le PDF (A4)
            img = Image(img_path, width=400, height=300)
            elements.append(img)
        elements.append(Spacer(1, 20))

        # --- TABLEAU DES SURFACES ---
        elements.append(Paragraph("<b>Statistiques de Variation des Surfaces (km²) :</b>", styles['Heading2']))
        
        data = [["Classe de Sol", "Variation de Surface"]]
        for key, value in comparaison.diff_surface_class.items():
            # Formater le nom de la clé (ex: diff_vegetation -> Végétation)
            label = key.replace('surface_', '').replace('_', ' ').capitalize()
            data.append([label, f"{value:+.4f} km²"])

        # Style du tableau
        table = Table(data, colWidths=[200, 150])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        elements.append(table)
        
        # --- CONCLUSION AUTOMATIQUE ---
        elements.append(Spacer(1, 20))
        veg_diff = comparaison.diff_surface_class.get('surface_vegetation', 0)
        conclusion = "<b>Interprétation :</b> "
        if veg_diff > 0:
            conclusion += f"Une augmentation de {abs(veg_diff):.2f} km² de la végétation a été détectée."
        else:
            conclusion += f"Une perte de {abs(veg_diff):.2f} km² de la végétation a été observée."
        
        elements.append(Paragraph(conclusion, styles['Normal']))

        # 3. Génération finale
        doc.build(elements)
        
        # 4. Retourner le PDF
        buffer.seek(0)
        response = HttpResponse(buffer, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="rapport_ndvi_{id_ancienne}_{id_recente}.pdf"'
        return response