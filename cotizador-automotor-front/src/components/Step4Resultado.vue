<script setup lang="ts">
import { ref, computed } from 'vue'
import { useWizardStore } from '../stores/wizard'
import { cotizadorApi } from '../api/cotizador'

const wizard = useWizardStore()
const r = computed(() => wizard.state.resultado!)
const guardando = ref(false)
const guardado = ref(false)
const errorGuardar = ref<string | null>(null)

const fmt = (n: number) => `$${n.toLocaleString('es-AR', { maximumFractionDigits: 0 })}`
const pct = (n: number) => `${n.toFixed(1)}%`

const factorItems = computed(() => [
  { label: 'Tasa base cobertura', value: pct(r.value.desglose.tasa_base_pct) },
  { label: 'Factor marca', value: r.value.desglose.factor_marca.toFixed(3) },
  { label: 'Factor zona', value: r.value.desglose.factor_zona.toFixed(3) },
  { label: 'Factor uso', value: r.value.desglose.factor_uso.toFixed(3) },
  { label: 'Factor antigüedad', value: r.value.desglose.factor_antiguedad.toFixed(3) },
  { label: 'Factor edad conductor', value: r.value.desglose.factor_edad.toFixed(3) },
  { label: 'Factor siniestralidad', value: r.value.desglose.factor_siniestralidad.toFixed(3) },
  { label: 'Factor total aplicado', value: r.value.desglose.factor_total.toFixed(4), bold: true },
])

async function guardar() {
  if (!wizard.isStep4Valid) return
  guardando.value = true
  errorGuardar.value = null
  try {
    const data = await cotizadorApi.guardar({
      marca_id: wizard.state.vehiculo.marca_id,
      modelo_id: wizard.state.vehiculo.modelo_id,
      anio: wizard.state.vehiculo.anio,
      cobertura: wizard.state.cobertura,
      zona: wizard.state.conductor.zona,
      uso: wizard.state.conductor.uso,
      edad_conductor: wizard.state.conductor.edad_conductor,
      tiene_siniestros: wizard.state.conductor.tiene_siniestros,
      nombre_conductor: wizard.state.contacto.nombre_conductor,
      email: wizard.state.contacto.email,
      dni: wizard.state.contacto.dni,
      valor_venal: r.value.valor_venal,
      prima_mensual: r.value.prima_mensual,
      prima_anual: r.value.prima_anual,
      factor_total: r.value.factor_total,
      desglose: r.value.desglose,
    })
    wizard.setNumeroCotizacion(data.numero)
    guardado.value = true
  } catch {
    errorGuardar.value = 'No se pudo guardar la cotización. Intentá nuevamente.'
  } finally {
    guardando.value = false
  }
}
</script>

<template>
  <div class="space-y-6">
    <div>
      <p class="section-label mb-1">Paso 4</p>
      <h2 class="text-xl font-semibold text-white">Tu cotización</h2>
    </div>

    <!-- Resultado principal -->
    <div class="bg-gradient-to-br from-accent/20 to-teal-brand/10 border border-accent/30 rounded-2xl p-6">
      <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <p class="text-sm text-slate-muted">{{ r.marca }} {{ r.modelo }} {{ r.anio }}</p>
          <p class="text-lg font-semibold text-white mt-0.5">{{ r.cobertura_label }}</p>
          <p class="text-xs text-slate-muted mt-1">Valor venal: {{ fmt(r.valor_venal) }}</p>
        </div>
        <div class="text-right">
          <p class="text-4xl font-bold text-white">{{ fmt(r.prima_mensual) }}</p>
          <p class="text-sm text-slate-muted">por mes</p>
          <p class="text-xs text-teal-brand mt-1">{{ fmt(r.prima_anual) }} / año</p>
        </div>
      </div>

      <div v-if="r.franquicia_pct > 0" class="mt-4 pt-4 border-t border-white/10">
        <p class="text-xs text-slate-muted">
          Franquicia: <span class="text-amber-300">{{ r.franquicia_pct }}%</span> del valor venal
          (≈ {{ fmt(r.valor_venal * r.franquicia_pct / 100) }})
        </p>
      </div>
    </div>

    <!-- Coberturas incluidas + desglose -->
    <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
      <div class="card">
        <p class="text-xs font-semibold text-slate-muted uppercase tracking-wide mb-3">Incluye</p>
        <ul class="space-y-1.5">
          <li v-for="item in r.incluye" :key="item" class="flex items-center gap-2 text-sm text-slate-text">
            <svg class="w-3.5 h-3.5 text-teal-brand flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M5 13l4 4L19 7"/>
            </svg>
            {{ item }}
          </li>
        </ul>
      </div>

      <div class="card">
        <p class="text-xs font-semibold text-slate-muted uppercase tracking-wide mb-3">Desglose de factores</p>
        <div class="space-y-1.5">
          <div v-for="f in factorItems" :key="f.label"
            class="flex justify-between text-xs"
            :class="f.bold ? 'pt-1.5 border-t border-slate-border mt-1' : ''"
          >
            <span :class="f.bold ? 'text-white font-semibold' : 'text-slate-muted'">{{ f.label }}</span>
            <span :class="f.bold ? 'text-accent font-bold font-mono' : 'text-slate-text font-mono'">{{ f.value }}</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Datos de contacto para guardar -->
    <div v-if="!guardado" class="card space-y-4">
      <p class="text-sm font-semibold text-white">Guardá tu cotización</p>
      <div class="grid sm:grid-cols-2 gap-3">
        <div>
          <label class="label">Nombre y apellido *</label>
          <input v-model="wizard.state.contacto.nombre_conductor" type="text" placeholder="Juan García" class="input" />
        </div>
        <div>
          <label class="label">Email *</label>
          <input v-model="wizard.state.contacto.email" type="email" placeholder="juan@email.com" class="input" />
        </div>
        <div>
          <label class="label">DNI (opcional)</label>
          <input v-model="wizard.state.contacto.dni" type="text" placeholder="12345678" class="input" />
        </div>
      </div>
      <p v-if="errorGuardar" class="text-xs text-red-400">{{ errorGuardar }}</p>
      <div class="flex flex-col sm:flex-row sm:justify-between items-center pt-2 gap-2">
        <button @click="wizard.goTo(3)" class="btn-ghost w-full sm:w-auto">← Cambiar cobertura</button>
        <button @click="guardar" :disabled="!wizard.isStep4Valid || guardando" class="btn-primary w-full sm:w-auto">
          <svg v-if="guardando" class="w-4 h-4 animate-spin" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"/>
          </svg>
          {{ guardando ? 'Guardando...' : 'Guardar cotización' }}
        </button>
      </div>
    </div>

    <!-- Confirmación guardado -->
    <div v-else class="card text-center py-8">
      <div class="w-14 h-14 rounded-full bg-teal-brand/20 flex items-center justify-center mx-auto mb-4">
        <svg class="w-7 h-7 text-teal-brand" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
        </svg>
      </div>
      <p class="text-white font-semibold text-lg mb-1">¡Cotización guardada!</p>
      <p class="font-mono text-accent text-sm mb-4">{{ wizard.state.numeroCotizacion }}</p>
      <p class="text-slate-muted text-sm mb-6">Un asesor se va a contactar con vos en las próximas 24 hs.</p>
      <button @click="wizard.reset()" class="btn-ghost">Nueva cotización</button>
    </div>
  </div>
</template>
