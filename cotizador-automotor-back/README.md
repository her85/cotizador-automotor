# Cotizador Automotor — Backend

Motor de cotización de seguros automotor con Django + DRF.

## Instalación

```bash
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_data   # carga marcas, modelos, tarifas y factores
python manage.py runserver
```

## Endpoints

| Método | URL | Descripción |
|--------|-----|-------------|
| GET | `/api/opciones/` | Marcas, zonas, usos, coberturas y años (una sola llamada) |
| GET | `/api/modelos/?marca=1` | Modelos filtrados por marca |
| POST | `/api/cotizar/` | Calcula prima sin persistir |
| POST | `/api/cotizaciones/guardar/` | Persiste la cotización |
| GET | `/api/cotizaciones/` | Listado de últimas 50 cotizaciones |

## Lógica de tarifación

```
prima_anual = valor_venal × tasa_base × factor_total

factor_total = f_marca × f_zona × f_uso × f_antigüedad × f_edad × f_siniestralidad
```

Coberturas: RCO · Terceros · Terceros Plus · Todo Riesgo
