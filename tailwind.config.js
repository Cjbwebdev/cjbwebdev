/** @type {import('tailwindcss').Config} */
module.exports = {
    darkMode: 'class',
    content: [
        './templates/**/*.html',
        './static/js/**/*.js',
    ],
    theme: {
        extend: {
            colors: {
                dark: {
                    50: '#1a1a2e',
                    100: '#16162a',
                    200: '#121226',
                    300: '#0e0e22',
                    400: '#0a0a1e',
                    500: '#0a0a0f',
                    600: '#08080d',
                    700: '#06060b',
                    800: '#040409',
                    900: '#020207',
                },
                accent: {
                    50: '#ecfeff',
                    100: '#cffafe',
                    200: '#a5f3fc',
                    300: '#67e8f9',
                    400: '#22d3ee',
                    500: '#06b6d4',
                    600: '#0891b2',
                    700: '#0e7490',
                    800: '#155e75',
                    900: '#164e63',
                },
                brand: {
                    50: '#fffbeb',
                    100: '#fef3c7',
                    200: '#fde68a',
                    300: '#fcd34d',
                    400: '#fbbf24',
                    500: '#f59e0b',
                    600: '#d97706',
                    700: '#b45309',
                    800: '#92400e',
                    900: '#78350f',
                },
            },
            fontFamily: {
                sans: ['Inter', 'system-ui', '-apple-system', 'sans-serif'],
                mono: ['JetBrains Mono', 'Fira Code', 'monospace'],
                display: ['Space Grotesk', 'Inter', 'sans-serif'],
            },
            animation: {
                'fade-up': 'fadeUp 0.6s ease-out',
                'fade-in': 'fadeIn 0.4s ease-out',
                'slide-right': 'slideRight 0.5s ease-out',
                'glow': 'glow 2s ease-in-out infinite alternate',
                'grid': 'grid 20s linear infinite',
            },
            keyframes: {
                fadeUp: {
                    '0%': { opacity: '0', transform: 'translateY(20px)' },
                    '100%': { opacity: '1', transform: 'translateY(0)' },
                },
                fadeIn: {
                    '0%': { opacity: '0' },
                    '100%': { opacity: '1' },
                },
                slideRight: {
                    '0%': { opacity: '0', transform: 'translateX(-20px)' },
                    '100%': { opacity: '1', transform: 'translateX(0)' },
                },
                glow: {
                    '0%': { boxShadow: '0 0 5px rgba(6,182,212,0.2)' },
                    '100%': { boxShadow: '0 0 20px rgba(6,182,212,0.4)' },
                },
                grid: {
                    '0%': { transform: 'translateY(0)' },
                    '100%': { transform: 'translateY(-50%)' },
                },
            },
        },
    },
    plugins: [],
};
