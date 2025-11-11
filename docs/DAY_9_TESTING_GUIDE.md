# Day 9 Testing Guide - Advanced Features

## 🚀 Getting Started

### Servers Running
- **Backend**: `http://localhost:8000` (should be running in separate window)
- **Frontend**: `http://localhost:5173` (should be running in separate window)

Open your browser to: **`http://localhost:5173`**

---

## 🧪 Test Checklist

### ✅ Test 1: Command Autocomplete

**Steps:**
1. Click in the input field
2. Type `/`
3. Observe the dropdown that appears above the input

**Expected:**
- ✅ Dropdown appears with 5 commands:
  - `/calc` - Perform calculations
  - `/products` - Search products
  - `/outlets` - Find outlets
  - `/reset` - Clear conversation
  - `/help` - Show available commands
- ✅ Each command has icon, name, and description
- ✅ Footer shows keyboard hints

**Try:**
- Type `/c` - should filter to show only `/calc`
- Press `↓` arrow - selection should move down
- Press `↑` arrow - selection should move up
- Press `Esc` - dropdown should close
- Press `Enter` on selected - command should insert into input

---

### ✅ Test 2: Calculator Command

**Steps:**
1. Type `/calc 25 * 4`
2. Press Enter

**Expected:**
- ✅ Message appears: "Calculate 25 * 4"
- ✅ Bot responds: "The result of 25*4 is 100"
- ✅ Tool badge appears below bot message: "🧮 Calculator" (yellow)

---

### ✅ Test 3: Product Search Command

**Steps:**
1. Type `/products tumbler`
2. Press Enter

**Expected:**
- ✅ Message appears: "Show me tumbler"
- ✅ Bot lists tumbler products
- ✅ Tool badge appears: "☕ Product Search" (pink)

---

### ✅ Test 4: Outlet Search Command

**Steps:**
1. Type `/outlets Kuala Lumpur`
2. Press Enter

**Expected:**
- ✅ Message appears: "Find outlets in Kuala Lumpur"
- ✅ Bot lists outlets in KL
- ✅ Tool badge appears: "📍 Outlet Finder" (blue)

---

### ✅ Test 5: Help Command

**Steps:**
1. Type `/help`
2. Press Enter

**Expected:**
- ✅ Bot responds with list of all commands
- ✅ Shows command syntax and descriptions
- ✅ No API call made (instant response)

---

### ✅ Test 6: Reset Command

**Steps:**
1. Send a few messages first
2. Type `/reset`
3. Press Enter

**Expected:**
- ✅ Confirmation dialog: "Clear this conversation?"
- ✅ Click OK
- ✅ All messages disappear
- ✅ Empty state shows again
- ✅ localStorage cleared

---

### ✅ Test 7: Quick Action Buttons

**Steps:**
1. Look at the bar above the input (below messages)
2. Click the "Calculator" button

**Expected:**
- ✅ See 4 buttons: 🧮 Calculator, ☕ Products, 📍 Outlets, ❓ Help
- ✅ Clicking inserts `/calc ` into input
- ✅ Input is focused
- ✅ Autocomplete may trigger

**Try each button:**
- 🧮 Calculator → inserts `/calc `
- ☕ Products → inserts `/products `
- 📍 Outlets → inserts `/outlets `
- ❓ Help → inserts `/help `

---

### ✅ Test 8: Copy Message

**Steps:**
1. Send a message (any message)
2. Hover your mouse over the message

**Expected:**
- ✅ Copy button (📋) appears in top-right of message
- ✅ Click the copy button
- ✅ Message is copied to clipboard
- ✅ Paste (Ctrl+V) somewhere to verify

---

### ✅ Test 9: Tool Badge Detection

**Steps:**
1. Send: "Calculate 5 + 3"
2. Observe bot response

**Expected:**
- ✅ Bot responds with result
- ✅ Yellow "🧮 Calculator" badge appears

**Try:**
1. Send: "Show me bottles"
2. ✅ Pink "☕ Product Search" badge appears

**Try:**
1. Send: "Where are outlets with WiFi?"
2. ✅ Blue "📍 Outlet Finder" badge appears

---

### ✅ Test 10: Message Persistence

