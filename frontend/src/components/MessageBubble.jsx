import React, { useState } from 'react';
import './MessageBubble.css';
import ToolBadge from './ToolBadge';
import { detectToolUsed } from '../utils/commandParser';

/**
 * MessageBubble Component
 * Displays a single message from either the user or the bot
 * 
 * @param {Object} props
 * @param {string} props.message - The message text
 * @param {string} props.sender - 'user' or 'bot'
 * @param {string} props.timestamp - ISO timestamp string
 * @param {string} props.tool - Tool used (optional)
 */
const MessageBubble = ({ message, sender, timestamp, tool }) => {
  const isUser = sender === 'user';
  const [showCopyButton, setShowCopyButton] = useState(false);
  
  // Detect tool if not provided
  const detectedTool = tool || (!isUser ? detectToolUsed(message) : null);
  
  // Format timestamp
  const formatTime = (isoString) => {
    const date = new Date(isoString);
    return date.toLocaleTimeString('en-US', { 
      hour: '2-digit', 
      minute: '2-digit' 
    });
  };
  
  // Copy message to clipboard
  const handleCopy = () => {
    navigator.clipboard.writeText(message);
    // Could add a toast notification here
  };
  
  // Format message with better structure
  const formatMessage = (text) => {
    if (!text) return null;
    
    // Split by lines
    const lines = text.split('\n');
    
    return lines.map((line, index) => {
      // Numbered list (e.g., "1. Item")
      if (/^\d+\.\s/.test(line)) {
        return (
          <div key={index} className="message-list-item">
            {line}
          </div>
        );
      }
      
      // Bullet points (e.g., "• Item" or "- Item")
      if (/^[•\-]\s/.test(line)) {
        return (
          <div key={index} className="message-bullet-item">
            {line}
          </div>
        );
      }
      
      // Bold text (e.g., "**text**")
      if (line.includes('**')) {
        const parts = line.split(/\*\*(.*?)\*\*/g);
        return (
          <p key={index} className="message-paragraph">
            {parts.map((part, i) => 
              i % 2 === 1 ? <strong key={i}>{part}</strong> : part
            )}
          </p>
        );
      }
      
      // Headers (lines ending with ":")
      if (line.trim().endsWith(':') && line.length < 50) {
        return (
          <div key={index} className="message-header-text">
            {line}
          </div>
        );
      }
      
      // Empty lines
      if (line.trim() === '') {
        return <br key={index} />;
      }
      
      // Regular paragraphs
      return (
        <p key={index} className="message-paragraph">
          {line}
        </p>
      );
    });
  };

  return (
    <div 
      className={`message-bubble ${isUser ? 'user' : 'bot'}`}
      onMouseEnter={() => setShowCopyButton(true)}
      onMouseLeave={() => setShowCopyButton(false)}
    >
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
          {isUser ? message : formatMessage(message)}
          {showCopyButton && (
            <button 
              className="copy-button" 
              onClick={handleCopy}
              title="Copy message"
            >
              📋
            </button>
          )}
        </div>
        {detectedTool && !isUser && (
          <ToolBadge tool={detectedTool} />
        )}
      </div>
    </div>
  );
};

export default MessageBubble;

