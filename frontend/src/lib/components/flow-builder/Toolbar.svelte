<!-- lib/components/flow-builder/Toolbar.svelte -->
<script lang="ts">
  import { createEventDispatcher } from 'svelte';
  const dispatch = createEventDispatcher();

  const nodeTypes = [
    { type: 'input', icon: '📥' },
    { type: 'process', icon: '⚙️' },
    { type: 'output', icon: '📤' }
  ];

  function handleDragStart(event: DragEvent, type: string) {
    event.dataTransfer?.setData('nodeType', type);
  }

  function handleDrop(event: DragEvent) {
    const type = event.dataTransfer?.getData('nodeType');
    if (type) {
      dispatch('addNode', {
        type,
        x: event.clientX,
        y: event.clientY
      });
    }
  }
</script>

<div class="toolbar">
  {#each nodeTypes as {type, icon}}
    <div 
      class="tool"
      draggable="true"
      on:dragstart={(e) => handleDragStart(e, type)}
    >
      <span>{icon}</span>
      {type}
    </div>
  {/each}
</div>

<style>
  .toolbar {
    position: absolute;
    top: 1rem;
    left: 1rem;
    display: flex;
    gap: 1rem;
    z-index: 100;
  }

  .tool {
    background: #2a2a2a;
    color: #00ff88;
    padding: 0.5rem 1rem;
    border-radius: 4px;
    cursor: move;
    display: flex;
    align-items: center;
    gap: 0.5rem;
    user-select: none;
  }

  .tool:hover {
    transform: translateY(-2px);
  }
</style>