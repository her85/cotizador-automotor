/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{vue,js,ts,tsx}'],
  theme: {
    extend: {
      colors: {
        navy: { 950: '#050A18', 900: '#080F22', 800: '#0D1730', 700: '#142040', 600: '#1C2D55' },
        accent: { DEFAULT: '#2D7DD2', light: '#5B9FE3', dim: '#1A4F8A' },
        teal: { brand: '#1D9E75', light: '#3DBEA0' },
        slate: { text: '#A8B4CC', muted: '#6B7A96', border: '#1E2D47' },
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
        mono: ['JetBrains Mono', 'monospace'],
      },
    },
  },
  plugins: [],
}
