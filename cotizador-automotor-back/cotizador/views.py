from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Marca, Modelo, TarifaBase, FactorRiesgo, Cotizacion
from .serializers import (
    MarcaSerializer, ModeloSerializer, TarifaSerializer, FactorRiesgoSerializer,
    CotizarInputSerializer, GuardarCotizacionSerializer, CotizacionListSerializer,
)
from .services import cotizar, CotizadorError


class MarcaViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Marca.objects.all()
    serializer_class = MarcaSerializer


class ModeloViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ModeloSerializer

    def get_queryset(self):
        qs = Modelo.objects.select_related('marca').all()
        marca_id = self.request.query_params.get('marca')
        if marca_id:
            qs = qs.filter(marca_id=marca_id)
        return qs


class TarifaViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = TarifaBase.objects.all()
    serializer_class = TarifaSerializer
    lookup_field = 'cobertura'


class FactorRiesgoViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = FactorRiesgoSerializer

    def get_queryset(self):
        qs = FactorRiesgo.objects.all()
        tipo = self.request.query_params.get('tipo')
        if tipo:
            qs = qs.filter(tipo=tipo)
        return qs


@api_view(['POST'])
def cotizar_view(request):
    """Calcula la prima sin guardar la cotización."""
    ser = CotizarInputSerializer(data=request.data)
    if not ser.is_valid():
        return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)

    try:
        resultado = cotizar(**ser.validated_data)
        return Response(resultado)
    except CotizadorError as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def guardar_cotizacion(request):
    """Persiste la cotización y devuelve el número generado."""
    ser = GuardarCotizacionSerializer(data=request.data)
    if not ser.is_valid():
        return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)

    d = ser.validated_data
    try:
        marca = Marca.objects.get(pk=d['marca_id'])
        modelo = Modelo.objects.get(pk=d['modelo_id'])
    except (Marca.DoesNotExist, Modelo.DoesNotExist):
        return Response({'error': 'Marca o modelo no encontrado'}, status=400)

    cot = Cotizacion.objects.create(
        marca=marca, modelo=modelo,
        anio=d['anio'], valor_venal=d['valor_venal'],
        nombre_conductor=d['nombre_conductor'], email=d['email'],
        dni=d.get('dni', ''), edad_conductor=d['edad_conductor'],
        tiene_siniestros=d['tiene_siniestros'],
        zona=d['zona'], uso=d['uso'],
        cobertura_elegida=d['cobertura'],
        prima_mensual=d['prima_mensual'], prima_anual=d['prima_anual'],
        factor_total=d['factor_total'], desglose=d['desglose'],
    )
    return Response({'numero': cot.numero, 'id': cot.id}, status=status.HTTP_201_CREATED)


@api_view(['GET'])
def listar_cotizaciones(request):
    qs = Cotizacion.objects.select_related('marca', 'modelo').all()[:50]
    return Response(CotizacionListSerializer(qs, many=True).data)


@api_view(['GET'])
def opciones_form(request):
    """Devuelve todas las opciones del formulario en una sola llamada."""
    zonas = FactorRiesgo.objects.filter(tipo='zona').values('codigo', 'label', 'factor').order_by('orden')
    usos = FactorRiesgo.objects.filter(tipo='uso').values('codigo', 'label', 'factor').order_by('orden')
    coberturas = TarifaBase.objects.all().values('cobertura', 'descripcion', 'incluye', 'franquicia_pct')
    marcas = Marca.objects.all().values('id', 'nombre')

    cobertura_labels = dict(TarifaBase._meta.get_field('cobertura').choices)

    return Response({
        'marcas': list(marcas),
        'zonas': list(zonas),
        'usos': list(usos),
        'coberturas': [
            {**c, 'label': cobertura_labels.get(c['cobertura'], c['cobertura'])}
            for c in coberturas
        ],
        'anios': list(range(2026, 1994, -1)),
    })
