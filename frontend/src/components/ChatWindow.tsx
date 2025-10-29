import React, { useState, useRef, useEffect } from 'react';
import MessageList from './MessageList';
import InputBox from './InputBox';
import { Message } from '../types';
import { chatAPI } from '../services/api';
import './ChatWindow.css';

const ChatWindow: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: '1',
      text: "👋 Hi! I'm Infra-Chat, your AI assistant for cloud infrastructure and documentation. I can help you with:\n\n• 📚 Searching team documentation\n• ☁️ Querying live AWS resources\n• 🔍 General cloud knowledge\n\nTry asking me something like:\n- \"List my EC2 instances\"\n- \"Show me the deployment guide\"\n- \"What are the troubleshooting steps?\"",
      sender: 'bot',
      timestamp: new Date(),
    },
  ]);
  const [isTyping, setIsTyping] = useState(false);
  const [isBackendHealthy, setIsBackendHealthy] = useState<boolean | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Check backend health on mount
  useEffect(() => {
    const checkHealth = async () => {
      const healthy = await chatAPI.healthCheck();
      setIsBackendHealthy(healthy);
      
      if (!healthy) {
        addBotMessage(
          "⚠️ Warning: I can't connect to the backend API. Please make sure the Flask server is running on http://localhost:5000"
        );
      }
    };
    
    checkHealth();
  }, []);

  // Auto-scroll to bottom when new messages arrive
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const addUserMessage = (text: string) => {
    const newMessage: Message = {
      id: Date.now().toString(),
      text,
      sender: 'user',
      timestamp: new Date(),
    };
    setMessages((prev) => [...prev, newMessage]);
  };

  const addBotMessage = (text: string) => {
    const newMessage: Message = {
      id: Date.now().toString(),
      text,
      sender: 'bot',
      timestamp: new Date(),
    };
    setMessages((prev) => [...prev, newMessage]);
  };

  const handleSendMessage = async (text: string) => {
    if (!text.trim()) return;

    // Add user message
    addUserMessage(text);

    // Show typing indicator
    setIsTyping(true);

    try {
      // Call backend API
      const response = await chatAPI.sendMessage(text);

      // Hide typing indicator
      setIsTyping(false);

      if (response.success && response.response) {
        addBotMessage(response.response);
      } else {
        addBotMessage(
          `❌ Sorry, I encountered an error: ${response.error || 'Unknown error'}`
        );
      }
    } catch (error) {
      setIsTyping(false);
      addBotMessage(
        '❌ Sorry, something went wrong. Please make sure the backend is running.'
      );
    }
  };

  return (
    <div className="chat-window">
      {isBackendHealthy === false && (
        <div className="backend-warning">
          ⚠️ Backend not connected. Start the Flask server: <code>python app.py</code>
        </div>
      )}
      
      <MessageList messages={messages} isTyping={isTyping} />
      <div ref={messagesEndRef} />
      
      <InputBox onSendMessage={handleSendMessage} disabled={isTyping} />
    </div>
  );
};

export default ChatWindow;
