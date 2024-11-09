<!-- lib/components/flow-builder/FlowBuilder.svelte -->
<script lang="ts">
  import Toolbar from './Toolbar.svelte';
  import ConfigPanel from './ConfigPanel.svelte';
  
  let nextId = 4;  // Since we already have 3 nodes

  let nodes = [
    { id: '1', title: 'Input', x: 100, y: 100 },
    { id: '2', title: 'Process', x: 300, y: 200 },
    { id: '3', title: 'Output', x: 500, y: 100 }
  ];

  let connections = [
    { from: '1', to: '2' },
    { from: '2', to: '3' }
  ];

  function drawConnection(from: string, to: string) {
    const fromNode = nodes.find(n => n.id === from);
    const toNode = nodes.find(n => n.id === to);
    
    if (!fromNode || !toNode) {
      return '';
    }
    
    const x1 = fromNode.x + 20;
    const y1 = fromNode.y + 20;
    const x2 = toNode.x;
    const y2 = toNode.y + 20;
    
    return `M ${x1} ${y1} C ${(x1 + x2) / 2} ${y1}, ${(x1 + x2) / 2} ${y2}, ${x2} ${y2}`;
  }

  let isDragging = false;
  let draggedNode: any = null;
  let dragOffset = { x: 0, y: 0 };

  function handleMouseDown(event: MouseEvent, node: any) {
    isDragging = true;
    draggedNode = node;
    dragOffset = {
      x: event.clientX - node.x,
      y: event.clientY - node.y
    };
  }

  function handleMouseMove(event: MouseEvent) {
    if (isDragging && draggedNode) {
      draggedNode.x = event.clientX - dragOffset.x;
      draggedNode.y = event.clientY - dragOffset.y;
      nodes = nodes; // Trigger reactivity
    }
    if (isConnecting) {
      connectionEnd = { x: event.clientX, y: event.clientY };
    }
  }

  function handleMouseUp() {
    isDragging = false;
    draggedNode = null;
  }

  function handleAddNode(event: CustomEvent) {
    const { type, x, y } = event.detail;
    nodes = [...nodes, {
      id: String(nextId++),
      title: type,
      x,
      y
    }];
  }

  function deleteNode(id: string) {
    nodes = nodes.filter(n => n.id !== id);
    connections = connections.filter(c => c.from !== id && c.to !== id);
  }

  let selectedNode: any = null;

  function handleNodeClick(event: MouseEvent, node: any) {
    if (!isDragging) {
      selectedNode = node;
    }
  }

  function handleCanvasClick(event: MouseEvent) {
    if (event.target === event.currentTarget) {
      selectedNode = null;
    }
  }

  function handleDragOver(event: DragEvent) {
    event.preventDefault();
  }

  function handleDrop(event: DragEvent) {
    event.preventDefault();
    const type = event.dataTransfer?.getData('nodeType');
    if (type) {
      nodes = [...nodes, {
        id: String(nextId++),
        title: type.charAt(0).toUpperCase() + type.slice(1),
        x: event.clientX - 50,  // Center the node under cursor
        y: event.clientY - 20
      }];
    }
  }

  let isConnecting = false;
  let connectionStart: any = null;
  let connectionEnd = { x: 0, y: 0 };

  function startConnection(node: any, isOutput: boolean) {
    isConnecting = true;
    connectionStart = { node, isOutput };
  }

  function finishConnection(node: any) {
    if (isConnecting && connectionStart.node.id !== node.id) {
      const newConnection = connectionStart.isOutput 
        ? { from: connectionStart.node.id, to: node.id }
        : { from: node.id, to: connectionStart.node.id };
      
      connections = [...connections, newConnection];
    }
    isConnecting = false;
  }
  function saveFlow() {
        const flowConfig = {
            id: crypto.randomUUID(),
            name: `Flow ${new Date().toLocaleString()}`,
            nodes,
            connections,
            timestamp: new Date().toISOString()
        };

        // Get existing flows or initialize empty array
        const savedFlows = JSON.parse(localStorage.getItem('flows') || '[]');
        savedFlows.push(flowConfig);
        localStorage.setItem('flows', JSON.stringify(savedFlows));  
    }

    let savedFlows: any[] = [];
    let selectedFlowId: string | null = null;

    // onMount(() => {
    //     savedFlows = JSON.parse(localStorage.getItem('flows') || '[]');
    // });

    function loadFlow() {
        if (selectedFlowId) {
            const flow = savedFlows.find(f => f.id === selectedFlowId);
            if (flow) {
                nodes = flow.nodes;
                connections = flow.connections;
            }
        }
    }
