# Chat App — Real-Time Room-Based Chat API

A real-time group chat backend built with Django and Django Channels. Users join named rooms with a username, send messages and reactions live, and see who joins or leaves — all over WebSockets. Messages are persisted in a database, and active users are tracked in memory.

---

## Tech Stack

- **Django 6** — web framework
- **Django Channels** — WebSocket support
- **Daphne** — ASGI server
- **Django REST Framework** — REST API
- **Redis** — channel layer for broadcasting
- **SQLite** — database (default)

---

## Project Structure

```
chat_app/
├── chat_app/
│   ├── settings.py
│   ├── asgi.py
│   └── urls.py
├── chat/
│   ├── models.py
│   ├── consumers.py
│   ├── routing.py
│   ├── views.py
│   ├── serializers.py
│   └── urls.py
└── manage.py
```

---

## Setup

### 1. Clone and install dependencies

```bash
git clone <your-repo-url>
cd chat_app
pip install -r requirements.txt
```

### 2. Run migrations

```bash
python manage.py migrate
```

### 3. Start Redis

```bash
redis-server
```

### 4. Run the server

```bash
python manage.py runserver
```

---

## Data Models

### Room

| Field | Type | Description |
|---|---|---|
| `name` | CharField | Unique room name |

### Messages

| Field | Type | Description |
|---|---|---|
| `content` | JSONField | Message content |
| `username` | CharField | Sender's username |
| `reaction` | CharField | Optional emoji reaction |
| `time_stamp` | DateTimeField | Auto-set on creation |
| `room` | ForeignKey | Room the message belongs to |

---

## REST API

### Create a Room

```
POST /api/rooms/
```

**Request body:**
```json
{
    "name": "general"
}
```

**Response:**
```json
{
    "name": "general"
}
```

---

### Get Active User Count

```
GET /api/rooms/<room_name>/active/
```

**Response:**
```json
{
    "count": 3
}
```

---

## WebSocket API

### Connect

```
ws://localhost:8000/ws/chat/<room_name>/<username>/
```

- If the room does not exist, the server sends an error and closes the connection.
- On successful connect, the server sends the full message history for that room.
- A system message is broadcast to all users in the room announcing the join.

**Error response (room not found):**
```json
{
    "error": "Room does not exist"
}
```

**History response (on connect):**
```json
[
    {
        "content": "Hello",
        "username": "Dev",
        "reaction": null,
        "time_stamp": "2026-05-23T00:27:20.398Z"
    }
]
```

---

### Send a Message

Send a JSON payload after connecting:

```json
{
    "content": "Hello everyone!",
    "reaction": "😎"
}
```

`reaction` is optional.

**Broadcast received by all users in the room:**
```json
{
    "type": "chat_message",
    "username": "Dev",
    "content": "Hello everyone!",
    "reaction": "😎"
}
```

---

### Join Notification

Broadcast to all users when someone connects:

```json
{
    "type": "chat_message",
    "username": "system",
    "content": "Dev has joined the chat"
}
```

---

### Leave Notification

Broadcast to all users when someone disconnects:

```json
{
    "type": "chat_message",
    "username": "system",
    "content": "Dev has left the chat"
}
```

---

## WebSocket Lifecycle

```
Client connects to ws/chat/<room>/<username>/
    → Server validates room exists
    → Server adds client to Redis group
    → Server accepts connection
    → Server broadcasts join notification
    → Server sends message history to client

Client sends a message
    → Server saves message to database
    → Server broadcasts to all clients in the room

Client disconnects
    → Server broadcasts leave notification
    → Server removes client from Redis group
    → Server removes client from active users
```

---

## Active Users

Active users per room are tracked in memory using a Python dictionary. This resets when the server restarts. For persistence across restarts, consider storing presence in the database.
