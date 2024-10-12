
# Sandbox 

## Landing Page

![alt text](image.png)

**The Hello World!**  
```html
	<!--Use ternary operator in HTML-->
	<h2 class="highlight">
		{data.visited
	    	? 'Good 2c u again 🤩'
			: 'Welcome! Glad 2c u 😎'
		}
	</h2>
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