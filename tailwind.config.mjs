/** @type {import('tailwindcss').Config} */
export default {
  content: ['./src/**/*.{astro,html,js,jsx,md,mdx,svelte,ts,tsx,vue}'],
  theme: {
    extend: {
      colors: {
        ferrari: {
          red: '#DC143C',
          yellow: '#FFD700',
          black: '#000000',
          gray: '#1a1a1a',
          'gray-light': '#2a2a2a',
          'gray-dark': '#0a0a0a'
        }
      },
      fontFamily: {
        'sans': ['Inter', 'system-ui', 'sans-serif'],
        'display': ['Montserrat', 'system-ui', 'sans-serif']
      }
    },
  },
  plugins: [],
}