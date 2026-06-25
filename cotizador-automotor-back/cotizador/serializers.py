from rest_framework import serializers
from .models import Marca, Modelo, TarifaBase, FactorRiesgo, Cotizacion


class MarcaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Marca
        fields = ['id', 'nombre', 'codigo']


class ModeloSerializer(serializers.ModelSerializer):
    marca_nombre = serializers.CharField(source='marca.nombre', read_only=True)

    class Meta:
        model = Modelo
        fields = ['id', 'nombre', 'marca', 'marca_nombre', 'anio_desde',
                  'anio_hasta', 'valor_venal_base', 'segmento']


class TarifaSerializer(serializers.ModelSerializer):
    cobertura_label = serializers.CharField(source='get_cobertura_display', read_only=True)

    class Meta:
        model = TarifaBase
        fields = ['cobertura', 'cobertura_label', 'tasa_base', 'descripcion',
                  'incluye', 'franquicia_pct']


class FactorRiesgoSerializer(serializers.ModelSerializer):
    tipo_label = serializers.CharField(source='get_tipo_display', read_only=True)

    class Meta:
        model = FactorRiesgo
        fields = ['tipo', 'tipo_label', 'codigo', 'label', 'factor', 'orden']


class CotizarInputSerializer(serializers.Serializer):
    marca_id = serializers.IntegerField()
    modelo_id = serializers.IntegerField()
    anio = serializers.IntegerField(min_value=1990, max_value=2026)
    cobertura = serializers.ChoiceField(choices=['rco', 'terceros', 'terceros_plus', 'todo_riesgo'])
    zona = serializers.CharField(max_length=50)
    uso = serializers.CharField(max_length=50)
    edad_conductor = serializers.IntegerField(min_value=18, max_value=99)
    tiene_siniestros = serializers.BooleanField(default=False)


class GuardarCotizacionSerializer(serializers.Serializer):
    marca_id = serializers.IntegerField()
    modelo_id = serializers.IntegerField()
    anio = serializers.IntegerField()
    cobertura = serializers.CharField()
    zona = serializers.CharField()
    uso = serializers.CharField()
    edad_conductor = serializers.IntegerField()
    tiene_siniestros = serializers.BooleanField(default=False)
    nombre_conductor = serializers.CharField(max_length=200)
    email = serializers.EmailField()
    dni = serializers.CharField(max_length=20, required=False, allow_blank=True)
    valor_venal = serializers.DecimalField(max_digits=14, decimal_places=2)
    prima_mensual = serializers.DecimalField(max_digits=12, decimal_places=2)
    prima_anual = serializers.DecimalField(max_digits=12, decimal_places=2)
    factor_total = serializers.DecimalField(max_digits=6, decimal_places=4)
    desglose = serializers.JSONField()


class CotizacionListSerializer(serializers.ModelSerializer):
    marca_nombre = serializers.CharField(source='marca.nombre', read_only=True)
    modelo_nombre = serializers.CharField(source='modelo.nombre', read_only=True)

    class Meta:
        model = Cotizacion
        fields = ['id', 'numero', 'nombre_conductor', 'email', 'marca_nombre',
                  'modelo_nombre', 'anio', 'cobertura_elegida', 'prima_mensual',
                  'prima_anual', 'estado', 'created_at']
