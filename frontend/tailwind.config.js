/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,jsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: '#3b82f6',
        secondary: '#0f172a',
      },
      backdropBlur: {
        xs: '2px',
      },
    },
  },
  plugins: [],
}
