# Testing Instructions - ConvoSage Chat Interface

## Prerequisites

Before testing, ensure both backend and frontend servers are running:

### 1. Start Backend Server

```bash
cd backend
.\venv\Scripts\activate  # Windows
# or
source venv/bin/activate  # macOS/Linux

uvicorn app.main:app --reload
```

Backend should be available at: `http://localhost:8000`

### 2. Start Frontend Server

```bash
cd frontend
npm run dev
```

Frontend should be available at: `http://localhost:5173`

---

## Manual Test Cases

### Test 1: Basic Chat Functionality ✅

**Steps:**
1. Open `http://localhost:5173` in your browser
2. You should see the ConvoSage chat interface with an empty state
3. Type "Hello!" in the input field
4. Press Enter or click the send button

**Expected Result:**
- Your message appears as a user bubble (right-aligned, purple gradient)
- Bot response appears as a bot bubble (left-aligned, gray background)
- Both messages show timestamps
- Auto-scroll to bottom occurs

---

### Test 2: Calculator Tool Integration ✅

**Steps:**
1. Type "Calculate 25 * 4" in the input
2. Press Enter

**Expected Result:**
- Bot responds with "The result of 25*4 is 100"
- Calculator tool was used (check backend logs)

**Additional Tests:**
- "What is 15 + 5?"
- "Compute (10 * 2) + 5"
- "Calculate 100 / 3"

---

### Test 3: Product Search (RAG) ✅

**Steps:**
1. Type "Show me tumblers" in the input
2. Press Enter

**Expected Result:**
- Bot lists ZUS Coffee tumbler products
- Product names and details are displayed
- RAG system was used (vector search)

**Additional Tests:**
- "Do you have any bottles?"
- "Show me glass products"
- "What products do you sell?"

---

### Test 4: Outlet Search (Text2SQL) ✅

**Steps:**
1. Type "Outlets in Kuala Lumpur" in the input
2. Press Enter

**Expected Result:**
- Bot lists outlets in KL
- Outlet names, addresses shown
- Text2SQL converted query to SQL

**Additional Tests:**
- "Show me outlets with drive-through"
- "Where can I find outlets with WiFi?"
- "Outlets in Selangor with drive-through"
- "How many outlets are there?"

---

### Test 5: Multi-turn Conversation ✅

**Steps:**
1. Type "Hi, my name is Sarah"
2. Press Enter, wait for response
3. Type "What is my name?"
4. Press Enter

**Expected Result:**
- Bot remembers your name from previous message
- Bot responds "Your name is Sarah" (or similar)
- Conversation memory working correctly

**Additional Tests:**
- "I like coffee"
- "What do I like?"

---

### Test 6: Input Features ✅

**Steps:**
1. Type a message in the input field
2. Try Shift+Enter to create a new line
3. Verify character counter updates (bottom right)
4. Type over 2000 characters

