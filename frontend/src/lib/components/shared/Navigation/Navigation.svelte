<!-- lib/components/shared/Navigation/Navigation.svelte -->
<nav class="main-nav">
  <div class="nav-container">
    <div class="logo">AppRAD</div>
    <div class="nav-links">
      <a href="/">Home</a>
      <a href="/chat">AI Chat</a>
      <a href="/codegen">Code Generator</a>
      <a href="/flow">Flow Builder</a>
    </div>
  </div>
</nav>

<style>
  .main-nav {
    background: rgba(26, 26, 26, 0.95);
    backdrop-filter: blur(10px);
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    position: sticky;
    top: 0;
    z-index: 100;
  }

  .nav-container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 1rem 2rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }

  .logo {
    font-size: 1.5rem;
    font-weight: bold;
    background: linear-gradient(to right, #00ff88, #00bfff);
    -webkit-background-clip: text;
    color: transparent;
  }

  .nav-links {
    display: flex;
    gap: 2rem;
  }

  a {
    color: #fff;
    text-decoration: none;
    font-weight: 500;
    transition: color 0.3s ease;
  }

  a:hover {
    color: #00ff88;
  }
</style> 