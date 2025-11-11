import React, { useState, useRef, useEffect } from 'react';
import './InputComposer.css';

/**
 * InputComposer Component
 * Input field for composing and sending messages
 * 
 * Features:
 * - Enter to send, Shift+Enter for new line
 * - Auto-resize textarea
 * - Disabled during loading
 * - Clear on send
 * 
 * @param {Object} props
 * @param {Function} props.onSendMessage - Callback when message is sent
 * @param {boolean} props.isLoading - Whether bot is responding
 */
const InputComposer = ({ onSendMessage, isLoading }) => {
  const [message, setMessage] = useState('');
  const textareaRef = useRef(null);

  // Auto-resize textarea
  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
      textareaRef.current.style.height = `${textareaRef.current.scrollHeight}px`;
    }
  }, [message]);

  const handleSubmit = (e) => {
    e.preventDefault();
    
    const trimmedMessage = message.trim();
    if (!trimmedMessage || isLoading) return;
    
    onSendMessage(trimmedMessage);
    setMessage('');
    
    // Reset textarea height
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
    }
  };

  const handleKeyDown = (e) => {
    // Enter without Shift = send
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  const handleChange = (e) => {
    setMessage(e.target.value);
  };

  return (
    <form className="input-composer" onSubmit={handleSubmit}>
      <div className="input-container">
        <textarea
          ref={textareaRef}
          className="message-input"
          placeholder={isLoading ? "Bot is typing..." : "Type a message... (Enter to send, Shift+Enter for new line)"}
          value={message}
          onChange={handleChange}
          onKeyDown={handleKeyDown}
          disabled={isLoading}
          rows={1}
          maxLength={2000}
        />
        <button
          type="submit"
          className="send-button"
          disabled={!message.trim() || isLoading}
          aria-label="Send message"
        >
          {isLoading ? (
            <span className="loading-spinner">⏳</span>
          ) : (
            <svg 
              width="24" 
              height="24" 
              viewBox="0 0 24 24" 
              fill="none" 
              stroke="currentColor" 
              strokeWidth="2" 
              strokeLinecap="round" 
              strokeLinejoin="round"
            >
              <line x1="22" y1="2" x2="11" y2="13"></line>
              <polygon points="22 2 15 22 11 13 2 9 22 2"></polygon>
            </svg>
          )}
        </button>
      </div>
      <div className="input-hints">
        <span className="character-count">
          {message.length}/2000
        </span>
        <span className="input-tip">
          💡 Try: "Calculate 25 * 4" or "Show me tumblers" or "Outlets in KL"
        </span>
      </div>
    </form>
  );
};

export default InputComposer;

