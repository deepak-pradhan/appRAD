<script lang="ts">
    import { onMount } from 'svelte';
    import type { PageData } from './$types';

    export let data: PageData;
    let vendors = data.vendors;

    onMount(fetchVendors);

    async function fetchVendors() {
        try {
            const response = await fetch('http://localhost:8081/vendors');
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const data = await response.json();
            vendors = data;
        } catch (error) {
            console.error('Error fetching vendors:', error);
        }
    }
</script>

<main class="section">
    <div class="container">
        <h1 class="title">Smart Vendor Management</h1>

        <!-- Vendor List -->
        <div class="box">
            <h2 class="title is-4">Vendor List</h2>
            <table class="table is-fullwidth">
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
                                <button class="button is-small is-info" on:click={() => viewingVendor = vendor}>View</button>
                                <button class="button is-small is-warning" on:click={() => editingVendor = {...vendor}}>Edit</button>
                                <button class="button is-small is-danger" on:click={() => deleteVendor(vendor.id)}>Delete</button>
                            </td>
                        </tr>
                    {/each}
                </tbody>
            </table>
        </div>

        <!-- Add New Vendor -->
        <div class="box">
            <h2 class="title is-4">Add New Vendor</h2>
            <form on:submit|preventDefault={createVendor}>
                <div class="field">
                    <label class="label">Name</label>
                    <div class="control">
                        <input class="input" type="text" bind:value={newVendor.name} required>
                    </div>
                </div>
                <div class="field">
                    <label class="label">Email</label>
                    <div class="control">
                        <input class="input" type="email" bind:value={newVendor.email} required>
                    </div>
                </div>
                <div class="field">
                    <label class="label">Type</label>
                    <div class="control">
                        <input class="input" type="text" bind:value={newVendor.type} required>
                    </div>
                </div>
                <div class="field">
                    <div class="control">
                        <button type="submit" class="button is-primary">Add Vendor</button>
                    </div>
                </div>
            </form>
        </div>

        <!-- Policy Q&A -->
        <div class="box">
            <h2 class="title is-4">Vendor Policy Q&A</h2>
            <div class="field">
                <label class="label">Ask a question about vendor policies</label>
                <div class="control">
                    <input class="input" type="text" bind:value={policyQuestion} placeholder="E.g., What is our policy on vendor payment terms?">
                </div>
            </div>
            <div class="field">
                <div class="control">
                    <button class="button is-primary" on:click={askPolicyQuestion}>Ask Question</button>
                </div>
            </div>
            {#if policyAnswer}
                <div class="notification">
                    <strong>Answer:</strong> {policyAnswer}
                </div>
            {/if}
        </div>
    </div>
</main>

<!-- Modals for viewing and editing vendors -->
{#if viewingVendor}
    <div class="modal is-active">
        <div class="modal-background"></div>
        <div class="modal-card">
            <header class="modal-card-head">
                <p class="modal-card-title">Vendor Details</p>
                <button class="delete" aria-label="close" on:click={() => viewingVendor = null}></button>
            </header>
            <section class="modal-card-body">
                <p><strong>Name:</strong> {viewingVendor.name}</p>
                <p><strong>Email:</strong> {viewingVendor.email}</p>
                <p><strong>Type:</strong> {viewingVendor.type}</p>
                <p><strong>Description:</strong> {viewingVendor.description || 'No description available.'}</p>
                <button class="button is-small" on:click={() => generateVendorDescription(viewingVendor)}>
                    Generate Description
                </button>
            </section>
            <footer class="modal-card-foot">
                <button class="button" on:click={() => viewingVendor = null}>Close</button>
            </footer>
        </div>
    </div>
{/if}

{#if editingVendor}
    <div class="modal is-active">
        <div class="modal-background"></div>
        <div class="modal-card">
            <header class="modal-card-head">
                <p class="modal-card-title">Edit Vendor</p>
                <button class="delete" aria-label="close" on:click={() => editingVendor = null}></button>
            </header>
            <section class="modal-card-body">
                <div class="field">
                    <label class="label">Name</label>
                    <div class="control">
                        <input class="input" type="text" bind:value={editingVendor.name} required>
                    </div>
                </div>
                <div class="field">
                    <label class="label">Email</label>
                    <div class="control">
                        <input class="input" type="email" bind:value={editingVendor.email} required>
                    </div>
                </div>
                <div class="field">
                    <label class="label">Type</label>
                    <div class="control">
                        <input class="input" type="text" bind:value={editingVendor.type} required>
                    </div>
                </div>
            </section>
            <footer class="modal-card-foot">
                <button class="button is-success" on:click={updateVendor}>Save changes</button>
                <button class="button" on:click={() => editingVendor = null}>Cancel</button>
            </footer>
        </div>
    </div>
{/if}