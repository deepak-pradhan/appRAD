<script lang="ts">
    import { onMount } from 'svelte';
  
    let vendors: any[] = [];
  
    onMount(async () => {
      const response = await fetch('http://localhost:8081/vendors');
      vendors = await response.json();
	  console.log(vendors);
    });
</script>
  
  <h1>Vendors List</h1>
  
  {#if vendors.length > 0}
    <ul>
      {#each vendors as vendor}
        <li>{vendor.name}</li>
      {/each}
    </ul>
  {:else}
    <p>Loading vendors...</p>
  {/if}