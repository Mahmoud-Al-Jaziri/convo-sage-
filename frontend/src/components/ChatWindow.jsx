import React, { useState, useEffect, useRef } from 'react';
import MessageList from './MessageList';
import InputComposer from './InputComposer';
import QuickActions from './QuickActions';
import './ChatWindow.css';
import { parseCommand, commandToMessage, getHelpMessage } from '../utils/commandParser';

/**
 * ChatWindow Component
 * Main chat interface that integrates all components
 * 
 * Features:
 * - Message history display
 * - Send/receive messages
 * - API integration
 * - Session management
 * - Error handling
 * - Command parsing
 * - Message persistence
 */
const ChatWindow = () => {
  const [messages, setMessages] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [sessionId, setSessionId] = useState(null);
  const [error, setError] = useState(null);
  const [stats, setStats] = useState(null);

  const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

  // Initialize session on mount
  useEffect(() => {
    // Prevent any scrolling during load
    document.body.style.overflow = 'hidden';
    document.documentElement.style.overflow = 'hidden';
    
    // Check if there's a saved session
    const savedSessionId = localStorage.getItem('chatSessionId');
    const savedMessages = localStorage.getItem('chatMessages');
    
    if (savedSessionId) {
      setSessionId(savedSessionId);
      // Try to load from localStorage first (faster)
      if (savedMessages) {
        try {
          setMessages(JSON.parse(savedMessages));
        } catch (e) {
          console.error('Failed to parse saved messages:', e);
        }
      }
      // Then load from backend (for sync) but don't override UI state
      loadHistory(savedSessionId);
    }
  }, []);
  
  // Save messages to localStorage whenever they change
  useEffect(() => {
    if (messages.length > 0) {
      localStorage.setItem('chatMessages', JSON.stringify(messages));
    }
  }, [messages]);

  // Load conversation history
  const loadHistory = async (sid) => {
    try {
      const response = await fetch(`${API_BASE_URL}/chat/history/${sid}`);
      if (response.ok) {
        const data = await response.json();
        if (data.history && data.history.length > 0) {
          // Only update if we don't already have messages from localStorage
          setMessages((prevMessages) => {
            // If we already have messages, don't overwrite them
            if (prevMessages.length > 0) {
              return prevMessages;
            }
            // Convert history format to message format
            const historyMessages = [];
            data.history.forEach((turn) => {
              historyMessages.push({
                message: turn.input,
                sender: 'user',
                timestamp: new Date().toISOString()
              });
              historyMessages.push({
                message: turn.output,
                sender: 'bot',
                timestamp: new Date().toISOString()
              });
            });
            return historyMessages;
          });
        }
      }
    } catch (error) {
      console.error('Failed to load history:', error);
    }
  };

  // Send message to backend
  const handleSendMessage = async (messageText) => {
    // Clear error
    setError(null);
    
    // Handle special commands
    const parsed = parseCommand(messageText);
    if (parsed) {
      if (parsed.command === 'reset' || parsed.command === 'clear') {
        // Handle reset command
        handleClearChat();
        return;
      }
      
      if (parsed.command === 'help') {
        // Show help message
        const userMessage = {
          message: messageText,
          sender: 'user',
          timestamp: new Date().toISOString()
        };
        const helpMessage = {
          message: getHelpMessage(),
          sender: 'bot',
          timestamp: new Date().toISOString()
        };
        setMessages(prev => [...prev, userMessage, helpMessage]);
        return;
      }
      
      // Convert command to natural language
      const naturalMessage = commandToMessage(parsed.command, parsed.args);
      if (naturalMessage) {
        messageText = naturalMessage;
      }
    }

    // Add user message to UI immediately
    const userMessage = {
      message: messageText,
      sender: 'user',
      timestamp: new Date().toISOString()
    };
    setMessages(prev => [...prev, userMessage]);

    // Set loading state
    setIsLoading(true);

    try {
      // Call chat API
      const response = await fetch(`${API_BASE_URL}/chat/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message: messageText,
          session_id: sessionId
        })
      });

      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      }

      const data = await response.json();

      // Save session ID if it's the first message
      if (!sessionId && data.session_id) {
        setSessionId(data.session_id);
        localStorage.setItem('chatSessionId', data.session_id);
      }

      // Add bot response to UI
      const botMessage = {
        message: data.response,
        sender: 'bot',
        timestamp: new Date().toISOString()
      };
      setMessages(prev => [...prev, botMessage]);

    } catch (error) {
      console.error('Error sending message:', error);
      setError(error.message || 'Failed to send message. Please try again.');
      
      // Add error message to UI
      const errorMessage = {
        message: `❌ Error: ${error.message || 'Failed to connect to server. Please try again.'}`,
        sender: 'bot',
        timestamp: new Date().toISOString()
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  // Clear conversation
  const handleClearChat = async () => {
    if (!window.confirm('Clear this conversation?')) return;

    try {
      if (sessionId) {
        await fetch(`${API_BASE_URL}/chat/session/${sessionId}`, {
          method: 'DELETE'
        });
      }
      
      // Clear UI and storage
      setMessages([]);
      setSessionId(null);
      setError(null);
      localStorage.removeItem('chatSessionId');
      localStorage.removeItem('chatMessages');
    } catch (error) {
      console.error('Error clearing chat:', error);
    }
  };

  // Get conversation stats
  const handleGetStats = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/chat/stats`);
      if (response.ok) {
        const data = await response.json();
        setStats(data);
        setTimeout(() => setStats(null), 5000); // Hide after 5 seconds
      }
    } catch (error) {
      console.error('Error fetching stats:', error);
    }
  };

  return (
    <div className="chat-window">
      {/* Header */}
      <div className="chat-header">
        <div className="header-left">
          <div className="bot-avatar">🤖</div>
          <div className="header-info">
            <h2>ConvoSage</h2>
            <p className="status">
              {isLoading ? 'Typing...' : 'Online'}
            </p>
          </div>
        </div>
        <div className="header-actions">
          <button
            className="icon-button"
            onClick={handleGetStats}
            title="View stats"
            aria-label="View statistics"
          >
            📊
          </button>
          <button
            className="icon-button"
            onClick={handleClearChat}
            title="Clear chat"
            aria-label="Clear conversation"
          >
            🗑️
          </button>
        </div>
      </div>

      {/* Stats Display */}
      {stats && (
        <div className="stats-banner">
          <strong>Stats:</strong> {stats.total_sessions} sessions, {stats.total_messages} messages
        </div>
      )}

      {/* Error Display */}
      {error && (
        <div className="error-banner">
          <strong>⚠️ Connection Error:</strong> {error}
          <button onClick={() => setError(null)}>✕</button>
        </div>
      )}

      {/* Messages */}
      <MessageList messages={messages} isLoading={isLoading} />

      {/* Quick Actions */}
      <QuickActions onActionClick={(command) => {
        // Trigger input focus with command (would need to pass ref or callback)
        // For now, just send the command
        const textarea = document.querySelector('.message-input');
        if (textarea) {
          textarea.value = command;
          textarea.focus();
          // Trigger change event
          const event = new Event('input', { bubbles: true });
          textarea.dispatchEvent(event);
        }
      }} />

      {/* Input */}
      <InputComposer onSendMessage={handleSendMessage} isLoading={isLoading} />
    </div>
  );
};

export default ChatWindow;

