import React from 'react';
import './QuickActions.css';

/**
 * QuickActions Component
 * Displays quick action buttons for common commands
 * 
 * @param {Object} props
 * @param {Function} props.onActionClick - Callback when an action is clicked
 */
const QuickActions = ({ onActionClick }) => {
  const actions = [
    { icon: '🧮', label: 'Calculator', command: '/calc' },
    { icon: '☕', label: 'Products', command: '/products' },
    { icon: '📍', label: 'Outlets', command: '/outlets' },
    { icon: '❓', label: 'Help', command: '/help' }
  ];

  return (
    <div className="quick-actions">
      {actions.map((action) => (
        <button
          key={action.command}
          className="quick-action-btn"
          onClick={() => onActionClick(action.command + ' ')}
          title={`${action.label} - ${action.command}`}
        >
          <span className="action-icon">{action.icon}</span>
          <span className="action-label">{action.label}</span>
        </button>
      ))}
    </div>
  );
};

export default QuickActions;

