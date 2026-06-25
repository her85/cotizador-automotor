from django.contrib import admin
from .models import Marca, Modelo, TarifaBase, FactorRiesgo, Cotizacion


@admin.register(Marca)
class MarcaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'codigo', 'factor_marca']


@admin.register(Modelo)
class ModeloAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'marca', 'anio_desde', 'anio_hasta', 'valor_venal_base', 'segmento']
    list_filter = ['marca', 'segmento']


@admin.register(TarifaBase)
class TarifaAdmin(admin.ModelAdmin):
    list_display = ['cobertura', 'tasa_base', 'franquicia_pct']


@admin.register(FactorRiesgo)
class FactorAdmin(admin.ModelAdmin):
    list_display = ['tipo', 'codigo', 'label', 'factor']
    list_filter = ['tipo']


@admin.register(Cotizacion)
class CotizacionAdmin(admin.ModelAdmin):
    list_display = ['numero', 'nombre_conductor', 'marca', 'modelo', 'anio',
                    'cobertura_elegida', 'prima_mensual', 'estado', 'created_at']
    list_filter = ['estado', 'cobertura_elegida']
    readonly_fields = ['numero', 'created_at']
