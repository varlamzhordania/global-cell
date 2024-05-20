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
                }
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