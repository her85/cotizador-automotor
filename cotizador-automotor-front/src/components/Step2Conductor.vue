<script setup lang="ts">
import { computed } from 'vue'
import { useWizardStore } from '../stores/wizard'
import type { OpcionesForm } from '../types'

const props = defineProps<{ opciones: OpcionesForm }>()
const wizard = useWizardStore()
const c = computed(() => wizard.state.conductor)
</script>

<template>
  <div class="space-y-5">
    <div>
      <p class="section-label mb-1">Paso 2</p>
      <h2 class="text-xl font-semibold text-white">Datos del conductor</h2>
      <p class="text-sm text-slate-muted mt-1">Estos datos se usan para calcular el factor de riesgo.</p>
    </div>

    <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
      <!-- Edad -->
      <div>
        <label class="label">Edad del conductor principal</label>
        <input
          type="number" min="18" max="99"
          :value="c.edad_conductor ?? ''"
          @input="c.edad_conductor = Number(($event.target as HTMLInputElement).value) || null"
          placeholder="Ej: 35"
          class="input"
        />
      </div>

      <!-- Zona -->
      <div>
        <label class="label">Zona de circulación habitual</label>
        <select :value="c.zona" @change="c.zona = ($event.target as HTMLSelectElement).value" class="select">
          <option value="">— Seleccioná zona —</option>
          <option v-for="z in opciones.zonas" :key="z.codigo" :value="z.codigo">{{ z.label }}</option>
        </select>
      </div>

      <!-- Uso -->
      <div>
        <label class="label">Uso del vehículo</label>
        <select :value="c.uso" @change="c.uso = ($event.target as HTMLSelectElement).value" class="select">
          <option value="">— Seleccioná uso —</option>
          <option v-for="u in opciones.usos" :key="u.codigo" :value="u.codigo">{{ u.label }}</option>
        </select>
      </div>
    </div>

    <!-- Siniestralidad -->
    <div
      class="flex items-center gap-4 p-4 rounded-xl border cursor-pointer transition-all"
      :class="c.tiene_siniestros
        ? 'border-amber-500/40 bg-amber-500/5'
        : 'border-slate-border bg-navy-700/40 hover:border-slate-border/80'"
      @click="c.tiene_siniestros = !c.tiene_siniestros"
    >
      <div
        class="w-5 h-5 rounded flex items-center justify-center border-2 flex-shrink-0 transition-colors"
        :class="c.tiene_siniestros ? 'bg-amber-500 border-amber-500' : 'border-slate-border'"
      >
        <svg v-if="c.tiene_siniestros" class="w-3 h-3 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M5 13l4 4L19 7"/>
        </svg>
      </div>
      <div>
        <p class="text-sm font-medium text-white">Registré siniestros en los últimos 2 años</p>
        <p class="text-xs text-slate-muted mt-0.5">Aplica un recargo del 15% sobre la prima</p>
      </div>
    </div>

    <div class="pt-2 flex flex-col sm:flex-row sm:justify-between gap-2">
      <button @click="wizard.goTo(1)" class="btn-ghost w-full sm:w-auto">← Anterior</button>
      <button @click="wizard.goTo(3)" :disabled="!wizard.isStep2Valid" class="btn-primary w-full sm:w-auto">
        Siguiente →
      </button>
    </div>
  </div>
</template>
