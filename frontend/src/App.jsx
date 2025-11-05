import './App.css'

function App() {
  return (
    <div className="app">
      <header className="app-header">
        <h1>ConvoSage</h1>
        <p className="subtitle">AI Chatbot with Agentic Planning</p>
      </header>
      
      <main className="app-main">
        <div className="status-card">
          <h2>✅ Frontend Running</h2>
          <p>React + Vite development server is live</p>
          <p className="info">Ready to build the chat interface on Day 8</p>
        </div>
        
        <div className="status-card">
          <h3>Backend Status</h3>
          <p>Backend API: <code>http://localhost:8000</code></p>
          <p>Health Check: <code>http://localhost:8000/health</code></p>
          <p>API Docs: <code>http://localhost:8000/docs</code></p>
        </div>
        
        <div className="next-steps">
          <h3>Next Steps (Day 2)</h3>
          <ul>
            <li>Implement LangChain conversation memory</li>
            <li>Create /chat endpoint</li>
            <li>Add multi-turn conversation tracking</li>
          </ul>
        </div>
      </main>
      
      <footer className="app-footer">
        <p>Day 1 Complete 🎉 | 10-Day Milestone Plan</p>
      </footer>
    </div>
  )
}

export default App
