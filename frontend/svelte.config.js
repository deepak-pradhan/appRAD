import { vitePreprocess } from '@sveltejs/vite-plugin-svelte';
// import { preprocess } from 'svelte/compiler';
import { sveltePreprocess } from 'svelte-preprocess';

import adapter from '@sveltejs/adapter-auto';
import { mdsvex } from 'mdsvex'
import mdsvexConfig from './mdsvex.config.js'; // 👈import our mdsvex config


/** @type {import('@sveltejs/kit').Config} */
const config = {
	
	preprocess: [
		vitePreprocess(),
		// sveltePreprocess(),
		mdsvex(mdsvexConfig)
	],
	extensions: ['.svelte', '.md', '.svx'],
	//extensions: ['.svelte', ...mdsvexConfig.extensions],
	
	kit: {
		adapter: adapter(),
		alias: {
			$root: 'src'
		}
	},
	vitePlugin: {
		experimental: {
		}
	}
};

export default config;