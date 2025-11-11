import React from 'react';
import './CommandSuggestions.css';

/**
 * CommandSuggestions Component
 * Displays autocomplete dropdown for slash commands
 * 
 * @param {Object} props
 * @param {Array} props.suggestions - Array of command suggestions
 * @param {Function} props.onSelect - Callback when suggestion is selected
 * @param {number} props.selectedIndex - Currently selected suggestion index
 */
const CommandSuggestions = ({ suggestions, onSelect, selectedIndex }) => {
  if (!suggestions || suggestions.length === 0) {
    return null;
  }

  return (
    <div className="command-suggestions">
      <div className="suggestions-header">
        <span className="suggestions-icon">⚡</span>
        Quick Actions
      </div>
      <ul className="suggestions-list">
        {suggestions.map((suggestion, index) => (
          <li
            key={suggestion.command}
            className={`suggestion-item ${index === selectedIndex ? 'selected' : ''}`}
            onClick={() => onSelect(suggestion)}
            onMouseEnter={() => {}} // Could update selected index on hover
          >
            <div className="suggestion-command">{suggestion.display}</div>
            <div className="suggestion-description">{suggestion.description}</div>
          </li>
        ))}
      </ul>
      <div className="suggestions-footer">
        Use <kbd>↑</kbd> <kbd>↓</kbd> to navigate, <kbd>Enter</kbd> to select, <kbd>Esc</kbd> to close
      </div>
    </div>
  );
};

export default CommandSuggestions;

