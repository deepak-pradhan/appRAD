<!-- lib/components/agent-flow/AgentFlowBuilder.svelte -->
<script lang="ts">
  import AgentNode from './AgentNode.svelte';
  import AgentToolbar from './AgentToolbar.svelte';
  
  let nodes = [
    { id: '1', type: 'llm', title: 'LLM Node', x: 100, y: 100 },
    { id: '2', type: 'function', title: 'Function Node', x: 300, y: 200 }
  ];

  let connections: Connection[] = [];
  let selectedNode: any = null;
</script>

<div class="flow-canvas">
  <AgentToolbar />
  
  <svg class="connections">
    {#each connections as conn}
      <path class="connection-line"/>
    {/each}
  </svg>
  
  {#each nodes as node}
    <AgentNode {...node} />
  {/each}
</div>

<style>
  .flow-canvas {
    width: 100%;
    height: 800px;
    background: #1a1a1a;
    position: relative;
    overflow: hidden;
  }

  .connections {
    position: absolute;
    width: 100%;
    height: 100%;
    pointer-events: none;
  }

  .connection-line {
    fill: none;
    stroke: #00ff88;
    stroke-width: 2px;
  }
</style>