import React, { useEffect, useRef } from 'react';
import MessageBubble from './MessageBubble';
import './MessageList.css';

/**
 * MessageList Component
 * Displays a scrollable list of messages with auto-scroll
 * 
 * @param {Object} props
 * @param {Array} props.messages - Array of message objects
 * @param {boolean} props.isLoading - Whether the bot is typing
 */
const MessageList = ({ messages, isLoading }) => {
  const messagesEndRef = useRef(null);
  const containerRef = useRef(null);

  // Auto-scroll to bottom when new messages arrive
  useEffect(() => {
    if (messagesEndRef.current) {
      messagesEndRef.current.scrollIntoView({ 
        behavior: 'smooth',
        block: 'end'
      });
    }
  }, [messages, isLoading]);

  return (
    <div className="message-list" ref={containerRef}>
      {messages.length === 0 ? (
        <div className="empty-state">
          <div className="empty-icon">💬</div>
          <h3>Start a conversation</h3>
          <p>Ask me anything! I can help with:</p>
          <ul className="capabilities-list">
            <li>💬 General conversation</li>
            <li>🧮 Math calculations</li>
            <li>☕ ZUS Coffee products</li>
            <li>📍 Store locations & info</li>
          </ul>
        </div>
      ) : (
        <>
          {messages.map((msg, index) => (
            <MessageBubble
              key={index}
              message={msg.message}
              sender={msg.sender}
              timestamp={msg.timestamp}
            />
          ))}
          
          {isLoading && (
            <div className="typing-indicator">
              <div className="message-avatar">🤖</div>
              <div className="typing-dots">
                <span></span>
                <span></span>
                <span></span>
              </div>
            </div>
          )}
          
          <div ref={messagesEndRef} />
        </>
      )}
    </div>
  );
};

export default MessageList;

