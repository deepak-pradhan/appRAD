<!-- src/routes/codegen/+page.svelte -->
<script>
    import CodeGenerator from '$lib/components/code-gen/CodeGenerator.svelte';
  </script>
  
  <main>
    <h1>Code Generator</h1>
    <CodeGenerator language="python" theme="dark" />
  </main>
  
  <style>
    main {
      padding: 2rem;
      max-width: 1200px;
      margin: 0 auto;
    }
  </style>
  