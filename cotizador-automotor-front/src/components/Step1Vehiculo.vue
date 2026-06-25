<script setup lang="ts">
import { ref, watch, computed } from 'vue'
import { useWizardStore } from '../stores/wizard'
import { cotizadorApi } from '../api/cotizador'
import type { Modelo, OpcionesForm } from '../types'

const props = defineProps<{ opciones: OpcionesForm }>()
const wizard = useWizardStore()

const modelos = ref<Modelo[]>([])
const loadingModelos = ref(false)

const marcaSeleccionada = computed({
  get: () => wizard.state.vehiculo.marca_id,
  set: (v) => {
    wizard.state.vehiculo.marca_id = v
    wizard.state.vehiculo.modelo_id = null
    modelos.value = []
  }
})

watch(marcaSeleccionada, async (id) => {
  if (!id) return
  loadingModelos.value = true
  try {
    modelos.value = await cotizadorApi.getModelos(id)
  } finally {
    loadingModelos.value = false
  }
})

const modeloSeleccionado = computed({
  get: () => wizard.state.vehiculo.modelo_id,
  set: (v) => { wizard.state.vehiculo.modelo_id = v }
})

const anioSeleccionado = computed({
  get: () => wizard.state.vehiculo.anio,
  set: (v) => { wizard.state.vehiculo.anio = v }
})

const aniosFiltrados = computed(() => {
  if (!modeloSeleccionado.value || !modelos.value.length) return props.opciones.anios
  const m = modelos.value.find(m => m.id === modeloSeleccionado.value)
  if (!m) return props.opciones.anios
  return props.opciones.anios.filter(a => a >= m.anio_desde && (m.anio_hasta == null || a <= m.anio_hasta))
})

function siguiente() {
  if (wizard.isStep1Valid) wizard.goTo(2)
}
</script>

<template>
  <div class="space-y-5">
    <div>
      <p class="section-label mb-1">Paso 1</p>
      <h2 class="text-xl font-semibold text-white">Datos del vehículo</h2>
      <p class="text-sm text-slate-muted mt-1">Seleccioná la marca, modelo y año de tu auto.</p>
    </div>

    <!-- Marca -->
    <div>
      <label class="label">Marca</label>
      <select :value="marcaSeleccionada ?? ''" @change="marcaSeleccionada = Number(($event.target as HTMLSelectElement).value) || null" class="select">
        <option value="">— Seleccioná una marca —</option>
        <option v-for="m in opciones.marcas" :key="m.id" :value="m.id">{{ m.nombre }}</option>
      </select>
    </div>

    <!-- Modelo -->
    <div>
      <label class="label">Modelo</label>
      <select
        :value="modeloSeleccionado ?? ''"
        @change="modeloSeleccionado = Number(($event.target as HTMLSelectElement).value) || null"
        class="select"
        :disabled="!marcaSeleccionada || loadingModelos"
      >
        <option value="">{{ loadingModelos ? 'Cargando modelos...' : '— Seleccioná un modelo —' }}</option>
        <option v-for="m in modelos" :key="m.id" :value="m.id">
          {{ m.nombre }} ({{ m.segmento }})
        </option>
      </select>
    </div>

    <!-- Año -->
    <div>
      <label class="label">Año</label>
      <select
        :value="anioSeleccionado ?? ''"
        @change="anioSeleccionado = Number(($event.target as HTMLSelectElement).value) || null"
        class="select"
        :disabled="!modeloSeleccionado"
      >
        <option value="">— Seleccioná el año —</option>
        <option v-for="a in aniosFiltrados" :key="a" :value="a">{{ a }}</option>
      </select>
    </div>

    <div class="pt-2 flex flex-col sm:flex-row sm:justify-end gap-2">
      <button @click="siguiente" :disabled="!wizard.isStep1Valid" class="btn-primary w-full sm:w-auto">
        Siguiente
        <svg class="w-4 h-4 ml-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 8l4 4m0 0l-4 4m4-4H3"/>
        </svg>
      </button>
    </div>
  </div>
</template>
