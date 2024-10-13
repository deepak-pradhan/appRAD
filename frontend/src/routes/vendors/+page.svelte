<script lang="ts">
    import { onMount } from 'svelte';
    import { DataTable, Pagination, Search, Button, Modal, TextInput, Form, Grid, Row, Column } from 'carbon-components-svelte';
    import View from "carbon-icons-svelte/lib/View.svelte";
    import Edit from "carbon-icons-svelte/lib/Edit.svelte";
    import Trash from "carbon-icons-svelte/lib/TrashCan.svelte";

    interface Vendor {
        id: number;
        name: string;
        email: string;
        type: string;
    }

    let vendors: Vendor[] = [];
    let newVendor: Omit<Vendor, 'id'> = { name: '', email: '', type: '' };
    let editingVendor: Vendor | null = null;
    let viewingVendor: Vendor | null = null;
    let editingVendorData: Omit<Vendor, 'id'> = { name: '', email: '', type: '' };


    onMount(fetchVendors);

    async function fetchVendors() {
        const response = await fetch('http://localhost:8081/vendors');
        vendors = await response.json();
    }

    async function addVendor() {
        const response = await fetch('http://localhost:8081/vendors', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(editingVendorData)
        });
        if (response.ok) {
            await fetchVendors();
            editingVendor = null;
            editingVendorData = { name: '', email: '', type: '' };
        }
    }

    async function updateVendor() {
        if (!editingVendor) return;
        const response = await fetch(`http://localhost:8081/vendors/${editingVendor.id}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(editingVendorData)
        });
        if (response.ok) {
            await fetchVendors();
            editingVendor = null;
            editingVendorData = { name: '', email: '', type: '' };
        }
    }

    async function deleteVendor(id: number) {
        const response = await fetch(`http://localhost:8081/vendors/${id}`, { method: 'DELETE' });
        if (response.ok) await fetchVendors();
    }

    function startEditing(vendor: Vendor) {
        editingVendor = vendor;
        editingVendorData = { name: vendor.name, email: vendor.email, type: vendor.type };
    }

    function viewVendor(vendor: Vendor) {
        viewingVendor = { ...vendor };
    }
</script>

<Grid>
    <Row>
        <Column>
            <h1>Vendor Management</h1>
        </Column>
    </Row>
    <Row>
        <Column>
            <Button on:click={() => { editingVendor = {}; editingVendorData = { name: '', email: '', type: '' }; }}>
                Add New Vendor
            </Button>
        </Column>
    </Row>

    <Row>
        <Column>
            <DataTable
            headers={[
              { key: 'name', value: 'Name' },
              { key: 'email', value: 'Email' },
              { key: 'type', value: 'Type' },
              { key: 'actions', value: 'Actions' }
            ]}
            rows={vendors}
          >
            <svelte:fragment slot="cell" let:row let:cell>
              {#if cell.key === 'actions'}
                <Button kind="ghost" size="small" iconDescription="View" on:click={() => viewVendor(row)}>
                  <View />
                </Button>
                <Button kind="ghost" size="small" iconDescription="Edit" on:click={() => startEditing(row)}>
                  <Edit />
                </Button>
                <Button kind="danger-ghost" size="small" iconDescription="Delete" on:click={() => deleteVendor(row.id)}>
                  <Trash />
                </Button>
              {:else}
                {cell.value}
              {/if}
            </svelte:fragment>
          </DataTable>
          
        </Column>
    </Row>
</Grid>
   <Modal
    open={editingVendor !== null || editingVendorData.name !== ''}
    modalHeading={editingVendor ? "Edit Vendor" : "Add New Vendor"}
    primaryButtonText="Save"
    secondaryButtonText="Cancel"
    on:click:button--secondary={() => { editingVendor = null; editingVendorData = { name: '', email: '', type: '' }; }}
    on:submit={() => editingVendor ? updateVendor() : addVendor()}
>
    <form on:submit|preventDefault>
      <TextInput labelText="Name" bind:value={editingVendorData.name} required />
      <TextInput labelText="Email" type="email" bind:value={editingVendorData.email} required />
      <TextInput labelText="Type" bind:value={editingVendorData.type} required />
    </form>
</Modal>
<Modal
    open={!!viewingVendor}
    modalHeading="View Vendor"
    primaryButtonText="Close"
    on:click:button--primary={() => viewingVendor = null}
>
    <p><strong>Name:</strong> {viewingVendor?.name}</p>
    <p><strong>Email:</strong> {viewingVendor?.email}</p>
    <p><strong>Type:</strong> {viewingVendor?.type}</p>
</Modal>