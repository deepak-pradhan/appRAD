<!-- src/routes/+page.svelte -->
<script>
  import Hero from '../lib/components/shared/Hero/Hero.svelte';
  import Features from '../lib/components/shared/Features/Features.svelte';
  import Button from '../lib/components/shared/Button/Button.svelte';
  const features = [
  // Core Technical Features
  {
    title: 'Metadata & Schema Management',
    description: 'Intelligent schema evolution with SQLModel, powering rapid application development through metadata-driven architecture',
    icon: '🔄',
    gradient: 'from-violet-500 to-purple-500'
  },
  {
    title: 'In-Process Memory',
    description: 'High-performance context management inspired by AIOS Storage Manager, using TinyDB for lightning-fast LLM operations',
    icon: '⚡',
    gradient: 'from-blue-500 to-cyan-500'
  },
  {
    title: 'LLM Integration',
    description: 'Advanced AI capabilities with structured workflows, optimized for rural agricultural applications',
    icon: '🤖',
    gradient: 'from-orange-500 to-amber-500'
  },
  // Development Tools
  {
    title: 'Visual Flow Builder',
    description: 'Design complex agricultural workflows visually with Rete.js, perfect for collaborative development',
    icon: '📊',
    gradient: 'from-pink-500 to-rose-500'
  },
  {
    title: 'Code Generation',
    description: 'Rapid prototyping tools generating production-ready code for agricultural applications',
    icon: '🚀',
    gradient: 'from-indigo-500 to-purple-500'
  },
  {
    title: 'AI Development',
    description: 'Smart coding assistance powered by Llama and AIOS foundation models, tailored for agricultural solutions',
    icon: '🧠',
    gradient: 'from-teal-500 to-emerald-500'
  }
];</script>

<main class="landing">
  <div class="gradient-bg">
    <Hero 
      title="Build Apps <span class='gradient-text'>Faster</span>"
      subtitle="Visual Development Platform Powered by AI"
      ctaText="Start Building"
    />
  </div> 
  
  <Features {features} />
  
  <section class="cta-section">
    <h2 class="gradient-text">Ready to Transform Your Development?</h2>
    <Button href="/get-started" kind="primary">Get Started Now</Button>
  </section>
</main>

<style>
  .landing {
    min-height: 100vh;
    background: #0a0a0a;
    color: #fff;
    overflow: hidden;
  }

  .gradient-bg {
    position: relative;
    background: linear-gradient(145deg, #1a1a1a, #2a2a2a);
    overflow: hidden;
  }

  .gradient-bg::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: radial-gradient(circle at 50% 50%, rgba(45, 212, 191, 0.1), transparent 50%);
    animation: pulse 8s ease infinite;
  }

  .gradient-text {
    background: linear-gradient(to right, #00ff88, #00bfff);
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent;
    animation: hue-rotate 10s infinite linear;
  }

  .cta-section {
    text-align: center;
    padding: 8rem 2rem;
    position: relative;
    background: linear-gradient(to bottom, transparent, #1a1a1a);
  }

  h2 {
    margin-bottom: 2rem;
    font-size: 3.5rem;
    font-weight: 700;
    line-height: 1.2;
  }

  @keyframes pulse {
    0%, 100% { transform: scale(1); }
    50% { transform: scale(1.05); }
  }

  @keyframes hue-rotate {
    from { filter: hue-rotate(0deg); }
    to { filter: hue-rotate(360deg); }
  }
</style>