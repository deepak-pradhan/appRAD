<!-- ConfigPanel.svelte -->
<script lang="ts">
  export let selectedNode: any = null;
  
  let modelParams = {
    temperature: 0.7,
    max_tokens: 1000,
    top_p: 1.0,
    frequency_penalty: 0.0,
    presence_penalty: 0.0
  };
</script>

<div class="config-panel" class:visible={selectedNode}>
  <div class="panel-content">
    <h3>Node Configuration</h3>
    
    <!-- Node Settings -->
    <div class="field">
      <label>Title</label>
      <input type="text" bind:value={selectedNode?.title} />
    </div>

    <!-- Model Parameters -->
    <div class="field">
      <label>Temperature</label>
      <input type="range" min="0" max="1" step="0.1" bind:value={modelParams.temperature} />
      <span>{modelParams.temperature}</span>
    </div>

    <div class="field">
      <label>Max Tokens</label>
      <input type="number" bind:value={modelParams.max_tokens} />
    </div>

    <div class="field">
      <label>Top P</label>
      <input type="range" min="0" max="1" step="0.1" bind:value={modelParams.top_p} />
    </div>
  </div>
</div>

<style>
  .config-panel {
    position: absolute;
    right: 0;
    top: 0;
    width: 300px;
    height: 100%;
    background: #2a2a2a;
    padding: 1rem;
    transform: translateX(100%);
    transition: transform 0.3s ease;
  }

  .config-panel.visible {
    transform: translateX(0);
  }

  .field {
    margin: 1rem 0;
  }

  label {
    display: block;
    margin-bottom: 0.5rem;
    color: #00ff88;
  }

  input {
    width: 100%;
    padding: 0.5rem;
    background: #3a3a3a;
    border: 1px solid #4a4a4a;
    color: white;
    border-radius: 4px;
  }
</style>