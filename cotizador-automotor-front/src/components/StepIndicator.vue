<script setup lang="ts">
const props = defineProps<{ current: number; total: number }>()

const steps = [
  { n: 1, label: 'Vehículo' },
  { n: 2, label: 'Conductor' },
  { n: 3, label: 'Cobertura' },
  { n: 4, label: 'Confirmación' },
]
</script>

<template>
  <div class="flex items-center justify-center gap-2 md:gap-4">
    <template v-for="(s, i) in steps" :key="s.n">
      <div class="flex flex-col items-center gap-1">
        <div
          class="step-indicator w-8 h-8 md:w-10 md:h-10 text-sm md:text-base"
          :class="{
            'bg-accent border-accent text-white': current === s.n,
            'bg-teal-brand/20 border-teal-brand text-teal-brand': current > s.n,
            'bg-navy-700 border-slate-border text-slate-muted': current < s.n,
          }"
        >
          <svg v-if="current > s.n" class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M5 13l4 4L19 7"/>
          </svg>
          <span v-else>{{ s.n }}</span>
        </div>
        <span
          class="text-xs font-medium hidden md:block"
          :class="current >= s.n ? 'text-white' : 'text-slate-muted'"
        >{{ s.label }}</span>
      </div>

      <div
        v-if="i < steps.length - 1"
        class="h-px w-10 md:w-24 mx-1 mb-5 transition-colors duration-300"
        :class="current > s.n ? 'bg-teal-brand/50' : 'bg-slate-border'"
      ></div>
    </template>
  </div>
</template>
