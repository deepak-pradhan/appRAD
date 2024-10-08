<script>
  import { onMount } from 'svelte';

  let features = [
    { icon: 'fas fa-bolt', title: 'Fast API', description: 'High-performance backend' },
    { icon: 'fas fa-code', title: 'Svelte Frontend', description: 'Reactive UI with SvelteKit' },
    { icon: 'fas fa-database', title: 'Database Integration', description: 'Seamless ORM with SQLModel' },
    { icon: 'fas fa-shield-alt', title: 'RBAC', description: 'Role-Based Access Control' }
  ];


  onMount(() => {
    // Any initialization logic can go here
  });
</script>

<main>

  <section class="hero is-primary is-bold is-fullheight-with-navbar">
    <div class="hero-body">
      <div class="container">
        <h1
				class="title is-1 mb-6">
          Welcome to AppRAD
        </h1>
        <h2 class="subtitle is-3 mb-6">
          Rapid Application Development Framework
        </h2>        
        <a href="/dashboard" class="button is-light is-large">Get Started</a>
      </div>
    </div>
  </section>

  <section class="section">
    <div class="container">
      <h2 class="title is-2 has-text-centered">Key Features</h2>
      <div class="columns is-multiline">
        {#each features as feature}
          <div class="column is-3">
            <div class="box has-text-centered">
              <span class="icon is-large">
                <i class="{feature.icon} fa-2x"></i>
              </span>
              <h3 class="title is-4">{feature.title}</h3>
              <p>{feature.description}</p>
            </div>
          </div>
        {/each}
      </div>
    </div>
  </section>
  
</main>
