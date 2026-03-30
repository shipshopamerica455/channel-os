/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{ts,tsx}'],
  theme: {
    extend: {
      colors: {
        surface: {
          0: '#0A0A0A',
          1: '#111111',
          2: '#1A1A1A',
          3: '#242424',
          4: '#2E2E2E',
        },
        border: '#2A2A2A',
        muted: '#666666',
        dim: '#999999',
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
        mono: ['JetBrains Mono', 'Fira Code', 'monospace'],
      },
    },
  },
  plugins: [],
};
