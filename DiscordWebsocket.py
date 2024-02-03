import json
import threading
import time
from datetime import datetime
import requests
import colorama
from websocket import create_connection

colorama.init(autoreset=True)

def __OutPut__(Message, OutputEnabled):
    if OutputEnabled:
        now = datetime.now()
        CurrentTime = "%0.2d:%0.2d:%0.2d" % (now.hour, now.minute, now.second)
        print(colorama.Fore.MAGENTA + Message + f" [Crtrz {CurrentTime}]")


def __Error__(Message):
    now = datetime.now()
    CurrentTime = "%0.2d:%0.2d:%0.2d" % (now.hour, now.minute, now.second)
    print(colorama.Fore.RED + Message + f" [Crtrz {CurrentTime}]")

class EventDispatcher:
    def __init__(self):
        self.listeners = {}
        self.lock = threading.Lock()

    def add_listener(self, event_name, callback):
        with self.lock:
            if event_name not in self.listeners:
                self.listeners[event_name] = []
            self.listeners[event_name].append(callback)

    def remove_listener(self, event_name, callback):
        with self.lock:
            if event_name in self.listeners:
                self.listeners[event_name].remove(callback)

    def dispatch_event(self, event_name, *args, **kwargs):
        with self.lock:
            if event_name in self.listeners:
                for callback in self.listeners[event_name]:
                    threading.Thread(target=callback, args=args, kwargs=kwargs).start()

class DiscordWebsocket:
    def __init__(self, AccountToken, Output):
        self.OutPut = Output

        self.WebsocketEvents = EventDispatcher()

        self.AccountToken = AccountToken
        self.WebsocketConnection = create_connection("wss://gateway.discord.gg/?v=9&encoding=json")
        threading.Thread(target=self.__MessageCreated__).start()

        Connection = {"op": 2, "d": { "token": self.AccountToken, "properties": {"os": "Windows", "browser": "Chrome", "device": "Chrome"} } }
        self.WebsocketConnection.send(json.dumps(Connection))
        __OutPut__("Authorising User", self.OutPut)

        self.RequestSession = requests.Session()
        self.RequestSession.headers["authorization"] = AccountToken

    def __Heartbeat__(self):
        HeartbeatDictinary = {
            "op": 1,
            "d": 6322
        }

        self.WebsocketConnection.send(json.dumps(HeartbeatDictinary))
        __OutPut__("Sending Heartbeat", self.OutPut)

    def __HeartbeatLoop__(self, HeatbeatInterval):
        while True:
            time.sleep(HeatbeatInterval)
            self.__Heartbeat__()

    def __MessageCreated__(self):
        self.WebsocketEvents.add_listener("OnMessage", self.OnMessage)

        while True:
            try:
                TextMessage = self.WebsocketConnection.recv()
                if not TextMessage:
                    __Error__(f"Ran Into An Issue While Getting Returned Message. [{TextMessage}]")
                    continue

                JsonMessage = json.loads(TextMessage)
                if not JsonMessage:
                    continue

                self.WebsocketEvents.dispatch_event("OnMessage", JsonMessage)

            except Exception as e:
                __Error__(f"WebSocket connection error: {e}")
                self.reconnect()

        __OutPut__("WebSocket connection closed.", self.OutPut)

    def reconnect(self):
        __OutPut__("Reconnecting to WebSocket...", self.OutPut)
        self.WebsocketConnection = create_connection("wss://gateway.discord.gg/?v=9&encoding=json")
        Connection = {"op": 2, "d": {"token": self.AccountToken,"properties": {"os": "Windows", "browser": "Chrome", "device": "Chrome"}}}
        self.WebsocketConnection.send(json.dumps(Connection))
        __OutPut__("Reconnection successful.", self.OutPut)

        self.WebsocketEvents.dispatch_event("Reconnecting")

    def OnMessage(self, Message):
        EventType = Message.get("t")
        Data = Message.get("d")
        OpCode = Message.get("op")

        __OutPut__(f"Recived A [{EventType}] Message! [OpCode {OpCode}]", self.OutPut)

        #//All Events\\#
        if Data and "heartbeat_interval" in Data:
            HeartBeatInterval = Data["heartbeat_interval"]/1000
            self.__HeartbeatLoop__(HeartBeatInterval)

        if EventType == "MESSAGE_CREATE":
            self.WebsocketEvents.dispatch_event("MessageSent", Message)

        if EventType == "READY":
            self.SessionID = Data.get("session_id", "???")
            self.WebsocketEvents.dispatch_event("ReadyEvent", Message)

            __OutPut__(f"Authenticated User! (Ready) [SessionID: {self.SessionID}]", self.OutPut)

    def FocusGuild(self, GuildID):
        GuildRequest = {"op": 14, "d": {"guild_id": GuildID, "typing": True, "activities": True, "threads": True}}
        self.WebsocketConnection.send(json.dumps(GuildRequest))

    def SendMessage(self, PostData, ChannelID):
        RequestLink = f"https://discord.com/api/v9/channels/{ChannelID}/messages"
        Request = self.RequestSession.post(RequestLink, data=PostData)
        if Request.status_code != 200:
            __Error__(f"Got A Error While Trying To Sent Message To [{ChannelID}]. [{Request.reason}]")
        else:
            __OutPut__(f"Sent Message To [{ChannelID}]! {PostData}", True)
        return  Request


class Webhook:
    def __init__(self, Webhook, Output):
        self.OutPut = Output
        self.Webhook = Webhook

        WebhookResponse = requests.get(Webhook)

        JsonResponse = {}
        if 'application/json' in WebhookResponse.headers.get('Content-Type', ''):
            JsonResponse = WebhookResponse.json()

        self.ChannelID = JsonResponse.get("channel_id", "None")
        self.GuildID = JsonResponse.get("guild_id", "None")

        __OutPut__(f"[Guild: {self.GuildID}] [Channel: {self.ChannelID}]", self.OutPut)

    def Send(self, WebhookData):
        response = requests.post(self.Webhook, json=WebhookData)
        __OutPut__(f"Got A [{response.status_code}] Status Code From Webhook. [{response.reason}]", self.OutPut)
