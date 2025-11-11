# ConvoSage Frontend

React-based chat interface for the ConvoSage AI chatbot.

## Features

- ✅ **Modern Chat UI** - Beautiful, responsive chat interface
- ✅ **Real-time Messaging** - Send and receive messages instantly
- ✅ **Session Persistence** - Conversation history saved locally
- ✅ **Loading States** - Typing indicators and loading animations
- ✅ **Error Handling** - Graceful error messages and recovery
- ✅ **Auto-scroll** - Automatic scroll to latest messages
- ✅ **Mobile Responsive** - Works on all screen sizes

## Tech Stack

- **React 19** - UI framework
- **Vite** - Build tool and dev server
- **CSS3** - Modern styling with animations
- **LocalStorage** - Client-side session persistence

## Getting Started

### Prerequisites

- Node.js 16+ and npm

### Installation

```bash
# Install dependencies
npm install

# Start development server
npm run dev
```

The frontend will be available at `http://localhost:5173`

### Environment Variables

Create a `.env` file in the frontend directory:

```env
VITE_API_URL=http://localhost:8000
```

## Project Structure

```
frontend/
├── src/
│   ├── components/
│   │   ├── ChatWindow.jsx       # Main chat container
│   │   ├── ChatWindow.css
│   │   ├── MessageList.jsx      # Message list with auto-scroll
│   │   ├── MessageList.css
│   │   ├── MessageBubble.jsx    # Individual message display
│   │   ├── MessageBubble.css
│   │   ├── InputComposer.jsx    # Message input with Enter/Shift+Enter
│   │   └── InputComposer.css
│   ├── App.jsx                  # Root component
│   ├── App.css
│   ├── main.jsx                 # Entry point
│   └── index.css                # Global styles
├── public/
├── .env                         # Environment variables
├── .env.example                 # Example environment variables
├── package.json
└── vite.config.js
```

## Components

### ChatWindow

Main container that orchestrates all chat functionality:
- API integration with backend `/chat` endpoint
- Session management (create, restore, delete)
- Message state management
- Error handling
- Stats display

**Props:** None (stateful component)

### MessageList

Scrollable list of messages with empty state:
- Auto-scroll to latest message
- Typing indicator
- Empty state with capabilities list
- Smooth animations

**Props:**
- `messages` (Array): Array of message objects
- `isLoading` (Boolean): Whether bot is typing

### MessageBubble

Individual message display:
- User/bot differentiation
- Avatars and timestamps
- Styled bubbles
- Animations on entry

**Props:**
- `message` (String): Message text
- `sender` (String): 'user' or 'bot'
- `timestamp` (String): ISO timestamp

### InputComposer

Message input with smart controls:
- Auto-resizing textarea
- Enter to send, Shift+Enter for newline
- Character count (max 2000)
- Disabled during loading
- Send button with loading state

**Props:**
- `onSendMessage` (Function): Callback when message is sent
- `isLoading` (Boolean): Whether bot is responding

## Features in Detail

### Session Management

- Sessions are created automatically on first message
- Session ID is stored in `localStorage`
- Conversations persist across page reloads
- Clear conversation button to delete session

### Message Flow

1. User types message and hits Enter
2. Message appears immediately in UI
3. API request sent to backend
4. Loading indicator shown
5. Bot response displayed when received
6. Auto-scroll to latest message

### Error Handling

- Network errors display inline error message
- Failed messages shown to user
- Retry available by resending
- Connection status in header

### Responsive Design

- **Desktop (769px+)**: Centered card layout with max width
- **Mobile (<768px)**: Full-screen layout
- Touch-friendly buttons and inputs
- No iOS zoom on input focus

## API Integration

The frontend communicates with the backend API:

### POST /chat/
```json
Request:
{
  "message": "Hello!",
  "session_id": "optional-session-id"
}

Response:
{
  "response": "Hi there! How can I help?",
  "session_id": "generated-session-id"
}
```

### GET /chat/history/{session_id}
```json
Response:
{
  "session_id": "...",
  "history": [
    {"input": "Hello", "output": "Hi there!"}
  ]
}
```

### DELETE /chat/session/{session_id}
Deletes a conversation session.

### GET /chat/stats
```json
Response:
{
  "total_sessions": 5,
  "total_messages": 42
}
```

## Keyboard Shortcuts

- `Enter` - Send message
- `Shift + Enter` - New line in message
- Input auto-resizes with content

## Browser Support

- Chrome/Edge 90+
- Firefox 88+
- Safari 14+
- Mobile browsers (iOS Safari, Chrome Mobile)

## Development

### Build for Production

```bash
npm run build
```

Output will be in `dist/` directory.

### Lint

```bash
npm run lint
```

## Day 8 Achievements ✅

- [x] Created 4 reusable React components
- [x] Implemented full chat UI with modern design
- [x] Integrated with backend API
- [x] Added session persistence with localStorage
- [x] Implemented loading states and animations
- [x] Error handling and user feedback
- [x] Mobile-responsive design
- [x] Auto-scroll and typing indicators
- [x] Character counting and input validation
- [x] Stats and conversation management

## Next Steps (Day 9)

- [ ] Quick actions (/calc, /products, /outlets)
- [ ] Command autocomplete
- [ ] Tool activity visualization
- [ ] Enhanced agentic planning visibility
- [ ] Additional UI polish and animations

## License

Part of the Mindhive AI Assessment project.
