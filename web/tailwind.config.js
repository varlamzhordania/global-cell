module.exports = {
    content: [
        './templates/**/*.html',
        './node_modules/flowbite/**/*.js',
        './**/forms.py',
    ],
    darkMode: "class",
    theme: {
        extend: {
            container: {
                center: true,
                padding: {
                    DEFAULT: '1rem',
                    sm: '2rem',
                    lg: '4rem',
                    xl: '5rem',
                    '2xl': '6rem',
                },
            },
            colors: {
                primary: {
                    DEFAULT: '#6366f1',
                    50: '#eef2ff',
                    100: '#e0e7ff',
                    200: '#c7d2fe',
                    300: '#a5b4fc',
                    400: '#818cf8',
                    500: '#6366f1',
                    600: '#4f46e5',
                    700: '#4338ca',
                    800: '#3730a3',
                    900: '#312e81',
                    950: '#1e1b4b',
                },
                secondary: {
                    DEFAULT: '#ff7e67',
                    50: '#fff2f1',
                    100: '#ffe9e7',
                    200: '#ffbfb6',
                    300: '#ff8f82',
                    400: '#ff725b',
                    500: '#ff7e67',
                    600: '#ff6f5f',
                    700: '#f95e4d',
                    800: '#d9482e',
                    900: '#a53e2b',
                },
                success: {
                    DEFAULT: '#057A55',
                    50: '#E0F2ED',  // Very light green
                    100: '#B3DEC9', // Light green
                    200: '#80C7A5', // Light-medium green
                    300: '#4DA081', // Medium green
                    400: '#1A7A5D', // Dark-medium green
                    500: '#057A55', // Main green (green-600)
                    600: '#046648', // Slightly darker green
                    700: '#03543C', // Dark green
                    800: '#024331', // Darker green
                    900: '#013226', // Very dark green
                    950: '#001814', // Almost black green
                },
                danger: {
                    DEFAULT: '#E02424', // red-600
                    50: '#FFE5E5',  // Very light red
                    100: '#FFB8B8', // Light red
                    200: '#FF8A8A', // Light-medium red
                    300: '#FF5C5C', // Medium red
                    400: '#FF2E2E', // Dark-medium red
                    500: '#E02424', // Main red (red-600)
                    600: '#B81D1D', // Slightly darker red
                    700: '#901616', // Dark red
                    800: '#680F0F', // Darker red
                    900: '#400808', // Very dark red
                    950: '#200404', // Almost black red
                },
                warning: {
                    DEFAULT: '#ffc107',
                    50: '#fff9e6',
                    100: '#ffefcc',
                    200: '#ffe099',
                    300: '#ffd066',
                    400: '#ffc133',
                    500: '#ffc107', // Main warning color
                    600: '#d4a000',
                    700: '#aa8000',
                    800: '#806000',
                    900: '#554000',
                    950: '#2a2000',
                },
                info: {
                    DEFAULT: '#2F82FF', // info-600
                    50: '#E5F0FF',  // Very light blue
                    100: '#B8D4FF', // Light blue
                    200: '#8AB9FF', // Light-medium blue
                    300: '#5D9EFF', // Medium blue
                    400: '#2F82FF', // Dark-medium blue
                    500: '#1C64F2', // Main blue (info-600)
                    600: '#1958C4', // Slightly darker blue
                    700: '#144494', // Dark blue
                    800: '#0F3164', // Darker blue
                    900: '#0A1F3A', // Very dark blue
                    950: '#050F1D', // Almost black blue
                },
            },
        },
        fontFamily: {
            'sans': ['Poppins', "ui-sans-serif", "system-ui", "sans-serif", "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol", "Noto Color Emoji"],
            'serif': ['Poppins', "ui-serif", "Georgia", "Cambria", "Times New Roman", "Times", "serif"],
            'mono': ['Poppins', "ui-monospace", "SFMono-Regular", "Menlo", "Monaco", "Consolas", "Liberation Mono", "Courier New", "monospace"],
        }
    },
    plugins:
        [
            require('flowbite/plugin')({charts: true,}),
            require('@tailwindcss/typography'),
            require('tailwind-scrollbar')({nocompatible: true}),
        ],
}