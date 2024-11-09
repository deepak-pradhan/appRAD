<!-- lib/components/shared/Hero/Hero.svelte -->
<script lang="ts">
  export let title: string;
  export let subtitle: string;
  export let ctaText: string;
</script>

<section class="hero">
  <div class="hero-content">
    <h1>{@html title}</h1>
    <p>{subtitle}</p>
    <button class="cta">{ctaText}</button>
  </div>  
</section>

<style>
  .hero {
    min-height: 60vh;
    display: flex;
    align-items: center;
    justify-content: center;
  }

  .hero-content {
    text-align: center;
    max-width: 800px;
  }
</style>