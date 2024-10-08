<script>
    let steps = [
      { number: 1, title: 'Set Up Your Environment', description: 'Install Python, Node.js, and required dependencies.' },
      { number: 2, title: 'Create a New Project', description: 'Use our CLI tool to scaffold a new AppRAD project.' },
      { number: 3, title: 'Define Your Models', description: 'Create your data models using SQLModel in the backend.' },
      { number: 4, title: 'Generate API Endpoints', description: 'Automatically generate CRUD endpoints with FastAPI.' },
      { number: 5, title: 'Design Your UI', description: 'Create responsive UI components with SvelteKit.' },
      { number: 6, title: 'Configure RBAC', description: 'Set up role-based access control for your application.' },
    ];
  </script>
  
  
  <main>
    <section class="hero is-info">
      <div class="hero-body">
        <div class="container">
          <h1 class="title mb-5">Get Started with AppRAD</h1>
          <h2 class="subtitle">Follow these steps to build your application rapidly</h2>
        </div>
      </div>
    </section>
  
    <section class="section">
      <div class="container">
        <div class="timeline">
          {#each steps as step, index}
            <div class="timeline-item">
              <div class="timeline-marker is-icon">
                <span class="icon">
                  <i class="fas fa-flag"></i>
                </span>
              </div>
              <div class="timeline-content">
                <p class="heading has-text-primary">Step {step.number}</p>
                <h1 class="title is-4">{step.title}</h1>
                <p>{step.description}</p>
              </div>
            </div>
          {/each}
        </div>
      </div>
    </section>
  
    <section class="section">
      <div class="container">
        <div class="buttons is-centered">
          <a href="/docs" class="button is-primary is-large">View Documentation</a>
          <a href="/examples" class="button is-link is-large">See Examples</a>
        </div>
      </div>
    </section>
  </main>
  
  <style>
    .timeline {
      position: relative;
      max-width: 1200px;
      margin: 0 auto;
      padding: 15px 0;
    }
    .timeline::after {
      content: '';
      position: absolute;
      width: 6px;
      background-color: #3298dc;
      top: 0;
      bottom: 0;
      left: 50%;
      margin-left: -3px;
    }
    .timeline-item {
      padding: 10px 40px;
      position: relative;
      background-color: inherit;
      width: 50%;
    }
    .timeline-item:nth-child(odd) {
      left: 0;
    }
    .timeline-item:nth-child(even) {
      left: 50%;
    }
    .timeline-content {
      padding: 20px 30px;
      background-color: white;
      position: relative;
      border-radius: 6px;
      box-shadow: 0 0.5em 1em -0.125em rgba(10, 10, 10, 0.1), 0 0px 0 1px rgba(10, 10, 10, 0.02);
    }
    .timeline-marker {
      position: absolute;
      background-color: #3298dc;
      width: 40px;
      height: 40px;
      border-radius: 50%;
      top: 15px;
      display: flex;
      align-items: center;
      justify-content: center;
      color: white;
      z-index: 1;
    }
    .timeline-item:nth-child(odd) .timeline-marker {
      right: -20px;
    }
    .timeline-item:nth-child(even) .timeline-marker {
      left: -20px;
    }
  </style>
  