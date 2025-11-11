/**
 * Command Parser for Quick Actions
 * Parses user input for slash commands like /calc, /products, /outlets
 */

export const COMMANDS = {
  CALC: 'calc',
  CALCULATE: 'calculate',
  PRODUCTS: 'products',
  PRODUCT: 'product',
  OUTLETS: 'outlets',
  OUTLET: 'outlet',
  LOCATIONS: 'locations',
  RESET: 'reset',
  CLEAR: 'clear',
  HELP: 'help'
};

export const COMMAND_DESCRIPTIONS = {
  [COMMANDS.CALC]: 'Perform calculations - e.g., /calc 25 * 4',
  [COMMANDS.PRODUCTS]: 'Search products - e.g., /products tumbler',
  [COMMANDS.OUTLETS]: 'Find outlets - e.g., /outlets Kuala Lumpur',
  [COMMANDS.RESET]: 'Clear conversation history',
  [COMMANDS.HELP]: 'Show available commands'
};

/**
 * Check if a message starts with a command
 * @param {string} message - User input message
 * @returns {boolean}
 */
export const isCommand = (message) => {
  if (!message) return false;
  const trimmed = message.trim();
  return trimmed.startsWith('/');
};

/**
 * Parse command from message
 * @param {string} message - User input message
 * @returns {Object|null} - {command: string, args: string} or null
 */
export const parseCommand = (message) => {
  if (!isCommand(message)) return null;

  const trimmed = message.trim();
  const parts = trimmed.slice(1).split(/\s+/); // Remove '/' and split by whitespace
  
  if (parts.length === 0) return null;

  const command = parts[0].toLowerCase();
  const args = parts.slice(1).join(' ');

  return {
    command,
    args: args || ''
  };
};

/**
 * Get command suggestions based on partial input
 * @param {string} input - Partial command input
 * @returns {Array} - Array of matching commands with descriptions
 */
export const getCommandSuggestions = (input) => {
  if (!input || !input.startsWith('/')) return [];

  const partial = input.slice(1).toLowerCase();
  if (partial === '') {
    // Show all commands
    return Object.keys(COMMAND_DESCRIPTIONS).map(cmd => ({
      command: cmd,
      description: COMMAND_DESCRIPTIONS[cmd],
      display: `/${cmd}`
    }));
  }

  // Filter commands that start with partial input
  return Object.keys(COMMAND_DESCRIPTIONS)
    .filter(cmd => cmd.startsWith(partial))
    .map(cmd => ({
      command: cmd,
      description: COMMAND_DESCRIPTIONS[cmd],
      display: `/${cmd}`
    }));
};

/**
 * Convert command to natural language message for backend
 * @param {string} command - Command name
 * @param {string} args - Command arguments
 * @returns {string} - Natural language message
 */
export const commandToMessage = (command, args) => {
  switch (command) {
    case COMMANDS.CALC:
    case COMMANDS.CALCULATE:
      return args ? `Calculate ${args}` : 'Please provide a calculation';
    
    case COMMANDS.PRODUCTS:
    case COMMANDS.PRODUCT:
      return args ? `Show me ${args}` : 'Show me all products';
    
    case COMMANDS.OUTLETS:
    case COMMANDS.OUTLET:
    case COMMANDS.LOCATIONS:
      return args ? `Find outlets in ${args}` : 'Show me all outlets';
    
    case COMMANDS.HELP:
      return getHelpMessage();
    
    default:
      return null; // Unknown command
  }
};

/**
 * Get help message with all available commands
 * @returns {string}
 */
export const getHelpMessage = () => {
  const commands = Object.keys(COMMAND_DESCRIPTIONS)
    .map(cmd => `• /${cmd} - ${COMMAND_DESCRIPTIONS[cmd]}`)
    .join('\n');
  
  return `Available commands:\n${commands}`;
};

/**
 * Detect tool from message response
 * @param {string} message - Bot response message
 * @returns {string|null} - Tool name or null
 */
export const detectToolUsed = (message) => {
  const lowerMessage = message.toLowerCase();
  
  if (lowerMessage.includes('result') && lowerMessage.match(/\d+/)) {
    return 'calculator';
  }
  
  if (lowerMessage.includes('product') || lowerMessage.includes('tumbler') || 
      lowerMessage.includes('bottle') || lowerMessage.includes('glass')) {
    return 'products';
  }
  
  if (lowerMessage.includes('outlet') || lowerMessage.includes('location') || 
      lowerMessage.includes('address') || lowerMessage.includes('drive-through')) {
    return 'outlets';
  }
  
  return null;
};

/**
 * Get tool icon emoji
 * @param {string} tool - Tool name
 * @returns {string} - Emoji
 */
export const getToolIcon = (tool) => {
  switch (tool) {
    case 'calculator':
      return '🧮';
    case 'products':
      return '☕';
    case 'outlets':
      return '📍';
    default:
      return '💬';
  }
};

/**
 * Get tool display name
 * @param {string} tool - Tool name
 * @returns {string}
 */
export const getToolName = (tool) => {
  switch (tool) {
    case 'calculator':
      return 'Calculator';
    case 'products':
      return 'Product Search';
    case 'outlets':
      return 'Outlet Finder';
    default:
      return 'Conversation';
  }
};

