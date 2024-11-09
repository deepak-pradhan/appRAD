<!-- lib/components/flow-builder/ConfigPanel.svelte -->
<script lang="ts">
  export let selectedNode: any = null;
</script>

<div class="config-panel" class:visible={selectedNode}>
  <div class="panel-content">
    <h3>Node Configuration</h3>
    
    {#if selectedNode}
      <div class="field">
        <label>Title</label>
        <input type="text" bind:value={selectedNode.title} />
      </div>

      <div class="field">
        <label>Position</label>
        <div class="coords">
          <input type="number" bind:value={selectedNode.x} />
          <input type="number" bind:value={selectedNode.y} />
        </div>
      </div>
    {/if}
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

  h3 {
    color: #00ff88;
    margin-bottom: 1rem;
  }

  .field {
    margin: 1rem 0;
  }

  label {
    display: block;
    color: #00ff88;
    margin-bottom: 0.5rem;
  }

  input {
    width: 100%;
    padding: 0.5rem;
    background: #3a3a3a;
    border: 1px solid #4a4a4a;
    color: white;
    border-radius: 4px;
  }

  .coords {
    display: flex;
    gap: 1rem;
  }
</style>