<script lang="ts">
	// import 'bulma/css/bulma.min.css';
	import Nav from '$lib/Nav.svelte';
	import Footer from '$lib/Footer.svelte';
	import "carbon-components-svelte/css/all.css";
</script>


<svelte:head>
	<title>Demo</title>
	<link rel="icon" href="https://fav.farm/🎯" />
    <script defer src="https://use.fontawesome.com/releases/v5.15.4/js/all.js"></script>
</svelte:head>

<div class="page-container">
	<Nav />
	<slot />
	<Footer />
</div>

<style>
	:global(body) {
		font-family: 'Roboto', sans-serif;
		margin: 0;
		padding: 0;
		box-sizing: border-box;
		overflow: hidden;
	}

	:global(.page-container) {
    max-width: 100vw;
  	}

	:global(h1) {
	  font-size: 3rem;
	  margin-bottom: 1rem;
	}
  
	:global(h2) {
	  font-size: 1.5rem;
	  margin-bottom: 2rem;
	  font-weight: 400;
	}

	:global(h3) {
		margin-top: 1rem;
		font-size: 1.2rem;
		font-weight: 600;
	}

	:global(p) {
		flex-grow: 1;
		margin: 0.5rem 0;
	}
  </style>
