Sure! Here's some API documentation on how to use the `DiscordClient` library:

### DiscordClient Library Documentation

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

### Notes
- Ensure that you have installed the required dependencies (`colorama`, `websocket`, `requests`) before using the library.
- Make sure you handle exceptions properly, especially when dealing with network connections and websockets.

This documentation should help you get started with using the `DiscordClient` library for building Discord bots or interacting with Discord's API using websockets.
