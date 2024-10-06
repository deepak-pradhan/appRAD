<style>
    table {
      width: 100%;
      border-collapse: collapse;
    }
    th, td {
      padding: 8px;
      text-align: left;
      border-bottom: 1px solid #ddd;
    }
    button {
      margin: 2px;
      padding: 5px 10px;
      background-color: #4CAF50;
      color: white;
      border: none;
      cursor: pointer;
    }
    button:hover {
      background-color: #45a049;
    }
  </style>
  
  <script lang="ts">
    import { onMount } from 'svelte';
  
    let vendors: any[] = [];
  
    onMount(async () => {
        const response = await fetch('http://localhost:8081/vendors');
        vendors = await response.json();
	    // console.log(vendors);
    });

    async function deleteVendor(id: number) {
        await fetch(`http://localhost:8081/vendors/${id}`, { method: 'DELETE' });
        vendors = vendors.filter(v => v.id !== id);
    }
</script>
  
  <h1>Vendors List</h1>
  
  <table>
    <thead>
      <tr>
        <th>Name</th>
        <th>Email</th>
        <th>Type</th>
        <th>Actions</th>
      </tr>
    </thead>
    <tbody>
      {#each vendors as vendor}
        <tr>
          <td>{vendor.name}</td>
          <td>{vendor.email}</td>
          <td>{vendor.type}</td>
          <td>
            <button on:click={() => editVendor(vendor.id)}>Edit</button>
            <button on:click={() => deleteVendor(vendor.id)}>Delete</button>
          </td>
        </tr>
      {/each}
    </tbody>
  </table>

  <!-- <button on:click={createVendor}>Add New Vendor</button> -->

S