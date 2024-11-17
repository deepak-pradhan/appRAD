
# Sandbox 
_Just got GIT! Exploring the new paradigms after 15+ year no coding_

## Landing Page

![alt text](_docs/image.png)

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
![alt text](_docs/image-1.png)

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

![alt text](_docs/image-2.png)

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
    │   │   ├── 📑 in-process.json
    │   │   ├── 📑 in-process.duck
    │   │   ├── 🗃️ contexts
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



![alt text](_docs/image-3.png)

---

## To run this APP
2024.11.16: Revisiting after 2 weeks, I realized that I do forget ;)  
So here is a small document!

### 1. Serve the backend
   ```bash
   source ./sbox1/bin/activate
   fastapi run main.py --host 0.0.0.0 --port 8082
   ```

**If no error then following links will become available:**  

#### Backend-Front : [http://0.0.0.0:8082](http://0.0.0.0:8082) 
  for lean UIs with HTMX and Jinja2 
  
   ![alt text](_docs/image-3a.png "alt text")
   
#### APIs [http://0.0.0.0:8082/docs](http://0.0.0.0:8082/docs)
for simplicity, ease of use, and the auto generated docs.  
   ![alt text](_docs/image-1a.png)


#### Redoc [http://0.0.0.0:8082/redoc](http://0.0.0.0:8082/redoc)
   ![alt text](_docs/image-2a.png)

  
#### OpenAPI [http://0.0.0.0:8082/openapi.json](http://0.0.0.0:8082/openapi.json)
```json
{
  "openapi": "3.1.0",
  "info": {
    "title": "FastAPI",
    "version": "0.1.0"
  },
  "paths": {
    "/chat": {
      "post": {
        "tags": [
          "ollama"
        ],
        "summary": "Chat With Ollama",
        "operationId": "chat_with_ollama_chat_post",
        "requestBody": {
          "content": {
            "application/json": {
              "schema": {
                "$ref": "#/components/schemas/backend__models__l_model__LModel"
              }
            }
          },
          "required": true
        },
        "responses": {
          "200": {
            "description": "Successful Response",
            "content": {
              "application/json": {
                "schema": {

                }
              }
            }
          },
          "422": {
            "description": "Validation Error",
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/HTTPValidationError"
                }
              }
            }
          }
        }
      }
    },
    "/generate_code": {
```

### 2. Serve the frontend-back  (Storybook)
   ```bash
   source ./sbox1/bin/activate
   cd frontend
   npm run storybook 
   ```
![alt text](_docs/image-4a.png)


### 3. Serve the frontend
Not all the Svelte 4 pages were migrated to Svelte 5.
   ```bash
   source ./sbox1/bin/activate
   cd frontend
   npm run dev -- --open 
   ```
![alt text](_docs/image-5a.png)


---

### __init__ vs namespace
from Joshua, [Traps for the Unwary in Python’s Import System](https://python-notes.curiousefficiency.org/en/latest/python_concepts/import_traps.html)
- Removed all dunder inits, switched to **namespace** convention.
- all codes in sandbag `backend.examples..` works
- Both ollama `endpoints` (/chat & /generate_code)  works
- All 3 llama `endpoints` (chat, /fuctions, /models) failed due to unimplemented validation errors! 


### sanbag Concept of in-process, in-memory (DB & JSON), in-disk (ext files/contents)
...