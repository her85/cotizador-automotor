export interface Marca {
  id: number
  nombre: string
  codigo: string
}

export interface Modelo {
  id: number
  nombre: string
  marca: number
  marca_nombre: string
  anio_desde: number
  anio_hasta: number | null
  valor_venal_base: number
  segmento: string
}

export interface Cobertura {
  cobertura: string
  label: string
  descripcion: string
  incluye: string[]
  franquicia_pct: number
}

export interface OpcionForm {
  codigo: string
  label: string
  factor: number
}

export interface OpcionesForm {
  marcas: Marca[]
  zonas: OpcionForm[]
  usos: OpcionForm[]
  coberturas: Cobertura[]
  anios: number[]
}

export interface CotizarInput {
  marca_id: number
  modelo_id: number
  anio: number
  cobertura: string
  zona: string
  uso: string
  edad_conductor: number
  tiene_siniestros: boolean
}

export interface ResultadoCotizacion {
  marca: string
  modelo: string
  anio: number
  cobertura: string
  cobertura_label: string
  valor_venal: number
  prima_mensual: number
  prima_anual: number
  factor_total: number
  franquicia_pct: number
  incluye: string[]
  desglose: {
    tasa_base_pct: number
    factor_marca: number
    factor_zona: number
    factor_uso: number
    factor_antiguedad: number
    factor_edad: number
    factor_siniestralidad: number
    factor_total: number
  }
}

export interface DatosContacto {
  nombre_conductor: string
  email: string
  dni: string
}

export type WizardStep = 1 | 2 | 3 | 4

export interface WizardState {
  step: WizardStep
  vehiculo: {
    marca_id: number | null
    modelo_id: number | null
    anio: number | null
  }
  conductor: {
    edad_conductor: number | null
    zona: string
    uso: string
    tiene_siniestros: boolean
  }
  cobertura: string
  contacto: DatosContacto
  resultado: ResultadoCotizacion | null
  numeroCotizacion: string | null
}
