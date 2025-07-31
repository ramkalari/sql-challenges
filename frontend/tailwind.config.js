/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './src/pages/**/*.{js,ts,jsx,tsx,mdx}',
    './src/components/**/*.{js,ts,jsx,tsx,mdx}',
    './src/app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        background: 'var(--background)',
        foreground: 'var(--foreground)',
      },
    },
  },
  plugins: [],
  // Ensure all text colors are preserved
  safelist: [
    'text-gray-900',
    'text-gray-700',
    'text-gray-600',
    'text-gray-500',
    'text-gray-400',
    'text-blue-600',
    'text-green-600',
    'text-red-600',
    'text-yellow-600',
    'text-purple-600',
    'text-white',
    'text-black',
  ]
} 