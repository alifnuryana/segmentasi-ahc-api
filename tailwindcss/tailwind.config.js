/** @type {import('tailwindcss').Config} */
module.exports = {
    content: ["../templates/**/*.html", 'node_modules/preline/dist/*.js',],
    theme: {
        extend: {},
    },
    plugins: [
        require('@tailwindcss/forms'),
        require('preline/plugin')
    ],
}

