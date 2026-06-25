<script setup lang="ts">
import { useOpciones } from '../composables/useOpciones'
import { useWizardStore } from '../stores/wizard'
import StepIndicator from '../components/StepIndicator.vue'
import Step1Vehiculo from '../components/Step1Vehiculo.vue'
import Step2Conductor from '../components/Step2Conductor.vue'
import Step3Cobertura from '../components/Step3Cobertura.vue'
import Step4Resultado from '../components/Step4Resultado.vue'

const { opciones, loading, error } = useOpciones()
const wizard = useWizardStore()
</script>

<template>
  <div class="min-h-screen bg-navy-950">
    <!-- Header -->
    <header class="border-b border-slate-border bg-navy-900/80 backdrop-blur sticky top-0 z-10">
      <div class="container h-14 flex items-center justify-between">
        <div class="flex items-center gap-2">
          <div class="w-7 h-7 rounded-lg bg-accent/20 flex items-center justify-center">
            <svg class="w-4 h-4 text-accent" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5"
                d="M9 17a2 2 0 11-4 0 2 2 0 014 0zM19 17a2 2 0 11-4 0 2 2 0 014 0z"/>
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5"
                d="M13 16V6a1 1 0 00-1-1H4a1 1 0 00-1 1v10a1 1 0 001 1h1m8-1a1 1 0 01-1 1H9m4-1V8a1 1 0 011-1h2.586a1 1 0 01.707.293l3.414 3.414a1 1 0 01.293.707V16a1 1 0 01-1 1h-1m-6-1a1 1 0 001 1h1"/>
            </svg>
          </div>
          <div>
            <p class="text-sm font-semibold text-white leading-none">Cotizador Automotor</p>
            <p class="text-[10px] text-slate-muted font-mono">InsurTech · MVP</p>
          </div>
        </div>
        <button @click="wizard.reset()" class="text-xs text-slate-muted hover:text-white transition-colors font-mono">
          Reiniciar
        </button>
      </div>
    </header>

    <main class="container py-10">
      <!-- Loading inicial -->
      <div v-if="loading" class="flex items-center justify-center h-64">
        <div class="text-center">
          <div class="w-8 h-8 border-2 border-accent border-t-transparent rounded-full animate-spin mx-auto mb-3"></div>
          <p class="text-sm text-slate-muted">Cargando cotizador...</p>
        </div>
      </div>

      <div v-else-if="error" class="text-center py-16">
        <p class="text-red-400 mb-4">{{ error }}</p>
        <p class="text-sm text-slate-muted">Verificá que el backend esté corriendo en el puerto 8000.</p>
      </div>

      <template v-else-if="opciones">
        <!-- Step indicator -->
        <div class="mb-10">
          <StepIndicator :current="wizard.state.step" :total="4" />
        </div>

        <!-- Step content -->
        <div class="card max-w-2xl mx-auto">
          <Transition name="slide" mode="out-in">
            <Step1Vehiculo v-if="wizard.state.step === 1" :opciones="opciones" key="s1" />
            <Step2Conductor v-else-if="wizard.state.step === 2" :opciones="opciones" key="s2" />
            <Step3Cobertura v-else-if="wizard.state.step === 3" :opciones="opciones" key="s3" />
            <Step4Resultado v-else-if="wizard.state.step === 4" key="s4" />
          </Transition>
        </div>

        <!-- Info footer -->
        <p class="text-center text-xs text-slate-muted mt-8 font-mono">
          Las primas son estimadas y no constituyen oferta contractual.
        </p>
      </template>
    </main>
  </div>
</template>

<style scoped>
.slide-enter-active, .slide-leave-active { transition: all 0.25s ease; }
.slide-enter-from { opacity: 0; transform: translateX(20px); }
.slide-leave-to { opacity: 0; transform: translateX(-20px); }
</style>
