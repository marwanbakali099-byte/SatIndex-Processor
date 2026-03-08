from django.urls import path, include
from .views import Ndvi,TraitementImage_ViewSet,ComparaisonNDVI_ViewSet,ComparaisonNDVI_View,GenerateRapport
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'traitement',TraitementImage_ViewSet,basename='traitImg')
router.register(r'comp',ComparaisonNDVI_ViewSet,basename='comp')
urlpatterns = [
    path('',include(router.urls)),
    path('ndvi/<int:id_trait>/',Ndvi.as_view(),name="ndvi"),
    path('comp/<int:id_anciennne>/<int:id_recente>/',ComparaisonNDVI_View.as_view(),name="comp_ndvi"),
    path('report/<int:id_ancienne>/<int:id_recente>/', GenerateRapport.as_view(), name="generate_report"),
]