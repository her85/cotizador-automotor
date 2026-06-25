from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('marcas', views.MarcaViewSet)
router.register('modelos', views.ModeloViewSet, basename='modelo')
router.register('tarifas', views.TarifaViewSet)
router.register('factores', views.FactorRiesgoViewSet, basename='factor')

urlpatterns = [
    path('', include(router.urls)),
    path('cotizar/', views.cotizar_view),
    path('cotizaciones/', views.listar_cotizaciones),
    path('cotizaciones/guardar/', views.guardar_cotizacion),
    path('opciones/', views.opciones_form),
]
