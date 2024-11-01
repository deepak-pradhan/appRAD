
<script lang="ts">
  import { nodeTypes } from './nodeTypes';
  import { createEventDispatcher } from 'svelte';

  export let id: string;
  export let type: string;
  export let title: string;
  export let x: number;
  export let y: number;

  const dispatch = createEventDispatcher();

  const nodeConfig = nodeTypes[type];
  const inputPorts = nodeConfig.ports.filter(p => p.type === 'input');
  const outputPorts = nodeConfig.ports.filter(p => p.type === 'output');
</script>

<div class="node {nodeConfig.shape}" style="transform: translate({x}px, {y}px)">
  <button class="delete-btn" on:click={() => dispatch('delete', { id })}>×</button>
  <div class="title">{title}</div>
  
  <div class="ports-container">
    <div class="input-ports">
      {#each inputPorts as port}
        <div class="port input" data-port-id={port.id}>
          <span class="port-name">{port.name}</span>
        </div>
      {/each}
    </div>
    
    <div class="output-ports">
      {#each outputPorts as port}
        <div class="port output" data-port-id={port.id}>
          <span class="port-name">{port.name}</span>
        </div>
      {/each}
    </div>
  </div>
</div>

<style>
  .node {
    position: absolute;
    padding: 1rem;
    color: #00ff88;
    font-weight: bold;
    min-width: 150px;
  }

  .circle {
    border-radius: 50%;
    background: #2a2a2a;
  }

  .rectangle {
    border-radius: 8px;
    background: #2a2a2a;
  }

  .diamond {
    transform: rotate(45deg);
    background: #2a2a2a;
  }

  .ports-container {
    display: flex;
    justify-content: space-between;
    margin-top: 1rem;
  }

  .port {
    width: 12px;
    height: 12px;
    background: #00ff88;
    border-radius: 50%;
    margin: 4px;
    cursor: crosshair;
    position: relative;
  }

  .port-name {
    position: absolute;
    font-size: 0.8rem;
    white-space: nowrap;
  }

  .input .port-name {
    right: 100%;
    margin-right: 8px;
  }

  .output .port-name {
    left: 100%;
    margin-left: 8px;
  }
</style>

