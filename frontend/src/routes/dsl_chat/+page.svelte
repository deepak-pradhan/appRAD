<script lang="ts">
    import { onMount } from 'svelte';

    let codePrompt = '';
    let generatedCode = '';
    let isLoading = false;
    let language = 'python';

    const languages = ['python', 'javascript', 'java', 'c++', 'rust'];

    async function generateCode() {
        if (!codePrompt.trim()) return;

        isLoading = true;

        try {
            const response = await fetch('http://localhost:8081/generate-code', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ 
                    prompt: codePrompt,
                    language: language,
                    model: 'llama3.1:8b',
                    temperature: 0.7,
                    max_tokens: 500
                })
            });

            const data = await response.json();
            generatedCode = data.code;
        } catch (error) {
            console.error('Error:', error);
        } finally {
            isLoading = false;
        }
    }
</script>

<section class="section">
    <div class="container">
        <h1 class="title">AI Code Generator</h1>
        <div class="box">
            <div class="field">
                <label class="label" for="language-select">Select Language</label>
                <div class="control">
                    <div class="select">
                        <select id="language-select" bind:value={language}>
                            {#each languages as lang}
                                <option value={lang}>{lang}</option>
                            {/each}
                        </select>
                    </div>
                </div>
            </div>
            <div class="field">
                <label class="label" for="code-prompt">Describe the code you want to generate</label>
                <div class="control">
                    <textarea id="code-prompt" class="textarea" bind:value={codePrompt} placeholder="E.g., Write a function to calculate the fibonacci sequence"></textarea>
                </div>
            </div>
            <div class="field">
                <div class="control">
                    <button class="button is-primary" on:click={generateCode} disabled={isLoading}>
                        {isLoading ? 'Generating...' : 'Generate Code'}
                    </button>
                </div>
            </div>
            {#if generatedCode}
                <div class="field">
                    <label class="label" for="generated-code">Generated Code</label>
                    <pre><code id="generated-code">{generatedCode}</code></pre>
                </div>
            {/if}
        </div>
    </div> 
</section>

<style>
    pre {
        background-color: #f5f5f5;
        padding: 1em;
        border-radius: 4px;
    }
</style>