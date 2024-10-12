<script lang="ts">
	import { Content, Grid, Row, Column, Tile } from 'carbon-components-svelte'
	import Hero from '$root/routes/Hero.svelte'

	export let data

	let features = [
		{ icon: 'fas fa-bolt', title: 'Fast API', description: 'High-performance backend' },
		{ icon: 'fas fa-code', title: 'Svelte Frontend', description: 'Reactive UI with SvelteKit' },
		{ icon: 'fas fa-database', title: 'Database', description: 'Seamless ORM with SQLModel' },
		{
			icon: 'fas fa-brain',
			title: 'Interface LLMs',
			description: 'AI capabilities with local LLMs & AIOS'
		}
	]
</script>

<Content>
	<Hero {data} />

	<Grid>
		<h2>In Sandbox are:</h2>
  
		<Row>
			{#each features.slice(0, 4) as feature}
				<Column>
					<Tile class="tile">
						<div class="icon"><i class={feature.icon}></i></div>
						<h3>{feature.title}</h3>
						<p>{feature.description}</p>
					</Tile>
				</Column>
			{/each}
		</Row>

	</Grid>
</Content>

<style>
	:global(.tile) {
		display: flex;
		justify-content: center;
		align-items: center;
    flex-direction: column;
		transition: transform 0.3s ease;
	}

	:global(.tile:hover) {
		transform: translateY(-5px);
	}

	.icon {
		font-size: 2rem;
	}

</style>
