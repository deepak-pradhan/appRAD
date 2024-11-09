<!-- lib/components/code-gen/CodeGenerator.svelte -->
<script lang="ts">
	export let language: string;
	export let theme: 'light' | 'dark' = 'dark';

	let prompt = '';
	let generatedCode = '';

	async function generateCode() {
		console.log('Generate button clicked!');
		const response = await fetch('http://0.0.0.0:8082/generate_code', {
			method: 'POST',
			headers: { 'Content-Type': 'application/json' },
			body: JSON.stringify({
				model: 'llama3.1:8b',
				language,
				prompt
			})
		});
		const data = await response.json();
		generatedCode = data.code;
	}
</script>

<div class="code-gen {theme}">
	<textarea bind:value={prompt} placeholder="Describe the code you want to generate..."> </textarea>
	<button on:click={generateCode}>Generate Code</button>
	<pre>{generatedCode}</pre>
</div>

<style>
	.code-gen {
		max-width: 800px;
		margin: 0 auto;
		padding: 2rem;
	}

	.dark {
		background: #1a1a1a;
		color: #fff;
	}

	textarea {
		width: 100%;
		height: 150px;
		margin-bottom: 1rem;
		padding: 1rem;
		background: #2a2a2a;
		color: white;
		border: 1px solid #3a3a3a;
		border-radius: 4px;
	}

	pre {
		background: #2a2a2a;
		padding: 1rem;
		border-radius: 4px;
		overflow-x: auto;
	}
</style>
