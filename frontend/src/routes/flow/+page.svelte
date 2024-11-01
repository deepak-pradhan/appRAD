<!-- src/routes/flow/+page.svelte -->
<script lang="ts">
  import FlowBuilder from '$lib/components/flow-builder/FlowBuilder.svelte';
</script>

<main class="flow-page">
  <h1>Visual Flow Builder</h1>
  <FlowBuilder />
</main>

<style>
  .flow-page {
    padding: 2rem;
    max-width: 1200px;
    margin: 0 auto;
  }

  h1 {
    color: #00ff88;
    margin-bottom: 2rem;
  }
</style>
