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
