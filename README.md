### DiscordClient Library Documentation

This documentation should help you use the `Webhook` class to send data to Discord channels via webhooks.

### Notes
- Ensure that you have installed the required dependencies (`colorama`, `websocket`, `requests`) before using the library.
- Make sure you handle exceptions properly, especially when dealing with network connections and websockets.

This documentation should help you get started with using the `DiscordClient` library for building Discord bots or interacting with Discord's API using websockets.


#### Importing the Library
```python
import DiscordClient
```

#### Creating a Discord Client Instance
```python
Token = open("TOKEN", "r").read()  # Read your Discord bot token from a file
Client = DiscordClient.DiscordWebsocket(AccountToken=Token, Output=False)
```

#### Registering Event Handlers
```python
# Define event handler functions
def MessageSent(MessageJson):
    # Your logic to handle a message sent event
    pass

def ReadyEvent(MessageJson):
    # Your logic to handle a ready event
    pass

def Reconnecting():
    # Your logic to handle reconnection
    pass

# Register event handlers
Client.WebsocketEvents.add_listener("MessageSent", MessageSent)
Client.WebsocketEvents.add_listener("ReadyEvent", ReadyEvent)
Client.WebsocketEvents.add_listener("Reconnecting", Reconnecting)
```

#### Sending Messages
```python
# Send a message to a specific channel
Client.SendMessage({"content": "Your message content"}, channel_id)
```

#### Focusing on a Guild
```python
# Focus on a specific guild to receive events from it
Client.FocusGuild("guild_id")
```

#### Running the Client
```python
# The client runs asynchronously and will handle events in the background
# Make sure your script keeps running to maintain the WebSocket connection
```

### Event Handling
The following events are available for handling:

- **MessageSent:** Triggered when a message is sent.
- **ReadyEvent:** Triggered when the bot is ready and connected to Discord.
- **Reconnecting:** Triggered when the bot is attempting to reconnect to Discord.

### Webhook Class Documentation

### Notes
- The `Webhook` class allows you to interact with Discord webhooks.
- You need to provide the URL of the webhook when creating an instance of the `Webhook` class.
- The `Send()` method allows you to send data (like messages) to the specified webhook URL.
- You can customize the message content, username, and avatar URL when sending data via the webhook.

#### Importing the Library
```python
import DiscordClient
```

#### Creating a Webhook Instance
```python
# Initialize a Webhook instance with the webhook URL and output option
webhook_url = "your_webhook_url_here"
webhook = DiscordClient.Webhook(webhook_url, Output=False)
```

#### Sending Data via Webhook
```python
# Define the data you want to send via the webhook
webhook_data = {
    "content": "Your message content",
    "username": "Your custom username (optional)",
    "avatar_url": "URL of the avatar (optional)"
}

# Send the data via the webhook
webhook.Send(webhook_data)
```

#### Example Usage:
```python
webhook_url = "your_webhook_url_here"
webhook = DiscordClient.Webhook(webhook_url)

webhook_data = {
    "content": "Hello from the webhook!",
    "username": "Webhook Bot",
    "avatar_url": "https://example.com/avatar.png"
}

webhook.Send(webhook_data)
```
