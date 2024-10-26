
# Sandbox 
_Just got GIT! Exploring the new paradigms after 15+ year no coding_

## Landing Page

![alt text](image.png)

**The Hello World!, the Svelte way**  
```html
    <Column class="hero-content">
        <h1>
            Hello, <span class="highlight">{data.visited ? 'friend' : 'stranger'}!</span>
        </h1>

        <!--Use ternary operator in HTML-->
        <h2 class="highlight">
            {data.visited
               ? 'Good 2c u again 🤩'
               : 'Welcome! Glad 2c u 😎'
            }
        </h2>

        <Button href="/get-started" kind="primary" class="custom-button">Get Started</Button>
    </Column>
```                

## Chat
![alt text](image-1.png)

**Less Clutter**
```html
        <Row>
            <Column>
                {#if errorMessage}
                    <InlineNotification
                        kind="error"
                        title="Error"
                        subtitle={errorMessage}
                        hideCloseButton
                    />
                {/if}
                <div class="chat-container">
                    <div class="chat-history">
                        {#each chatHistory as message}
                            <div class={`chat-bubble ${message.role === 'user' ? 'user-bubble' : 'ai-bubble'}`}>
                                {#if message.role === 'user'}
                                    <p>{message.content}</p>
                                {:else}
                                    {@html formatMessage(message.content)}
                                {/if}
                            </div>
                        {/each}
                    </div>

                    {#if isLoading}
                        <ProgressBar />
                    {/if}
                </div>
            </Column>
        </Row>
```

## Code Generator: I got Huang Nguyen & Entu Chu! 

![alt text](image-2.png)

**Inital Structure**
- 2024.10.26: @WIP stucture: skeleton, concept only, untested.   

```yaml
├── 📑 README.md
├── 📑 main.py
├── 🗂️  backend
│   ├── 🗂️  controllers
│   │   └── 🗂️  bases
│   ├── 🗂️  db
│   │   └── 🗂️  stores
    │   │   ├── 📑 in-process.db
    │   │   ├── 🗃️ context
│   │   └── 🗂️  tools
│   ├── 🗂️  helpers
│   ├── 🗂️  middlewares
│   ├── 🗂️  models
│   │   └── 🗂️  bases
│   │   └── 🗃️  enums
│   └── 🧰  utils
└── 🗂️  frontend (TBD)
    ├── 🗂️  src
    │   ├── 🗂️  lib
    │   ├── 🗂️  routes
    │   │   ├── 🗂️  chat
    │   │   ├── 🗂️  codegen
    │   │   ├── 🗂️  get-started
    │   └── 🗂️  utils
    └── 🗂️  static
```    