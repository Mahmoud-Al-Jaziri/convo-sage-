# Frontend Architecture

## Overview

The ConvoSage frontend is built with **React 19** and **Vite**, providing a modern, responsive chat interface for interacting with the AI chatbot backend.

## Technology Stack

| Technology | Version | Purpose |
|------------|---------|---------|
| React | 19.1.1 | UI framework |
| Vite | 7.1.7 | Build tool & dev server |
| CSS3 | - | Styling & animations |
| LocalStorage | - | Session persistence |

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                         App.jsx                             │
│                    (Root Component)                         │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                     ChatWindow.jsx                          │
│  - API Integration                                          │
│  - Session Management                                       │
│  - State Management                                         │
│  - Error Handling                                           │
└───┬─────────────────────────────────────────────────────┬───┘
    │                                                     │
    ▼                                                     ▼
┌────────────────────────────┐          ┌────────────────────────────┐
│    MessageList.jsx         │          │   InputComposer.jsx        │
│  - Display messages        │          │  - Message input           │
│  - Auto-scroll             │          │  - Enter to send           │
│  - Typing indicator        │          │  - Character count         │
│  - Empty state             │          │  - Loading state           │
└───┬────────────────────────┘          └────────────────────────────┘
    │
    ▼
┌────────────────────────────┐
│   MessageBubble.jsx        │
│  - User/bot messages       │
│  - Avatars & timestamps    │
│  - Animations              │
└────────────────────────────┘
```

## Component Hierarchy

```
App
└── ChatWindow
    ├── Header (inline)
    │   ├── Bot Avatar
    │   ├── Status Indicator
    │   └── Action Buttons (Stats, Clear)
    ├── Stats Banner (conditional)
    ├── Error Banner (conditional)
    ├── MessageList
    │   ├── Empty State (if no messages)
    │   ├── MessageBubble (per message)
    │   │   ├── Avatar
    │   │   └── Message Content
    │   └── Typing Indicator (if loading)
    └── InputComposer
        ├── Textarea
        ├── Send Button
        └── Hints/Counter
```

## Component Details

### App.jsx
**Purpose:** Root component that renders the ChatWindow  
**State:** None  
**Props:** None  
**Styling:** Minimal container styling

### ChatWindow.jsx
**Purpose:** Main orchestration component  
**State:**
- `messages` (Array): Current conversation messages
- `isLoading` (Boolean): Bot response in progress
- `sessionId` (String): Current session ID
- `error` (String): Error message if any
- `stats` (Object): Session statistics

**Key Functions:**
- `handleSendMessage(text)`: Send message to backend
- `loadHistory(sessionId)`: Load conversation history
- `handleClearChat()`: Delete current session
- `handleGetStats()`: Fetch and display stats

**API Integration:**
- POST `/chat/` - Send messages
- GET `/chat/history/{id}` - Load history
- DELETE `/chat/session/{id}` - Clear session
- GET `/chat/stats` - Get statistics

### MessageList.jsx
**Purpose:** Display scrollable list of messages  
**Props:**
- `messages` (Array): Message objects to display
- `isLoading` (Boolean): Show typing indicator

**Features:**
- Auto-scroll to bottom on new messages
- Empty state with capability hints
- Typing indicator animation
- Custom scrollbar styling

### MessageBubble.jsx
**Purpose:** Render individual message  
**Props:**
- `message` (String): Message text
- `sender` (String): 'user' or 'bot'
- `timestamp` (String): ISO timestamp

**Features:**
- Different styling for user vs bot
- Avatar display (👤 / 🤖)
- Formatted timestamp
- Slide-in animation

### InputComposer.jsx
**Purpose:** Message input with smart controls  
**Props:**
- `onSendMessage` (Function): Callback to send message
- `isLoading` (Boolean): Disable during loading

**Features:**
- Auto-resizing textarea
- Enter to send, Shift+Enter for newline
- Character counter (max 2000)
- Send button with loading state
- Input hints and tips

## State Management

### Local State (useState)

Each component manages its own local state:

```javascript
// ChatWindow
const [messages, setMessages] = useState([]);
const [isLoading, setIsLoading] = useState(false);
const [sessionId, setSessionId] = useState(null);
const [error, setError] = useState(null);
const [stats, setStats] = useState(null);

// InputComposer
const [message, setMessage] = useState('');
```

### Persistent State (localStorage)

```javascript
// Save session ID
localStorage.setItem('chatSessionId', sessionId);

// Retrieve session ID
const savedSessionId = localStorage.getItem('chatSessionId');

// Clear session
localStorage.removeItem('chatSessionId');
```

### Props Flow

```
ChatWindow (manages state)
    ↓ messages, isLoading
MessageList
    ↓ message, sender, timestamp
MessageBubble

ChatWindow
    ↓ onSendMessage, isLoading
