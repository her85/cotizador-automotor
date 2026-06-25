import { ref, onMounted } from 'vue'
import { cotizadorApi } from '../api/cotizador'
import type { OpcionesForm } from '../types'

export function useOpciones() {
  const opciones = ref<OpcionesForm | null>(null)
  const loading = ref(true)
  const error = ref<string | null>(null)

  onMounted(async () => {
    try {
      opciones.value = await cotizadorApi.getOpciones()
    } catch {
      error.value = 'No se pudieron cargar las opciones del formulario'
    } finally {
      loading.value = false
    }
  })

  return { opciones, loading, error }
}
