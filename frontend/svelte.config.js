import adapter from '@sveltejs/adapter-auto';
import { vitePreprocess } from '@sveltejs/vite-plugin-svelte';
// import { preprocess } from 'svelte/compiler';
import { sveltePreprocess } from 'svelte-preprocess';

import { mdsvex } from 'mdsvex'
import mdsvexConfig from './mdsvex.config.js'; // 👈import our mdsvex config
import { preprocess } from 'svelte/compiler';

/** @type {import('mdsvex').MdsvexOptions} */
const mdsvexOptions = {
	extensions: ['.md'],
}

/** @type {import('@sveltejs/kit').Config} */
const config = {
	
	extensions: ['.svelte', '.md', '.svx'],
	preprocess: [
		vitePreprocess(),
		mdsvex(mdsvexConfig)
	],
	
	kit: {
		adapter: adapter(),
		alias: {
			$root: 'src'
		}
	},
	vitePlugin: {
		experimental: {
		}
	},
	// plugins: {
	// 	extensions: ['.svelte', '.md', '.svx'],
	// 	preprocess: mdsvex()
	// }
};

export default config;