**Expected Result:**
- Textarea auto-resizes as you type
- Shift+Enter creates new line (doesn't send)
- Enter sends message
- Character counter shows "X/2000"
- Cannot exceed 2000 characters

---

### Test 7: Loading States ✅

**Steps:**
1. Type a message and send
2. Observe the UI during processing

**Expected Result:**
- Typing indicator appears (animated dots)
- Send button shows loading spinner
- Input field is disabled
- Header status shows "Typing..."
- After response, everything returns to normal

---

### Test 8: Session Persistence ✅

**Steps:**
1. Send a few messages in the chat
2. Refresh the page (F5 or Ctrl+R)

**Expected Result:**
- All previous messages are restored
- Conversation history persists
- Session ID is maintained

---

### Test 9: Clear Conversation ✅

**Steps:**
1. Send some messages
2. Click the trash icon (🗑️) in the header
3. Confirm deletion in the alert

**Expected Result:**
- All messages are cleared
- Empty state is shown again
- New session will be created on next message

---

### Test 10: View Stats ✅

**Steps:**
1. Send a few messages
2. Click the stats icon (📊) in the header

**Expected Result:**
- Stats banner appears at top
- Shows "X sessions, Y messages"
- Banner auto-hides after 5 seconds

---

### Test 11: Error Handling ✅

**Steps:**
1. Stop the backend server
2. Try to send a message

**Expected Result:**
- Error message appears in chat
- Red error banner shows at top
- User is informed of connection issue
- Can dismiss error banner with X button

**Recovery:**
1. Restart backend server
2. Send a message again
3. Should work normally

---

### Test 12: Empty/Invalid Input ✅

**Steps:**
1. Try to send an empty message (just spaces)
2. Try to send only whitespace

**Expected Result:**
- Send button is disabled when input is empty
- Cannot send empty or whitespace-only messages

---

### Test 13: Long Message Handling ✅

**Steps:**
1. Type a very long message (multiple paragraphs)
2. Send it

**Expected Result:**
- Textarea scrolls internally
- Message is sent successfully
- Bot response handles long context
- UI remains responsive

---

### Test 14: Rapid Message Sending ✅

**Steps:**
1. Send multiple messages quickly in succession

**Expected Result:**
- Messages queue properly
- Responses appear in correct order
- No race conditions or UI glitches

---

## Mobile Testing 📱

### Test 15: Mobile Responsiveness

**Steps:**
1. Open the app on a mobile device or use browser DevTools (F12)
2. Switch to mobile view (iPhone, Android)
3. Test all features on mobile

**Expected Result:**
- Full-screen layout on mobile
- Touch-friendly buttons (44px+)
- No horizontal scroll
- Keyboard doesn't obscure input
- No zoom on input focus (iOS)

---

## Browser Compatibility 🌐

Test on multiple browsers:
- ✅ Chrome/Edge (Chromium)
- ✅ Firefox
- ✅ Safari (macOS/iOS)

**Expected Result:**
- UI looks consistent across browsers
- All features work on all platforms

---

## Performance Testing 🚀

### Test 16: Animation Performance

**Steps:**
1. Send many messages (20+)
2. Observe scrolling and animations

**Expected Result:**
- Smooth 60fps animations
- No lag or jank
- Auto-scroll is smooth
- Typing indicator animates smoothly

---

## Quick Test Checklist

Use these quick tests to verify everything works:

```
✅ "Hello" → Bot responds
✅ "Calculate 5 + 3" → Returns 8
✅ "Show me tumblers" → Lists products
✅ "Outlets in KL" → Lists outlets
✅ Page refresh → History persists
✅ Clear button → Clears chat
✅ Stats button → Shows stats
✅ Mobile view → Responsive layout
```

---

## Known Limitations

1. **No Authentication**: Sessions are stored locally
   - Anyone can see the conversation
   - No user accounts

2. **LocalStorage Only**: No server-side persistence
   - Clear browser data = lose history
   - No sync across devices

---

## Reporting Issues

If you find any bugs or issues during testing:

1. **Note the error message** (if any)
2. **Describe the steps** to reproduce
3. **Check browser console** (F12) for errors
4. **Note browser and OS** used
5. **Take a screenshot** if UI issue

---

## Backend API Testing

You can also test the backend API directly:

### Health Check
```bash
curl http://localhost:8000/health
```

### Send Chat Message
```bash
curl -X POST http://localhost:8000/chat/ \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello"}'
```

### Get Stats
```bash
curl http://localhost:8000/chat/stats
```

### API Documentation
Visit: `http://localhost:8000/docs` for interactive API docs

---

## Success Criteria ✅

The chat interface is working correctly if:
- ✅ All 16 test cases pass
- ✅ No console errors in browser DevTools
- ✅ UI is responsive on mobile and desktop
- ✅ Animations are smooth (60fps)
- ✅ Error handling works gracefully
- ✅ Session persistence works
- ✅ All tools integrate properly (calculator, products, outlets)

---

## Additional Resources

- **Frontend README**: `frontend/README.md`
- **Backend API Docs**: `http://localhost:8000/docs`
- **Architecture Docs**: `docs/frontend-architecture.md`

---

**Happy Testing! 🎉**

