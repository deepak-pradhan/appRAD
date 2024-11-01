<script lang="ts">
	import { i18n } from '$lib/i18n';
	import { ParaglideJS } from '@inlang/paraglide-sveltekit';
	import '../app.css'
	// let { children } = $props();
	import Navigation from '$lib/components/shared/Navigation/Navigation.svelte';
</script>

<!-- <ParaglideJS {i18n}>
	{@render children()}
</ParaglideJS> -->
<Navigation />
<slot />
