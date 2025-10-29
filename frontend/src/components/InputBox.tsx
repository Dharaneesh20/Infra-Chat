import React, { useState, useRef, useEffect } from 'react';
import './InputBox.css';

interface InputBoxProps {
  onSendMessage: (message: string) => void;
  disabled?: boolean;
}

const InputBox: React.FC<InputBoxProps> = ({ onSendMessage, disabled = false }) => {
  const [input, setInput] = useState('');
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  // Auto-resize textarea
  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
      textareaRef.current.style.height = `${textareaRef.current.scrollHeight}px`;
    }
  }, [input]);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    
    if (input.trim() && !disabled) {
      onSendMessage(input);
      setInput('');
      
      // Reset textarea height
      if (textareaRef.current) {
        textareaRef.current.style.height = 'auto';
      }
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    // Send on Enter (but allow Shift+Enter for new line)
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  const quickPrompts = [
    "List my EC2 instances",
    "Show deployment guide",
    "Troubleshooting steps",
  ];

  const handleQuickPrompt = (prompt: string) => {
    if (!disabled) {
      onSendMessage(prompt);
    }
  };

  return (
    <div className="input-box-container">
      <div className="quick-prompts">
        {quickPrompts.map((prompt, index) => (
          <button
            key={index}
            className="quick-prompt-btn"
            onClick={() => handleQuickPrompt(prompt)}
            disabled={disabled}
          >
            {prompt}
          </button>
        ))}
      </div>
      
      <form onSubmit={handleSubmit} className="input-form">
        <textarea
          ref={textareaRef}
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Ask me about your infrastructure or documentation..."
          className="input-textarea"
          disabled={disabled}
          rows={1}
        />
        <button
          type="submit"
          className={`send-button ${disabled ? 'disabled' : ''}`}
          disabled={disabled || !input.trim()}
        >
          <svg
            width="20"
            height="20"
            viewBox="0 0 20 20"
            fill="none"
            xmlns="http://www.w3.org/2000/svg"
          >
            <path
              d="M2.5 10L17.5 2.5L10 17.5L8.75 11.25L2.5 10Z"
              stroke="currentColor"
              strokeWidth="2"
              strokeLinecap="round"
              strokeLinejoin="round"
            />
          </svg>
        </button>
      </form>
      
      <div className="input-hint">
        Press <kbd>Enter</kbd> to send, <kbd>Shift + Enter</kbd> for new line
      </div>
    </div>
  );
};

export default InputBox;