InputComposer
```

## Data Flow

### Sending a Message

```
1. User types in InputComposer
2. User presses Enter
3. InputComposer calls onSendMessage()
4. ChatWindow receives message
5. ChatWindow adds message to state (optimistic UI)
6. ChatWindow calls API
7. API responds with bot message
8. ChatWindow adds bot message to state
9. MessageList re-renders with new messages
10. Auto-scroll to bottom
```

### Loading Conversation History

```
1. ChatWindow mounts
2. Check localStorage for sessionId
3. If found, call loadHistory(sessionId)
4. API returns conversation history
5. Convert history format to message format
6. setMessages() with history
7. MessageList renders all messages
```

## API Integration

### Configuration

```javascript
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';
```

### Request Format

```javascript
// Send Message
const response = await fetch(`${API_BASE_URL}/chat/`, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    message: messageText,
    session_id: sessionId
  })
});
```

### Error Handling

```javascript
try {
  // API call
} catch (error) {
  console.error('Error:', error);
  setError(error.message);
  
  // Show error message in chat
  const errorMessage = {
    message: `❌ Error: ${error.message}`,
    sender: 'bot',
    timestamp: new Date().toISOString()
  };
  setMessages(prev => [...prev, errorMessage]);
}
```

## Styling Architecture

### File Organization

Each component has its own CSS file:
```
MessageBubble.jsx → MessageBubble.css
MessageList.jsx → MessageList.css
InputComposer.jsx → InputComposer.css
ChatWindow.jsx → ChatWindow.css
```

### Global Styles (index.css)

```css
* { margin: 0; padding: 0; box-sizing: border-box; }
:root { /* Font and color definitions */ }
body { /* Base body styles */ }
#root { /* App container styles */ }
```

### Component Styles

Each component uses:
1. **BEM-like naming** - `.component-element`
2. **Scoped styles** - Component-specific classes
3. **Responsive design** - Mobile-first approach
4. **CSS Variables** - For consistent theming

### Color Palette

```css
/* Primary Gradient */
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);

/* User Messages */
background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);

/* Bot Messages */
background: #f5f5f5;

/* Backgrounds */
background: #f8f9fa; /* Light gray */
background: #ffffff; /* White */

/* Text */
color: #333; /* Primary text */
color: #666; /* Secondary text */
color: #999; /* Tertiary text */
```

### Animations

```css
/* Slide In */
@keyframes slideIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

/* Float */
@keyframes float {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-10px); }
}

/* Typing Dots */
@keyframes typing {
  0%, 60%, 100% { transform: translateY(0); opacity: 0.7; }
  30% { transform: translateY(-10px); opacity: 1; }
}

/* Pulse */
@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}
```

## Responsive Design

### Breakpoints

```css
/* Mobile First */
@media (max-width: 768px) {
  /* Mobile styles */
}

/* Desktop */
@media (min-width: 769px) {
  /* Desktop styles */
  .chat-window {
    max-width: 900px;
    margin: 20px auto;
    border-radius: 16px;
  }
}
```

### Mobile Optimizations

1. **Touch Targets** - Minimum 44px for buttons
2. **Font Sizing** - 16px to prevent iOS zoom
3. **Full Screen** - No margins on mobile
4. **Scrolling** - Optimized for touch
5. **Gestures** - Native scroll behavior

## Performance Optimizations

### React Best Practices

1. **Functional Components** - Use hooks instead of classes
2. **Minimal Re-renders** - Proper state management
3. **useEffect Dependencies** - Correct dependency arrays
4. **Refs for DOM** - Avoid direct DOM manipulation

### CSS Optimizations

1. **GPU Acceleration** - Use `transform` for animations
2. **Will-change** - Hint browser about animations
3. **Avoid Layout Thrashing** - Batch DOM reads/writes
4. **Efficient Selectors** - Use classes over complex selectors

### Bundle Optimization

1. **Tree Shaking** - Vite automatically removes unused code
2. **Code Splitting** - Dynamic imports for routes (future)
3. **Asset Optimization** - Compress images and fonts
4. **Lazy Loading** - Load components on demand (future)

## Security Considerations

### XSS Prevention

- React automatically escapes HTML in JSX
- Never use `dangerouslySetInnerHTML` without sanitization
- Validate all user input before display

### API Security

- Use environment variables for API URLs
- CORS properly configured on backend
- No sensitive data in localStorage
- Session IDs are opaque tokens

### Data Privacy

- No personal data stored in localStorage
- Session data can be cleared by user
- No tracking or analytics (yet)

## Testing Strategy

### Manual Testing

- [x] Component rendering
- [x] User interactions
- [x] API integration
- [x] Error handling
- [x] Responsive design
- [x] Browser compatibility


## Build & Deployment

### Development

```bash
npm run dev
# Starts Vite dev server at http://localhost:5173
```

### Production Build

```bash
npm run build
# Output: dist/ directory
# - Minified JS/CSS
# - Optimized assets
# - Source maps
```

### Environment Variables

```bash
# .env
VITE_API_URL=http://localhost:8000

# .env.production
VITE_API_URL=https://api.convosage.com
```

### Deployment Targets

- **Vercel** - Recommended for Vite apps
- **Netlify** - Good alternative
- **GitHub Pages** - Simple static hosting
- **AWS S3 + CloudFront** - Enterprise solution

## Conclusion

The frontend architecture is designed to be:
- **Modular** - Easy to extend with new components
- **Maintainable** - Clear structure and naming
- **Performant** - Optimized for speed
- **Responsive** - Works on all devices
- **User-friendly** - Intuitive and accessible

The component-based architecture allows for easy testing, modification, and extension.

