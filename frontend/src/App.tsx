import React from 'react';
import ChatWindow from './components/ChatWindow';
import './App.css';

function App() {
  return (
    <div className="app">
      <header className="app-header">
        <div className="header-content">
          <h1>Infra-Chat</h1>
          <p className="subtitle">Cloud Infrastructure Management Platform</p>
        </div>
      </header>
      
      <main className="app-main">
        <ChatWindow />
      </main>
      
      <footer className="app-footer">
        <p>Powered by Google Gemini • LangChain • ChromaDB</p>
      </footer>
    </div>
  );
}

export default App;
