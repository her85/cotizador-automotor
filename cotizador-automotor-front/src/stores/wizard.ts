import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { WizardState, WizardStep, ResultadoCotizacion } from '../types'

export const useWizardStore = defineStore('wizard', () => {
  const state = ref<WizardState>({
    step: 1,
    vehiculo: { marca_id: null, modelo_id: null, anio: null },
    conductor: { edad_conductor: null, zona: '', uso: '', tiene_siniestros: false },
    cobertura: '',
    contacto: { nombre_conductor: '', email: '', dni: '' },
    resultado: null,
    numeroCotizacion: null,
  })

  const isStep1Valid = computed(() =>
    state.value.vehiculo.marca_id !== null &&
    state.value.vehiculo.modelo_id !== null &&
    state.value.vehiculo.anio !== null
  )

  const isStep2Valid = computed(() =>
    state.value.conductor.edad_conductor !== null &&
    state.value.conductor.zona !== '' &&
    state.value.conductor.uso !== ''
  )

  const isStep3Valid = computed(() => state.value.cobertura !== '')

  const isStep4Valid = computed(() =>
    state.value.contacto.nombre_conductor.trim() !== '' &&
    state.value.contacto.email.includes('@')
  )

  function goTo(step: WizardStep) {
    state.value.step = step
  }

  function setResultado(r: ResultadoCotizacion) {
    state.value.resultado = r
  }

  function setNumeroCotizacion(n: string) {
    state.value.numeroCotizacion = n
  }

  function reset() {
    state.value = {
      step: 1,
      vehiculo: { marca_id: null, modelo_id: null, anio: null },
      conductor: { edad_conductor: null, zona: '', uso: '', tiene_siniestros: false },
      cobertura: '',
      contacto: { nombre_conductor: '', email: '', dni: '' },
      resultado: null,
      numeroCotizacion: null,
    }
  }

  return { state, isStep1Valid, isStep2Valid, isStep3Valid, isStep4Valid, goTo, setResultado, setNumeroCotizacion, reset }
})
