
<!-- lib/components/chat/OllamaChat.svelte -->
<script lang="ts">
  export let modelName: string;
  export let theme: 'light' | 'dark' = 'dark';
  
  let messages: Array<{role: string, content: string}> = [];
  let inputMessage = '';
  
  async function sendMessage() {
    if (!inputMessage.trim()) return;
    
    messages = [...messages, { role: 'user', content: inputMessage }];
    
    const response = await fetch('http://0.0.0.0:8082/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        model: modelName,
        prompt: inputMessage
      })
    });
    
    const data = await response.json();
    messages = [...messages, { role: 'assistant', content: data.response }];
    inputMessage = '';
  }
</script>
<div class="chat-container {theme}">
  <div class="chat-header">
    <h2>Chat with {modelName}</h2>
  </div>
  
  <div class="chat-messages">
    {#each messages as message}
      <div class="message {message.role}">
        {message.content}
      </div>
    {/each}
  </div>

  <div class="chat-input">
    <input 
      bind:value={inputMessage} 
      on:keydown={(e) => e.key === 'Enter' && sendMessage()}
      placeholder="Ask anything..." 
    />
    <button on:click={sendMessage}>Send</button>
  </div>
</div>
<style>
  .chat-container {
    border-radius: 8px;
    overflow: hidden;
    max-width: 800px;
    margin: 0 auto;
  }

  .dark {
    background: #1a1a1a;
    color: #fff;
  }

  .chat-messages {
    height: 400px;
    overflow-y: auto;
    padding: 1rem;
  }

  .message {
    margin: 1rem 0;
    padding: 1rem;
    border-radius: 8px;
  }

  .user {
    background: #2a2a2a;
    margin-left: 20%;
  }

  .assistant {
    background: #3a3a3a;
    margin-right: 20%;
  }

  .chat-input {
    display: flex;
    padding: 1rem;
    gap: 0.5rem;
  }

  input {
    flex: 1;
    padding: 0.5rem;
    border-radius: 4px;
    background: #2a2a2a;
    color: white;
    border: 1px solid #3a3a3a;
  }

  button {
    padding: 0.5rem 1rem;
    border-radius: 4px;
    background: #4a4a4a;
    color: white;
    border: none;
    cursor: pointer;
  }

  button:hover {
    background: #5a5a5a;
  }
</style>
