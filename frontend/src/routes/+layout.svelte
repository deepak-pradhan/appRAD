<script>
	let now = new Date();
	import 'bulma/css/bulma.min.css';
	import Nav from '$lib/Nav.svelte';
	import Footer from '$lib/Footer.svelte';
</script>

<svelte:head>
	<link rel="icon" href="https://fav.farm/🎯" />
	<title>Demo</title>
    <script defer src="https://use.fontawesome.com/releases/v5.15.4/js/all.js"></script>
</svelte:head>

<Nav />
<slot />
<Footer />