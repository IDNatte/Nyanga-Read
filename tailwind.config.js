/** @type {import('tailwindcss').Config} */
export default {
	content: ['./src/**/*.{html,js,svelte,ts}'],
	theme: {
		extend: {
			fontFamily: {
				sans: ['Quicksand', 'system-ui', 'sans-serif'],
				jpfont: ['Tsukimi']
			}
		}
	},
	plugins: [require('@tailwindcss/typography')]
};
