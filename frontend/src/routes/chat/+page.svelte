<script lang="ts">
    import { onMount } from 'svelte';

    let chatHistory = [];
    let userInput = '';
    let isLoading = false;
    let selectedModel = 'llama3.1:8b';
    let temperature = 0.7;
    let maxTokens = 100;

    const availableModels = ['llama3.1:8b', 'granite-code:8b', 'granite-code:20b', 'codegemma:7b-instruct-fp16', 'codellama:7b', 'codellama:13b'];

    async function sendMessage() {
        if (!userInput.trim()) return;

        isLoading = true;
        chatHistory = [...chatHistory, { role: 'user', content: userInput }];

        const conversationHistory = chatHistory.map(msg => `${msg.role}: ${msg.content}`);

        try {
            const response = await fetch('http://localhost:8081/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ 
                    model: selectedModel, 
                    prompt: userInput,
                    temperature: temperature,
                    max_tokens: maxTokens,
                    conversation_history: conversationHistory
                })
            });
            const data = await response.json();
            chatHistory = [...chatHistory, { role: 'assistant', content: data.response }];
        } catch (error) {
            console.error('Error:', error);
        } finally {
            isLoading = false;
            userInput = '';
        }
    }
</script>

<section class="section">
    <div class="container">
        <h1 class="title">Chat with AI</h1>
        <div class="box">
            <div class="columns">
                <div class="column">
                    <div class="field">
                        <label class="label" for="model-select">Select Model</label>
                        <div class="control">
                            <div class="select is-fullwidth">
                                <select id="model-select" bind:value={selectedModel}>
                                    {#each availableModels as model}
                                        <option value={model}>{model}</option>
                                    {/each}
                                </select>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="column">
                    <div class="field">
                        <label class="label" for="temperature-slider">Temperature: {temperature.toFixed(2)}</label>
                        <div class="control">
                            <input id="temperature-slider" type="range" class="slider is-fullwidth" min="0" max="1" step="0.01" bind:value={temperature}>
                        </div>
                    </div>
                </div>
                <div class="column">
                    <div class="field">
                        <label class="label" for="max-tokens-slider">Max Tokens: {maxTokens}</label>
                        <div class="control">
                            <input id="max-tokens-slider" type="range" class="slider is-fullwidth" min="1" max="500" step="1" bind:value={maxTokens}>
                        </div>
                    </div>
                </div>
            </div>            
        </div>
    </div>
</section>

<section class="section">
    <div class="container">
        <div class="box">
            <div class="content">
                {#each chatHistory as message}
                    <div class={`message ${message.role === 'user' ? 'is-primary' : 'is-info'}`}>
                        <div class="message-header">
                            <p>{message.role === 'user' ? 'You' : 'AI'}</p>
                        </div>
                        <div class="message-body">
                            {message.content}
                        </div>
                    </div>
                {/each}
                {#if isLoading}
                    <progress class="progress is-small is-primary" max="100">15%</progress>
                {/if}
            </div>
            <form on:submit|preventDefault={sendMessage} class="mt-4">
                <div class="field has-addons">
                    <div class="control is-expanded">
                        <label for="user-input" class="is-sr-only">Type your message</label>
                        <input id="user-input" class="input" type="text" bind:value={userInput} placeholder="Type your message..." />
                    </div>
                    <div class="control">
                        <button type="submit" class="button is-primary" disabled={isLoading}>
                            {isLoading ? 'Sending...' : 'Send'}
                        </button>
                    </div>
                </div>
            </form>
        </div>
    </div>
</section>