**Steps:**
1. Send 3-4 messages
2. Refresh the page (F5)

**Expected:**
- ✅ All messages appear immediately
- ✅ No loading delay
- ✅ Session ID preserved
- ✅ Can continue conversation

---

### ✅ Test 11: UI Polish & Animations

**Observe:**
1. **Send button hover** - Should rotate slightly when hovered
2. **Input focus** - Background should change when focused
3. **Quick actions** - Buttons should slide up in sequence on load
4. **Command dropdown** - Should slide up smoothly
5. **Tool badges** - Should have subtle animations
6. **Copy button** - Should fade in on hover

**Expected:**
- ✅ All animations smooth (60fps)
- ✅ No jank or lag
- ✅ Professional feel

---

### ✅ Test 12: Keyboard Navigation

**Steps:**
1. Type `/`
2. Use keyboard only:
   - `↓` - Move selection down
   - `↑` - Move selection up
   - `Enter` - Select command
   - `Esc` - Close dropdown

**Expected:**
- ✅ Full keyboard control works
- ✅ Selection highlights correctly
- ✅ No need for mouse

---

### ✅ Test 13: Mobile Responsiveness

**Steps:**
1. Open DevTools (F12)
2. Click device toolbar (mobile view)
3. Select iPhone or Android device

**Expected:**
- ✅ Quick actions bar scrollable horizontally
- ✅ Command dropdown fits screen
- ✅ Tool badges visible
- ✅ Copy button still works
- ✅ Touch-friendly buttons

---

## 🎯 Quick Test Script

Run through these quickly:

```
1. Type "/" → Dropdown appears ✅
2. Type "/calc 5+3" → Badge appears ✅
3. Hover message → Copy button ✅
4. Click Calculator quick action → Inserts command ✅
5. Type "/help" → Shows commands ✅
6. Refresh page → Messages persist ✅
```

---

## ⚠️ Common Issues

### Issue 1: Dropdown doesn't appear
- **Check**: Are you typing `/` at the start?
- **Try**: Clear input and type `/` fresh

### Issue 2: Commands don't work
- **Check**: Is backend running at :8000?
- **Try**: Check backend server window for errors

### Issue 3: Copy doesn't work
- **Check**: Browser permissions for clipboard
- **Try**: Use HTTPS or localhost

### Issue 4: Badges don't appear
- **Check**: Did bot respond with result?
- **Note**: Badges auto-detect from response content

---

## 📸 What You Should See

### Command Dropdown
```
┌─────────────────────────────────────┐
│ ⚡ Quick Actions                    │
├─────────────────────────────────────┤
│ /calc                               │
│ Perform calculations - e.g., /calc │
│                                     │
│ /products                           │
│ Search products - e.g., /products  │
├─────────────────────────────────────┤
│ Use ↑↓ to navigate, Enter to select│
└─────────────────────────────────────┘
```

### Tool Badge
```
┌─────────────────────────────────────┐
│ 🤖 ConvoSage      10:30 AM         │
│    The result of 25*4 is 100       │
│    🧮 Calculator                    │
└─────────────────────────────────────┘
```

### Quick Actions
```
┌─────────────────────────────────────┐
│ [🧮 Calculator] [☕ Products]        │
│ [📍 Outlets] [❓ Help]              │
└─────────────────────────────────────┘
```

---

## ✅ Success Criteria

All tests pass if:
- ✅ Command autocomplete works with keyboard
- ✅ All 5 commands work correctly
- ✅ Tool badges appear on appropriate messages
- ✅ Copy functionality works
- ✅ Quick actions insert commands
- ✅ Message persistence works
- ✅ All animations are smooth
- ✅ No console errors
- ✅ Mobile view works

---

## 🐛 Found a Bug?

If something doesn't work:
1. Check browser console (F12) for errors
2. Check backend server window for API errors
3. Try refreshing the page
4. Clear localStorage (in DevTools → Application)
5. Restart both servers

---

## 🎉 When Testing is Complete

If all tests pass:
- Day 9 features are working perfectly! ✅
- Ready to commit
- Ready for Day 10 (final polish & deployment)

**Time to commit?** Let me know when you're ready! 🚀

