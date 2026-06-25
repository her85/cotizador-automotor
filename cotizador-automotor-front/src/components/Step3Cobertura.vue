<script setup lang="ts">
import { ref, computed } from 'vue'
import { useWizardStore } from '../stores/wizard'
import { cotizadorApi } from '../api/cotizador'
import type { OpcionesForm } from '../types'

const props = defineProps<{ opciones: OpcionesForm }>()
const wizard = useWizardStore()
const loading = ref(false)
const error = ref<string | null>(null)

const ordenCobertura: Record<string, number> = { rco: 1, terceros: 2, terceros_plus: 3, todo_riesgo: 4 }
const coberturasSorted = computed(() =>
  [...props.opciones.coberturas].sort((a, b) => (ordenCobertura[a.cobertura] ?? 9) - (ordenCobertura[b.cobertura] ?? 9))
)

async function cotizarYSeguir() {
  if (!wizard.isStep3Valid) return
  loading.value = true
  error.value = null
  try {
    const resultado = await cotizadorApi.cotizar({
      marca_id: wizard.state.vehiculo.marca_id!,
      modelo_id: wizard.state.vehiculo.modelo_id!,
      anio: wizard.state.vehiculo.anio!,
      cobertura: wizard.state.cobertura,
      zona: wizard.state.conductor.zona,
      uso: wizard.state.conductor.uso,
      edad_conductor: wizard.state.conductor.edad_conductor!,
      tiene_siniestros: wizard.state.conductor.tiene_siniestros,
    })
    wizard.setResultado(resultado)
    wizard.goTo(4)
  } catch {
    error.value = 'Error al calcular la cotización. Verificá los datos.'
  } finally {
    loading.value = false
  }
}

const colorMap: Record<string, string> = {
  rco: 'border-slate-border hover:border-slate-text/60',
  terceros: 'border-blue-500/30 hover:border-blue-400/60',
  terceros_plus: 'border-teal-brand/30 hover:border-teal-brand/60',
  todo_riesgo: 'border-accent/30 hover:border-accent/70',
}
const selectedColor: Record<string, string> = {
  rco: 'border-slate-text bg-slate-border/20',
  terceros: 'border-blue-400 bg-blue-500/10',
  terceros_plus: 'border-teal-brand bg-teal-brand/10',
  todo_riesgo: 'border-accent bg-accent/10',
}
</script>

<template>
  <div class="space-y-5">
    <div>
      <p class="section-label mb-1">Paso 3</p>
      <h2 class="text-xl font-semibold text-white">Elegí tu cobertura</h2>
      <p class="text-sm text-slate-muted mt-1">Seleccioná el nivel de protección que necesitás.</p>
    </div>

    <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
      <div
        v-for="cob in coberturasSorted"
        :key="cob.cobertura"
        class="p-4 rounded-xl border-2 cursor-pointer transition-all duration-200"
        :class="wizard.state.cobertura === cob.cobertura
          ? selectedColor[cob.cobertura] || 'border-accent bg-accent/10'
          : colorMap[cob.cobertura] || 'border-slate-border hover:border-slate-text/60'"
        @click="wizard.state.cobertura = cob.cobertura"
      >
        <div class="flex items-start justify-between mb-2">
          <p class="font-semibold text-sm text-white">{{ cob.label }}</p>
          <div
            class="w-4 h-4 rounded-full border-2 flex-shrink-0 mt-0.5 flex items-center justify-center"
            :class="wizard.state.cobertura === cob.cobertura ? 'border-current bg-current' : 'border-slate-border'"
          >
            <div v-if="wizard.state.cobertura === cob.cobertura" class="w-1.5 h-1.5 rounded-full bg-navy-800"></div>
          </div>
        </div>
        <p class="text-xs text-slate-muted mb-3 leading-relaxed">{{ cob.descripcion }}</p>
        <ul class="space-y-1">
          <li v-for="item in cob.incluye.slice(0, 4)" :key="item" class="flex items-center gap-1.5 text-xs text-slate-text">
            <svg class="w-3 h-3 text-teal-brand flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M5 13l4 4L19 7"/>
            </svg>
            {{ item }}
          </li>
          <li v-if="cob.incluye.length > 4" class="text-xs text-slate-muted pl-4">
            +{{ cob.incluye.length - 4 }} más...
          </li>
        </ul>
        <div v-if="cob.franquicia_pct > 0" class="mt-3 pt-2 border-t border-slate-border/50">
          <span class="text-xs text-slate-muted">Franquicia: {{ cob.franquicia_pct }}% del valor venal</span>
        </div>
      </div>
    </div>

    <p v-if="error" class="text-sm text-red-400 bg-red-500/10 border border-red-500/20 rounded-lg px-4 py-2">
      {{ error }}
    </p>

    <div class="pt-2 flex flex-col sm:flex-row sm:justify-between gap-2">
      <button @click="wizard.goTo(2)" class="btn-ghost w-full sm:w-auto">← Anterior</button>
      <button @click="cotizarYSeguir" :disabled="!wizard.isStep3Valid || loading" class="btn-primary w-full sm:w-auto">
        <svg v-if="loading" class="w-4 h-4 animate-spin" fill="none" viewBox="0 0 24 24">
          <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/>
          <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"/>
        </svg>
        {{ loading ? 'Calculando...' : 'Calcular prima →' }}
      </button>
    </div>
  </div>
</template>
