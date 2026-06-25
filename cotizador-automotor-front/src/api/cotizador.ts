import { client } from './client'
import type { OpcionesForm, Modelo, ResultadoCotizacion, CotizarInput } from '../types'

export const cotizadorApi = {
  getOpciones: () =>
    client.get<OpcionesForm>('/opciones/').then(r => r.data),

  getModelos: (marcaId: number) =>
    client.get<{ results: Modelo[] }>('/modelos/', { params: { marca: marcaId } })
      .then(r => r.data.results ?? r.data),

  cotizar: (data: CotizarInput) =>
    client.post<ResultadoCotizacion>('/cotizar/', data).then(r => r.data),

  guardar: (data: Record<string, unknown>) =>
    client.post<{ numero: string; id: number }>('/cotizaciones/guardar/', data).then(r => r.data),
}
