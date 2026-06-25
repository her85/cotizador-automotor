"""
Motor de cotización.
Calcula la prima mensual y anual aplicando factores de riesgo sobre la
tasa base de la cobertura elegida y el valor venal del vehículo.
"""
from decimal import Decimal
from .models import TarifaBase, FactorRiesgo, Marca, Modelo


class CotizadorError(Exception):
    pass


def calcular_valor_venal(modelo: Modelo, anio: int) -> Decimal:
    """
    Ajusta el valor venal base por antigüedad del vehículo.
    Depreciación anual aproximada: 8% acumulativo.
    """
    from datetime import date
    anios_antiguedad = max(date.today().year - anio, 0)
    depreciacion = Decimal('0.92') ** anios_antiguedad
    return (modelo.valor_venal_base * depreciacion).quantize(Decimal('0.01'))


def get_factor(tipo: str, codigo: str) -> Decimal:
    try:
        return FactorRiesgo.objects.get(tipo=tipo, codigo=codigo).factor
    except FactorRiesgo.DoesNotExist:
        return Decimal('1.000')


def cotizar(
    marca_id: int,
    modelo_id: int,
    anio: int,
    cobertura: str,
    zona: str,
    uso: str,
    edad_conductor: int,
    tiene_siniestros: bool = False,
) -> dict:
    """
    Devuelve el desglose completo de la cotización.
    """
    try:
        marca = Marca.objects.get(pk=marca_id)
        modelo = Modelo.objects.get(pk=modelo_id, marca=marca)
        tarifa = TarifaBase.objects.get(cobertura=cobertura)
    except (Marca.DoesNotExist, Modelo.DoesNotExist):
        raise CotizadorError('Marca o modelo no encontrado')
    except TarifaBase.DoesNotExist:
        raise CotizadorError(f'Cobertura "{cobertura}" no configurada')

    # Valor venal ajustado
    valor_venal = calcular_valor_venal(modelo, anio)

    # Factores individuales
    f_marca = marca.factor_marca
    f_zona = get_factor('zona', zona)
    f_uso = get_factor('uso', uso)
    f_antig = get_factor('antiguedad', _bucket_antiguedad(anio))
    f_edad = get_factor('edad_conductor', _bucket_edad(edad_conductor))
    f_sinies = Decimal('1.150') if tiene_siniestros else Decimal('1.000')

    factor_total = (f_marca * f_zona * f_uso * f_antig * f_edad * f_sinies).quantize(Decimal('0.0001'))

    # Prima anual = valor_venal * tasa_base * factor_total
    prima_anual = (valor_venal * tarifa.tasa_base * factor_total).quantize(Decimal('0.01'))
    prima_mensual = (prima_anual / 12).quantize(Decimal('0.01'))

    return {
        'marca': marca.nombre,
        'modelo': str(modelo),
        'anio': anio,
        'cobertura': cobertura,
        'cobertura_label': tarifa.get_cobertura_display(),
        'valor_venal': float(valor_venal),
        'prima_mensual': float(prima_mensual),
        'prima_anual': float(prima_anual),
        'factor_total': float(factor_total),
        'franquicia_pct': float(tarifa.franquicia_pct),
        'incluye': tarifa.incluye,
        'desglose': {
            'tasa_base_pct': float(tarifa.tasa_base * 100),
            'factor_marca': float(f_marca),
            'factor_zona': float(f_zona),
            'factor_uso': float(f_uso),
            'factor_antiguedad': float(f_antig),
            'factor_edad': float(f_edad),
            'factor_siniestralidad': float(f_sinies),
            'factor_total': float(factor_total),
        },
    }


def _bucket_antiguedad(anio: int) -> str:
    from datetime import date
    anios = date.today().year - anio
    if anios <= 2:
        return '0_2'
    elif anios <= 5:
        return '3_5'
    elif anios <= 10:
        return '6_10'
    else:
        return '11_mas'


def _bucket_edad(edad: int) -> str:
    if edad < 25:
        return 'menor_25'
    elif edad <= 35:
        return '25_35'
    elif edad <= 55:
        return '36_55'
    else:
        return '56_mas'
