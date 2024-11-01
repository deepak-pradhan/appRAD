
<!-- src/routes/chat/+page.svelte -->
<script>
  import OllamaChat from '$lib/components/chat/OllamaChat.svelte';
</script>

<main>
  <h1>AI Chat Interface</h1>
  <OllamaChat modelName="llama3.1:8b" theme="dark" />
</main>

<style>
  main {
    padding: 2rem;
    max-width: 1200px;
    margin: 0 auto;
  }

  h1 {
    margin-bottom: 2rem;
  }
</style>
