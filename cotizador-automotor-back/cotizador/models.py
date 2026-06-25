from django.db import models


class Marca(models.Model):
    nombre = models.CharField(max_length=100)
    codigo = models.CharField(max_length=20, unique=True)
    factor_marca = models.DecimalField(
        max_digits=5, decimal_places=3, default=1.000,
        help_text='Multiplicador de prima base por marca (ej: 1.2 = 20% más caro)'
    )

    class Meta:
        ordering = ['nombre']

    def __str__(self):
        return self.nombre


class Modelo(models.Model):
    marca = models.ForeignKey(Marca, on_delete=models.CASCADE, related_name='modelos')
    nombre = models.CharField(max_length=150)
    anio_desde = models.PositiveIntegerField()
    anio_hasta = models.PositiveIntegerField(null=True, blank=True)
    valor_venal_base = models.DecimalField(
        max_digits=14, decimal_places=2,
        help_text='Valor venal de referencia en ARS'
    )
    segmento = models.CharField(max_length=50, choices=[
        ('compacto', 'Compacto'),
        ('sedan', 'Sedán'),
        ('suv', 'SUV'),
        ('pickup', 'Pick-up'),
        ('utilitario', 'Utilitario'),
        ('deportivo', 'Deportivo'),
    ], default='compacto')

    class Meta:
        ordering = ['marca__nombre', 'nombre']

    def __str__(self):
        return f'{self.marca.nombre} {self.nombre}'


class TarifaBase(models.Model):
    """Prima base mensual por cobertura como % del valor venal"""
    COBERTURA_CHOICES = [
        ('rco', 'Resp. Civil Obligatoria'),
        ('terceros', 'Terceros Completo'),
        ('terceros_plus', 'Terceros Plus'),
        ('todo_riesgo', 'Todo Riesgo'),
    ]
    cobertura = models.CharField(max_length=20, choices=COBERTURA_CHOICES, unique=True)
    tasa_base = models.DecimalField(
        max_digits=6, decimal_places=4,
        help_text='% anual sobre valor venal (ej: 0.0350 = 3.50%)'
    )
    descripcion = models.TextField(blank=True)
    incluye = models.JSONField(default=list, help_text='Lista de coberturas incluidas')
    franquicia_pct = models.DecimalField(
        max_digits=5, decimal_places=2, default=0,
        help_text='% de franquicia sobre valor venal'
    )

    def __str__(self):
        return self.get_cobertura_display()


class FactorRiesgo(models.Model):
    """Factores que ajustan la prima base"""
    TIPO_CHOICES = [
        ('zona', 'Zona geográfica'),
        ('uso', 'Uso del vehículo'),
        ('edad_conductor', 'Edad del conductor'),
        ('antiguedad', 'Antigüedad del vehículo'),
        ('siniestralidad', 'Historial de siniestros'),
    ]
    tipo = models.CharField(max_length=30, choices=TIPO_CHOICES)
    codigo = models.CharField(max_length=50)
    label = models.CharField(max_length=100)
    factor = models.DecimalField(
        max_digits=5, decimal_places=3,
        help_text='Multiplicador: 1.0 = sin cambio, 1.2 = +20%, 0.9 = -10%'
    )
    orden = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['tipo', 'orden']
        unique_together = ['tipo', 'codigo']

    def __str__(self):
        return f'{self.get_tipo_display()} – {self.label} ({self.factor})'


class Cotizacion(models.Model):
    """Registro de cotizaciones generadas"""
    ESTADO_CHOICES = [
        ('generada', 'Generada'),
        ('enviada', 'Enviada por email'),
        ('contratada', 'Contratada'),
        ('vencida', 'Vencida'),
    ]

    # Datos del vehículo
    marca = models.ForeignKey(Marca, on_delete=models.PROTECT)
    modelo = models.ForeignKey(Modelo, on_delete=models.PROTECT)
    anio = models.PositiveIntegerField()
    valor_venal = models.DecimalField(max_digits=14, decimal_places=2)

    # Datos del conductor
    nombre_conductor = models.CharField(max_length=200)
    email = models.EmailField()
    edad_conductor = models.PositiveIntegerField()
    dni = models.CharField(max_length=20, blank=True)
    tiene_siniestros = models.BooleanField(default=False)

    # Factores aplicados
    zona = models.CharField(max_length=50)
    uso = models.CharField(max_length=50)
    cobertura_elegida = models.CharField(max_length=20)

    # Resultado
    prima_mensual = models.DecimalField(max_digits=12, decimal_places=2)
    prima_anual = models.DecimalField(max_digits=12, decimal_places=2)
    factor_total = models.DecimalField(max_digits=6, decimal_places=4)
    desglose = models.JSONField(default=dict)

    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='generada')
    created_at = models.DateTimeField(auto_now_add=True)
    numero = models.CharField(max_length=20, unique=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.numero:
            import datetime
            ts = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
            self.numero = f'COT-{ts}'
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.numero} — {self.nombre_conductor}'
