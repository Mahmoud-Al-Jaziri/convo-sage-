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
  const isInitialMount = useRef(true);
  const previousMessageCount = useRef(0);

  // Auto-scroll to bottom when new messages arrive
  useEffect(() => {
    if (!containerRef.current) return;
    
    // Only scroll if messages were actually added (not on initial load with persisted messages)
    const messageCountChanged = messages.length !== previousMessageCount.current;
    previousMessageCount.current = messages.length;
    
    if (messageCountChanged || isLoading) {
      // Use setTimeout to ensure DOM is fully rendered
      setTimeout(() => {
        if (containerRef.current) {
          if (isInitialMount.current && messages.length > 0) {
            // On initial load with persisted messages, scroll instantly without animation
            containerRef.current.scrollTop = containerRef.current.scrollHeight;
            isInitialMount.current = false;
          } else if (!isInitialMount.current) {
            // For new messages, smooth scroll
            containerRef.current.scrollTo({
              top: containerRef.current.scrollHeight,
              behavior: 'smooth'
            });
          }
        }
      }, 0);
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

