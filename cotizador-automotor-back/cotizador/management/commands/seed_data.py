from decimal import Decimal
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from cotizador.models import Marca, Modelo, TarifaBase, FactorRiesgo


class Command(BaseCommand):
    help = 'Carga datos de configuración del cotizador'

    def handle(self, *args, **kwargs):
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@example.com', 'admin123')

        # ── Marcas ──────────────────────────────────────────────────────────
        marcas_data = [
            ('Toyota',     'TOYOTA',  Decimal('1.050')),
            ('Volkswagen', 'VW',      Decimal('1.000')),
            ('Ford',       'FORD',    Decimal('1.020')),
            ('Chevrolet',  'CHEV',    Decimal('1.010')),
            ('Renault',    'RENAULT', Decimal('0.980')),
            ('Peugeot',    'PEUGEOT', Decimal('0.990')),
            ('Fiat',       'FIAT',    Decimal('0.970')),
            ('Honda',      'HONDA',   Decimal('1.030')),
            ('Nissan',     'NISSAN',  Decimal('1.040')),
            ('BMW',        'BMW',     Decimal('1.350')),
            ('Mercedes',   'MERC',    Decimal('1.380')),
            ('Audi',       'AUDI',    Decimal('1.320')),
        ]
        marcas = {}
        for nombre, cod, factor in marcas_data:
            m, _ = Marca.objects.get_or_create(
                codigo=cod, defaults={'nombre': nombre, 'factor_marca': factor}
            )
            marcas[cod] = m

        # ── Modelos ─────────────────────────────────────────────────────────
        modelos_data = [
            # (marca_cod, nombre, anio_desde, anio_hasta, valor_venal_base, segmento)
            ('TOYOTA',  'Corolla',       2018, None,  Decimal('18500000'), 'sedan'),
            ('TOYOTA',  'Hilux',         2018, None,  Decimal('32000000'), 'pickup'),
            ('TOYOTA',  'RAV4',          2019, None,  Decimal('28000000'), 'suv'),
            ('VW',      'Polo',          2018, None,  Decimal('14500000'), 'compacto'),
            ('VW',      'Golf',          2018, None,  Decimal('17000000'), 'compacto'),
            ('VW',      'Amarok',        2018, None,  Decimal('35000000'), 'pickup'),
            ('FORD',    'Focus',         2017, None,  Decimal('13000000'), 'sedan'),
            ('FORD',    'EcoSport',      2018, None,  Decimal('16500000'), 'suv'),
            ('FORD',    'Ranger',        2018, None,  Decimal('31000000'), 'pickup'),
            ('CHEV',    'Cruze',         2017, None,  Decimal('13500000'), 'sedan'),
            ('CHEV',    'Tracker',       2019, None,  Decimal('19000000'), 'suv'),
            ('RENAULT', 'Logan',         2018, None,  Decimal('11000000'), 'sedan'),
            ('RENAULT', 'Duster',        2018, None,  Decimal('15500000'), 'suv'),
            ('RENAULT', 'Kangoo',        2018, None,  Decimal('14000000'), 'utilitario'),
            ('PEUGEOT', '208',           2019, None,  Decimal('13000000'), 'compacto'),
            ('PEUGEOT', '3008',          2019, None,  Decimal('22000000'), 'suv'),
            ('FIAT',    'Cronos',        2018, None,  Decimal('12000000'), 'sedan'),
            ('FIAT',    'Toro',          2018, None,  Decimal('24000000'), 'pickup'),
            ('HONDA',   'Civic',         2019, None,  Decimal('19500000'), 'sedan'),
            ('HONDA',   'HR-V',          2019, None,  Decimal('22000000'), 'suv'),
            ('BMW',     '320i',          2020, None,  Decimal('55000000'), 'sedan'),
            ('MERC',    'C200',          2020, None,  Decimal('60000000'), 'sedan'),
            ('AUDI',    'A3',            2020, None,  Decimal('52000000'), 'sedan'),
        ]
        for cod, nombre, ad, ah, vv, seg in modelos_data:
            Modelo.objects.get_or_create(
                marca=marcas[cod], nombre=nombre, anio_desde=ad,
                defaults={'anio_hasta': ah, 'valor_venal_base': vv, 'segmento': seg}
            )

        # ── Tarifas base ────────────────────────────────────────────────────
        tarifas = [
            ('rco', Decimal('0.0150'), 0,
             'Cubre daños a terceros por RC obligatoria según ley.',
             ['Resp. Civil Obligatoria', 'Defensa penal']),
            ('terceros', Decimal('0.0280'), 0,
             'Incluye RC ampliada, incendio total y robo total.',
             ['Resp. Civil Obligatoria', 'RC Ampliada', 'Incendio total', 'Robo total', 'Defensa penal']),
            ('terceros_plus', Decimal('0.0380'), 5,
             'Terceros completo más granizo, inundación y robo parcial.',
             ['Resp. Civil', 'RC Ampliada', 'Incendio total', 'Robo total',
              'Robo parcial', 'Granizo', 'Inundación', 'Defensa penal']),
            ('todo_riesgo', Decimal('0.0520'), 10,
             'Cobertura completa incluyendo daños propios.',
             ['Todo lo anterior', 'Daños propios', 'Cristales', 'Asistencia mecánica 24h',
              'Auto de reemplazo', 'Accidentes personales']),
        ]
        for cod, tasa, franq, desc, incluye in tarifas:
            TarifaBase.objects.get_or_create(
                cobertura=cod,
                defaults={'tasa_base': tasa, 'franquicia_pct': franq,
                          'descripcion': desc, 'incluye': incluye}
            )

        # ── Factores de riesgo ───────────────────────────────────────────────
        factores = [
            # Zona
            ('zona', 'caba',      'CABA',       Decimal('1.250'), 0),
            ('zona', 'gba_norte', 'GBA Norte',  Decimal('1.150'), 1),
            ('zona', 'gba_sur',   'GBA Sur',    Decimal('1.180'), 2),
            ('zona', 'gba_oeste', 'GBA Oeste',  Decimal('1.170'), 3),
            ('zona', 'cordoba',   'Córdoba',    Decimal('1.050'), 4),
            ('zona', 'rosario',   'Rosario',    Decimal('1.080'), 5),
            ('zona', 'mendoza',   'Mendoza',    Decimal('1.000'), 6),
            ('zona', 'interior',  'Interior',   Decimal('0.950'), 7),
            # Uso
            ('uso', 'particular',  'Particular',            Decimal('1.000'), 0),
            ('uso', 'comercial',   'Comercial / Reparto',   Decimal('1.350'), 1),
            ('uso', 'remis',       'Remis / Taxi',          Decimal('1.500'), 2),
            ('uso', 'app',         'App de transporte',     Decimal('1.450'), 3),
            # Antigüedad
            ('antiguedad', '0_2',    '0 a 2 años',   Decimal('0.900'), 0),
            ('antiguedad', '3_5',    '3 a 5 años',   Decimal('1.000'), 1),
            ('antiguedad', '6_10',   '6 a 10 años',  Decimal('1.100'), 2),
            ('antiguedad', '11_mas', 'Más de 10 años', Decimal('1.250'), 3),
            # Edad conductor
            ('edad_conductor', 'menor_25', 'Menor de 25 años', Decimal('1.400'), 0),
            ('edad_conductor', '25_35',    '25 a 35 años',     Decimal('1.100'), 1),
            ('edad_conductor', '36_55',    '36 a 55 años',     Decimal('1.000'), 2),
            ('edad_conductor', '56_mas',   'Mayor de 55 años', Decimal('1.050'), 3),
            # Siniestralidad — se aplica en el servicio directamente (1.15)
        ]
        for tipo, cod, label, factor, orden in factores:
            FactorRiesgo.objects.get_or_create(
                tipo=tipo, codigo=cod,
                defaults={'label': label, 'factor': factor, 'orden': orden}
            )

        self.stdout.write(self.style.SUCCESS(
            f'Seed OK: {Marca.objects.count()} marcas, '
            f'{Modelo.objects.count()} modelos, '
            f'{TarifaBase.objects.count()} coberturas, '
            f'{FactorRiesgo.objects.count()} factores'
        ))
