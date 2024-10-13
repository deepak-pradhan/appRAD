<script lang="ts">
    import { marked } from 'marked';
    import { Content, Grid, Row, Column, Select, SelectItem, Slider, TextInput, Button, ProgressBar, InlineNotification } from "carbon-components-svelte";
    import { writable } from 'svelte/store';
    
    interface ChatMessage {
        role: 'user' | 'assistant';
        content: string;
    }

    let chatHistory = writable<ChatMessage[]>([]);
    let userInput = writable('');
    let isLoading = writable(false);
    let selectedModel = writable('llama3.1:8b');
    let temperature = writable(0.7);
    let maxTokens = writable(100);
    let errorMessage = writable('');

    const availableModels = ['llama3.1:8b', 'granite-code:8b', 'granite-code:20b', 'codegemma:7b-instruct-fp16', 'codellama:7b', 'codellama:13b'];

    async function sendMessage() {
        if (!$userInput.trim()) return;

        $isLoading = true;
        $errorMessage = '';
        $chatHistory = [...$chatHistory, { role: 'user', content: $userInput }];

        const conversationHistory = $chatHistory.map(msg => `${msg.role}: ${msg.content}`);

        try {
            const response = await fetch('http://localhost:8081/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ 
                    model: $selectedModel, 
                    prompt: $userInput,
                    temperature: $temperature,
                    max_tokens: $maxTokens,
                    conversation_history: conversationHistory
                })
            });
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            const data = await response.json();
            $chatHistory = [...$chatHistory, { role: 'assistant', content: data.response }];
        } catch (error) {
            console.error('Error:', error);
            $errorMessage = 'An error occurred while fetching the response. Please try again.';
        } finally {
            $isLoading = false;
            $userInput = '';
        }
    }

    function formatMessage(content: string) {
        return marked(content);
    }
</script>

<Content>
    <Grid>
        <Row>
            <Column>
                <h1>Chat with AI: calls FastAPI's API</h1>
            </Column>
        </Row>

        <Row>
            <Column lg={16}>
                <Select labelText="Select Model" bind:selected={$selectedModel}>
                    {#each availableModels as model}
                        <SelectItem value={model} text={model} />
                    {/each}
                </Select>
            </Column>
        </Row>

        <Row>
            <Column lg={8}>
                <Slider 
                    labelText={`Temperature: ${$temperature.toFixed(2)}`}
                    min={0}
                    max={1}
                    step={0.01}
                    bind:value={$temperature}
                />
            </Column>
            <Column lg={8}>
                <Slider 
                    labelText={`Max Tokens: ${$maxTokens}`}
                    min={1}
                    max={500}
                    step={1}
                    bind:value={$maxTokens}
                />
            </Column>
        </Row>

        <Row>
            <Column>
                {#if $errorMessage}
                    <InlineNotification
                        kind="error"
                        title="Error"
                        subtitle={$errorMessage}
                        hideCloseButton
                    />
                {/if}
                <div class="chat-container">
                    <div class="chat-history">
                        {#each $chatHistory as message}
                            <div class={`chat-bubble ${message.role === 'user' ? 'user-bubble' : 'ai-bubble'}`}>
                                {#if message.role === 'user'}
                                    <p>{message.content}</p>
                                {:else}
                                    {@html formatMessage(message.content)}
                                {/if}
                            </div>
                        {/each}
                    </div>

                    {#if $isLoading}
                        <ProgressBar />
                    {/if}
                </div>
            </Column>
        </Row>

        <Row>
            <Column>
                <form on:submit|preventDefault={sendMessage}>
                    <TextInput
                        labelText="Type your message"
                        placeholder="Type your message..."
                        bind:value={$userInput}
                    />
                    <Button type="submit" disabled={$isLoading}>
                        {$isLoading ? 'Sending...' : 'Send'}
                    </Button>
                </form>
            </Column>
        </Row>
    </Grid>
</Content>

<style>
    :global(.chat-container) {
        height: 400px;
        display: flex;
        flex-direction: column;
    }

    .chat-history {
        flex-grow: 1;
        overflow-y: auto;
        padding: 10px;
        display: flex;
        flex-direction: column;
        gap: 10px;
    }

    .chat-bubble {
        max-width: 70%;
        padding: 10px 15px;
        border-radius: 20px;
        margin-bottom: 10px;
    }

    .user-bubble {
        align-self: flex-end;
        background-color: #0f62fe;
        color: white;
    }

    .ai-bubble {
        align-self: flex-start;
        background-color: #f4f4f4;
        color: #161616;
    }
</style>