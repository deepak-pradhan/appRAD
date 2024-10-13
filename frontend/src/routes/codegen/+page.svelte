<script lang="ts">
	import { marked } from 'marked';
	import { Row, Column, Content, Grid, Select, SelectItem, Slider, TextInput, Button, ProgressBar, InlineNotification, TextArea } from 'carbon-components-svelte'

	let codePrompt = ''
	let generatedCode = ''
	let isLoading = false
	let language = 'python'
	let selectedModel = 'llama3.1:8b'
	let temperature = 0.7
	let maxTokens = 500
	let errorMessage = ''
	let referenceModels = '';

	const languages = ['python', 'javascript', 'java', 'c++', 'rust']
	const availableModels = ['llama3.1:8b', 'granite-code:8b', 'granite-code:20b', 'codegemma:7b-instruct-fp16', 'codellama:7b', 'codellama:13b']

	async function generateCode() {
		if (!codePrompt.trim()) return

		isLoading = true
		errorMessage = ''

		try {
			const response = await fetch('http://localhost:8081/generate_code', {
				method: 'POST',
				headers: { 'Content-Type': 'application/json' },
				body: JSON.stringify({
					prompt: codePrompt,
					language: language,
					model: selectedModel,
					temperature: temperature,
					max_tokens: maxTokens,
					reference_models: referenceModels
				})
			})

			if (!response.ok) {
				throw new Error('Network response was not ok')
			}

			const data = await response.json()
			generatedCode = data.code
		} catch (error) {
			console.error('Error:', error)
			errorMessage = 'An error occurred while generating code. Please try again.'
		} finally {
			isLoading = false
		}
	}

	function formatCode(code: string) {
		return marked(code)
	}
</script>

<Content>
	<Grid>
		<h1>AI Code Generator: calls FastAPI</h1>
		<Row>
			<Column lg={8}>
				<Select labelText="Select Language" bind:selected={language}>
					{#each languages as lang}
						<SelectItem value={lang} text={lang} />
					{/each}
				</Select>
			</Column>
			<Column lg={8}>
				<Select labelText="Select Model" bind:selected={selectedModel}>
					{#each availableModels as model}
						<SelectItem value={model} text={model} />
					{/each}
				</Select>
			</Column>
		</Row>
		<Row>
			<Column lg={8}>
				<Slider 
					labelText={`Temperature: ${temperature.toFixed(2)}`}
					min={0}
					max={1}
					step={0.01}
					bind:value={temperature}
				/>
			</Column>
			<Column lg={8}>
				<Slider 
					labelText={`Max Tokens: ${maxTokens}`}
					min={1}
					max={1000}
					step={1}
					bind:value={maxTokens}
				/>
			</Column>
		</Row>
		<Row>
			<Column>
				<TextArea
					labelText="Reference Models (optional)"
					placeholder="Paste relevant model code here (e.g., Base and Vendor models)"
					bind:value={referenceModels}
					rows={5}
				/>
			</Column>
		</Row>
		<Row>
			<Column>
				{#if errorMessage}
					<InlineNotification
						kind="error"
						title="Error"
						subtitle={errorMessage}
						hideCloseButton
					/>
				{/if}
				<TextInput
					labelText="Describe the code you want to generate"
					placeholder="E.g., Using SQLModel generate a model class file for Person. Use the Base and Vendor models as examples. Attributes are: name, age, and email. Ensure it follows the structure and conventions."
					bind:value={codePrompt}
				/>
				<Button on:click={generateCode} disabled={isLoading}>
					{isLoading ? 'Generating...' : 'Generate Code'}
				</Button>
				{#if isLoading}
					<ProgressBar />
				{/if}
				{#if generatedCode}
					<div class="generated-code">
						<h2>Generated Code</h2>
						{@html formatCode(generatedCode)}
					</div>
				{/if}
			</Column>
		</Row>
	</Grid>
</Content>
<style>
	.generated-code {
		margin-top: 20px;
		padding: 15px;
		background-color: #f4f4f4;
		border-radius: 5px;
	}

	:global(.generated-code pre) {
		white-space: pre-wrap;
		word-wrap: break-word;
	}
</style>
