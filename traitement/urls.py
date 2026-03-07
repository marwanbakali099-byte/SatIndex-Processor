from django.urls import path, include
from .views import Ndvi,TraitementImage_ViewSet,ComparaisonNDVI
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'traitement',TraitementImage_ViewSet,basename='traitImg')
urlpatterns = [
    path('',include(router.urls)),
    path('ndvi/<int:id_trait>/',Ndvi.as_view(),name="ndvi"),
    path('comp/<int:id_anciennne>/<int:id_recente>',ComparaisonNDVI.as_view(),name="comp_ndvi"),
]