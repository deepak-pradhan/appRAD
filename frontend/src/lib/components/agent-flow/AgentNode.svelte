<!-- lib/components/agent-flow/AgentNode.svelte -->
<script lang="ts">
  import { agentNodeTypes } from './types/nodeTypes';
  
  export let id: string;
  export let type: string;
  export let title: string;
  export let x: number;
  export let y: number;

  const nodeConfig = agentNodeTypes[type];
  const inputPorts = nodeConfig.ports.filter(p => p.type === 'input');
  const outputPorts = nodeConfig.ports.filter(p => p.type === 'output');
</script>

<div class="node {nodeConfig.shape}" style="transform: translate({x}px, {y}px)">
  <div class="title">{title}</div>
  
  <div class="ports-container">
    <div class="input-ports">
      {#each inputPorts as port}
        <div class="port input">
          <span class="port-name">{port.name}</span>
        </div>
      {/each}
    </div>
    
    <div class="output-ports">
      {#each outputPorts as port}
        <div class="port output">
          <span class="port-name">{port.name}</span>
        </div>
      {/each}
    </div>
  </div>
</div>