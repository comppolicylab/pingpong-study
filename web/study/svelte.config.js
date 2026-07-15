import adapter from '@sveltejs/adapter-static';
import { vitePreprocess } from '@sveltejs/vite-plugin-svelte';

const landingOnly = process.env.LANDING_ONLY === 'true';

/** @type {import('@sveltejs/kit').Config} */
const config = {
	// Consult https://svelte.dev/docs/kit/integrations
	// for more information about preprocessors
	preprocess: vitePreprocess(),
	kit: {
		files: {
			routes: landingOnly ? 'src/landing-routes' : 'src/routes'
		},
		adapter: adapter({
			fallback: 'index.html'
		})
	}
};

export default config;
