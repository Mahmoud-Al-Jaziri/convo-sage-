import React from 'react';
import './MessageBubble.css';

/**
 * MessageBubble Component
 * Displays a single message from either the user or the bot
 * 
 * @param {Object} props
 * @param {string} props.message - The message text
 * @param {string} props.sender - 'user' or 'bot'
 * @param {string} props.timestamp - ISO timestamp string
 */
const MessageBubble = ({ message, sender, timestamp }) => {
  const isUser = sender === 'user';
  
  // Format timestamp
  const formatTime = (isoString) => {
    const date = new Date(isoString);
    return date.toLocaleTimeString('en-US', { 
      hour: '2-digit', 
      minute: '2-digit' 
    });
  };

  return (
    <div className={`message-bubble ${isUser ? 'user' : 'bot'}`}>
      <div className="message-avatar">
        {isUser ? '👤' : '🤖'}
      </div>
      <div className="message-content">
        <div className="message-header">
          <span className="message-sender">
            {isUser ? 'You' : 'ConvoSage'}
          </span>
          <span className="message-time">
            {formatTime(timestamp)}
          </span>
        </div>
        <div className="message-text">
          {message}
        </div>
      </div>
    </div>
  );
};

export default MessageBubble;

