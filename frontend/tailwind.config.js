/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{vue,js,ts,jsx,tsx}'],
  theme: {
    extend: {
      fontFamily: {
        sans: ['Poppins', 'sans-serif']
      },

      gridTemplateColumns: {
        '70/30': '70% 28%'
      },
      colors: {
        "my-blue-1": '#e9fffa',
        "my-blue-2": '#ffe9f9',
        "my-blue-3": '#ffefe9',
      },
    },
  },
  variants: {
    extend: {

    },
  },
  plugins: [],
}

