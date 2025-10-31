/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './templates/**/*.html',
    './**/templates/**/*.html',
    './static/src/**/*.js',
  ],
  theme: {
    extend: {
      fontFamily: {
        sans: ['var(--font-sans)', 'sans-serif'],
      },
      colors: {
        white: 'var(--color-white)',
        black: 'var(--color-black)',

        blue: {
          50: 'var(--color-blue-50)',
          100: 'var(--color-blue-100)',
          200: 'var(--color-blue-200)',
          300: 'var(--color-blue-300)',
          400: 'var(--color-blue-400)',
          500: 'var(--color-blue-500)',
          600: 'var(--color-blue-600)',
          700: 'var(--color-blue-700)',
          800: 'var(--color-blue-800)',
          900: 'var(--color-blue-900)',
        },
        darkBlue: {
          50: 'var(--color-darkBlue-50)',
          100: 'var(--color-darkBlue-100)',
          200: 'var(--color-darkBlue-200)',
          300: 'var(--color-darkBlue-300)',
          400: 'var(--color-darkBlue-400)',
          500: 'var(--color-darkBlue-500)',
          600: 'var(--color-darkBlue-600)',
          700: 'var(--color-darkBlue-700)',
          800: 'var(--color-darkBlue-800)',
          900: 'var(--color-darkBlue-900)',
        },
      },
      fontSize: {
        'heading-h1': 'var(--text--heading-h1)',
        'heading-h2': 'var(--text--heading-h2)',
        'heading-h3': 'var(--text--heading-h3)',
        'heading-h4': 'var(--text-heading-h4)',
        'heading-h5': 'var(--text--heading-h5)',
        'paragraph-lg': 'var(--text-paragraph-lg)',
        'paragraph-lg-md': 'var(--text-paragraph-lg-md)',
        'paragraph-md': 'var(--text-paragraph-md)',
        'paragraph-sm': 'var(--text-paragraph-sm)',
      },
    },
  },
  plugins: [],
}
