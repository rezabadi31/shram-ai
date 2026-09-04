/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        shram: {
          navy: '#0f172a',
          slate: '#1e293b',
          border: '#334155',
          gold: '#d97706',
          emerald: '#059669',
          crimson: '#dc2626',
          ashoka: '#1e3a8a',
        },
      },
    },
  },
  plugins: [],
}