</script>

<div class="flow-canvas"
  on:mousemove={handleMouseMove}
  on:mouseup={handleMouseUp}
  on:mouseleave={handleMouseUp}
  on:click={handleCanvasClick}
  on:dragover={handleDragOver}
  on:drop={handleDrop}
>
  <Toolbar on:addNode={handleAddNode} />

  <div class="flow-controls">
    <button class="control-btn" on:click={saveFlow}>Save Flow</button>
    <select bind:value={selectedFlowId}>
      <option value={null}>Select a flow...</option>
      {#each savedFlows as flow}
        <option value={flow.id}>{flow.name}</option>
      {/each}
    </select>
    <button class="control-btn" on:click={loadFlow}>Load Flow</button>
  </div>
  
  <svg class="connections">
    {#each connections as conn}
      <path d={drawConnection(conn.from, conn.to)} class="connection-line"/>
    {/each}
    
    {#if isConnecting}
      <path 
        d={drawTempConnection(connectionStart.node, connectionEnd)} 
        class="connection-line temp"
      />
    {/if}
  </svg>
  {#each nodes as node}
    <div 
      class="node" 
      class:selected={selectedNode === node}
      style="transform: translate({node.x}px, {node.y}px)"
      on:mousedown={(e) => handleMouseDown(e, node)}
      on:click={(e) => handleNodeClick(e, node)}
    >
      <button class="delete-btn" on:click={() => deleteNode(node.id)}>×</button>
      {node.title}
      <div class="ports">
        <div 
          class="port input" 
          on:mouseup={() => finishConnection(node)}
        />
        <div 
          class="port output"
          on:mousedown={() => startConnection(node, true)}
        />
      </div>
    </div>
  {/each}

<style>
  .ports {
    display: flex;
    justify-content: space-between;
    margin-top: 8px;
  }

  .port {
    width: 12px;
    height: 12px;
    background: #00ff88;
    border-radius: 50%;
    cursor: crosshair;
  }

  .port:hover {
    transform: scale(1.2);
  }
</style>
  <ConfigPanel bind:selectedNode />
</div>
<style>
  .flow-canvas {
    width: 100%;
    height: 800px;
    background: #1a1a1a;
    position: relative;
    overflow: hidden;
  }
  .node {
    position: absolute;
    background: #2a2a2a;
    border-radius: 8px;
    padding: 1rem;
    color: #00ff88;
    font-weight: bold;
    cursor: grab;
    transition: transform 0.2s ease, box-shadow 0.3s ease, opacity 0.3s ease;
    animation: nodeAppear 0.3s ease;
  }

  .node:active {
    cursor: grabbing;
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
    stroke-dasharray: 10;
    animation: flowLine 1s linear infinite;
  }

  .delete-btn {
    position: absolute;
    top: 4px;
    right: 4px;
    width: 20px;
    height: 20px;
    border-radius: 50%;
    border: none;
    background: #ff4444;
    color: white;
    font-size: 16px;
    line-height: 1;
    cursor: pointer;
    opacity: 0;
    transition: opacity 0.2s;
  }

  .node:hover .delete-btn {
    opacity: 1;
  }

  .node.selected {
    box-shadow: 0 0 0 2px #00ff88,
                0 0 20px rgba(0, 255, 136, 0.5);
  }

  .node.deleting {
    animation: nodeDelete 0.3s ease;
  }

  @keyframes flowLine {
    from { stroke-dashoffset: 20; }
    to { stroke-dashoffset: 0; }
  }

  @keyframes nodeAppear {
    from { 
      transform: scale(0.8); 
      opacity: 0; 
    }
    to { 
      transform: scale(1); 
      opacity: 1; 
    }
  }

  @keyframes nodeDelete {
    to { 
      transform: scale(0.8); 
      opacity: 0; 
    }
  }

  .flow-controls {
    position: absolute;
    top: 1rem;
    right: 1rem;
    display: flex;
    gap: 1rem;
    z-index: 100;
  }

  select {
    padding: 0.5rem;
    background: #2a2a2a;
    color: #00ff88;
    border: 1px solid #00ff88;
    border-radius: 4px;
    cursor: pointer;
  }

  select option {
    background: #2a2a2a;
    color: #00ff88;
  }
</style>
