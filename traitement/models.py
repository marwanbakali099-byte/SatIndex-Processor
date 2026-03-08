from django.db import models

class TraitementImage(models.Model):
    nom = models.CharField(max_length=50)
    date_traitement = models.DateTimeField(auto_now_add=True)
    description = models.TextField()
    bande_1 = models.ImageField(upload_to="sat/red")
    bande_2 = models.ImageField(upload_to="sat/green")
    bande_3 = models.ImageField(upload_to="sat/blue")
    bande_4 = models.ImageField(upload_to="sat/pir")
    moyen_ndvi = models.FloatField(null=True)
    standard_deviation = models.FloatField(null=True)
    true_color_img = models.ImageField(upload_to="sat/result/ture/",null=True)
    ndvi_img = models.ImageField(upload_to="sat/result/NDVI/",null=True)
    # pour image classifie par NDVI
    class_ndvi = models.ImageField(upload_to="sat/result/ture/",null=True)
    # pour stocker les surfaces de chaque classification de NDVI
    surfaces_clas = models.JSONField(null=True)

# un models qui stocker la résultat de comparaison de deux image sat
class ComparaisonNDVI(models.Model):
    id_img_ancienne = models.ForeignKey(TraitementImage,on_delete=models.CASCADE,related_name="comparaisons_anciennes")
    id_img_recente = models.ForeignKey(TraitementImage,on_delete=models.CASCADE,related_name="comparaisons_recente")
    date_comparaison = models.DateTimeField(auto_now_add=True)
    diff_date = models.FloatField(null=True)
    diff_img = models.ImageField(upload_to="sat/res/cmp/",null=True)
    diff_surface_class = models.JSONField(null=True)