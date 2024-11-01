<!-- lib/components/shared/Features/Features.svelte -->
<script lang="ts">
  interface Feature {
    title: string;
    description: string;
    icon: string;
    gradient: string;
  }
  
  export let features: Feature[];
</script>

<section class="features">
  <div class="features-grid">
    {#each features as feature}
      <div class="feature-card">
        <div class="icon-wrapper {feature.gradient}">
          <span class="icon">{feature.icon}</span>
        </div>
        <h3>{feature.title}</h3>
        <p>{feature.description}</p>
      </div>
    {/each}
  </div>
</section>

<style>
  .features-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 2rem;
    padding: 4rem 2rem;
    max-width: 1200px;
    margin: 0 auto;
  }

  .feature-card {
    padding: 2rem;
    border-radius: 12px;
    background: rgba(255, 255, 255, 0.05);
    backdrop-filter: blur(10px);
    transition: transform 0.3s ease;
  }

  .feature-card:hover {
    transform: translateY(-5px);
  }

  .icon-wrapper {
    width: 60px;
    height: 60px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    margin-bottom: 1rem;
    font-size: 1.5rem;
  }

  h3 {
    font-size: 1.5rem;
    margin: 1rem 0;
    background: linear-gradient(to right, #00ff88, #00bfff);
    -webkit-background-clip: text;
    color: transparent;
  }

  p {
    color: #a0a0a0;
    line-height: 1.6;
  }
</style>
