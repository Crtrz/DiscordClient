Certainly! Here's the updated documentation with separate code examples for each event and function:

---

## Discord Integration Script

The Discord Integration script facilitates seamless interaction with Discord's API, leveraging websockets and webhooks to enable real-time communication and event handling.

### Features

- **Websocket Integration:** Establishes a websocket connection with Discord's gateway for receiving and dispatching events in real-time.
- **Event Handling:** Listens for key events including message creation, user authentication, and reconnections, providing extensibility for custom event handling.
- **Webhook Support:** Enables communication with Discord channels via webhooks, allowing for message transmission and response retrieval.
- **Token Management:** Securely reads the Discord account token from a file for authentication and seamless connection establishment.

### Usage

#### 1. WebSocket Event Handling

```python
# Import DiscordClient module
import DiscordClient

# Read Discord account token from file
Token = open("TOKEN", "r").read()

# Initialize DiscordWebsocket with account token
Client = DiscordClient.DiscordWebsocket(AccountToken=Token, Output=False)

# Define event handling functions
def MessageSent(MessageJson):
    # Extract message content from JSON
    Data = MessageJson.get("d", {})
    Content = Data.get("content", "")

    # Print message content
    print(Content)

def ReadyEvent(MessageJson):
    # Extract user details from JSON
    Data = MessageJson.get("d", {})
    AuthenticatedUser = Data["user"]

    # Focus on a specific guild
    Client.FocusGuild("349051257702580224") #Discord requires you to Focus guilds if you want to beable to recive events from them!

    # Print authentication details
    print(f"Authenticated User! (Ready) [Username: {AuthenticatedUser['username']}] [SessionID: {Data['session_id']}]")

def Reconnecting():
    # Print reconnection status
    print("Reconnected")

# Register event listeners
Client.WebsocketEvents.add_listener("MessageSent", MessageSent)
Client.WebsocketEvents.add_listener("ReadyEvent", ReadyEvent)
Client.WebsocketEvents.add_listener("Reconnecting", Reconnecting)
```

#### 2. Webhook Interaction

```python
# Initialize DiscordWebsocket with account token
import DiscordClient

# Read Discord account token from file
Token = open("TOKEN", "r").read()

# Initialize DiscordWebsocket with account token
Client = DiscordClient.DiscordWebsocket(AccountToken=Token, Output=False)

# Send message via webhook
Client.SendMessage({"content":"blua"}, 745430737028644917)
```

### Contact Information

For inquiries or feedback, feel free to contact the developer at: `StellarZon@outlook.com`

---

Feel free to tailor the documentation further to match your specific requirements and preferences!
