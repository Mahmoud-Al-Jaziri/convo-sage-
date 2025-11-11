import React from 'react';
import './ToolBadge.css';
import { getToolIcon, getToolName } from '../utils/commandParser';

/**
 * ToolBadge Component
 * Displays a badge indicating which tool was used for a message
 * 
 * @param {Object} props
 * @param {string} props.tool - Tool name (calculator, products, outlets)
 * @param {boolean} props.isActive - Whether the tool is currently active
 */
const ToolBadge = ({ tool, isActive }) => {
  if (!tool || tool === 'conversation') return null;

  const icon = getToolIcon(tool);
  const name = getToolName(tool);

  return (
    <div className={`tool-badge ${isActive ? 'active' : ''} tool-${tool}`}>
      <span className="tool-icon">{icon}</span>
      <span className="tool-name">{name}</span>
      {isActive && <span className="tool-pulse"></span>}
    </div>
  );
};

export default ToolBadge;

