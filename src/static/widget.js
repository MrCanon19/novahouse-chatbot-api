/**
 * NovaHouse Chatbot Widget
 * Embed on any website with one line of code
 */
(function() {
    'use strict';
    
    // Configuration
    const WIDGET_CONFIG = {
        apiUrl: window.NOVAHOUSE_API_URL || 'https://your-app.appspot.com',
        position: 'bottom-right', // bottom-right, bottom-left
        primaryColor: '#667eea',
        title: 'Czat NovaHouse',
        greeting: 'Cześć! W czym mogę pomóc?',
        placeholder: 'Napisz wiadomość...'
    };
    
    // Widget State
    let isOpen = false;
    let sessionId = generateSessionId();
    let messageHistory = [];
    
    // Generate unique session ID
    function generateSessionId() {
        return 'widget_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
    }
    
    // Create widget HTML
    function createWidget() {
        const widgetHTML = `
            <div id="novahouse-widget" class="novahouse-widget ${WIDGET_CONFIG.position}">
                <!-- Chat Button -->
                <div id="novahouse-button" class="novahouse-button">
                    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                        <path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z"/>
                    </svg>
                </div>
                
                <!-- Chat Window -->
                <div id="novahouse-chat" class="novahouse-chat hidden">
                    <!-- Header -->
                    <div class="novahouse-header">
                        <h3>${WIDGET_CONFIG.title}</h3>
                        <button id="novahouse-close" class="novahouse-close">×</button>
                    </div>
                    
                    <!-- Messages -->
                    <div id="novahouse-messages" class="novahouse-messages">
                        <div class="novahouse-message bot">
                            <div class="message-content">${WIDGET_CONFIG.greeting}</div>
                        </div>
                    </div>
                    
                    <!-- Input -->
                    <div class="novahouse-input-container">
                        <input 
                            type="text" 
                            id="novahouse-input" 
                            placeholder="${WIDGET_CONFIG.placeholder}" 
                            autocomplete="off"
                        />
                        <button id="novahouse-send" class="novahouse-send">
                            <svg width="20" height="20" viewBox="0 0 20 20" fill="currentColor">
                                <path d="M2 10l18-8-8 18-2-8-8-2z"/>
                            </svg>
                        </button>
                    </div>
                </div>
            </div>
        `;
        
        document.body.insertAdjacentHTML('beforeend', widgetHTML);
        injectStyles();
        attachEventListeners();
    }
    
    // Inject widget styles
    function injectStyles() {
        const styles = `
            .novahouse-widget {
                position: fixed;
                z-index: 9999;
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            }
            
            .novahouse-widget.bottom-right {
                bottom: 20px;
                right: 20px;
            }
            
            .novahouse-widget.bottom-left {
                bottom: 20px;
                left: 20px;
            }
            
            .novahouse-button {
                width: 60px;
                height: 60px;
                border-radius: 30px;
                background: ${WIDGET_CONFIG.primaryColor};
                color: white;
                display: flex;
                align-items: center;
                justify-content: center;
                cursor: pointer;
                box-shadow: 0 4px 12px rgba(0,0,0,0.15);
                transition: transform 0.2s;
            }
            
            .novahouse-button:hover {
                transform: scale(1.1);
            }
            
            .novahouse-chat {
                position: absolute;
                bottom: 80px;
                right: 0;
                width: 380px;
                height: 600px;
                max-height: 80vh;
                background: white;
                border-radius: 12px;
                box-shadow: 0 8px 24px rgba(0,0,0,0.15);
                display: flex;
                flex-direction: column;
                overflow: hidden;
            }
            
            .novahouse-chat.hidden {
                display: none;
            }
            
            .novahouse-header {
                background: ${WIDGET_CONFIG.primaryColor};
                color: white;
                padding: 16px;
                display: flex;
                justify-content: space-between;
                align-items: center;
            }
            
            .novahouse-header h3 {
                margin: 0;
                font-size: 18px;
                font-weight: 600;
            }
            
            .novahouse-close {
                background: none;
                border: none;
                color: white;
                font-size: 28px;
                cursor: pointer;
                padding: 0;
                width: 32px;
                height: 32px;
                display: flex;
                align-items: center;
                justify-content: center;
            }
            
            .novahouse-messages {
                flex: 1;
                overflow-y: auto;
                padding: 16px;
                display: flex;
                flex-direction: column;
                gap: 12px;
            }
            
            .novahouse-message {
                display: flex;
                max-width: 80%;
            }
            
            .novahouse-message.user {
                align-self: flex-end;
            }
            
            .novahouse-message.bot {
                align-self: flex-start;
            }
            
            .message-content {
                padding: 12px 16px;
                border-radius: 12px;
                word-wrap: break-word;
            }
            
            .novahouse-message.user .message-content {
                background: ${WIDGET_CONFIG.primaryColor};
                color: white;
            }
            
            .novahouse-message.bot .message-content {
                background: #f0f0f0;
                color: #333;
            }
            
            .novahouse-input-container {
                padding: 16px;
                border-top: 1px solid #e0e0e0;
                display: flex;
                gap: 8px;
            }
            
            .novahouse-input-container input {
                flex: 1;
                padding: 12px;
                border: 1px solid #e0e0e0;
                border-radius: 8px;
                font-size: 14px;
                outline: none;
            }
            
            .novahouse-input-container input:focus {
                border-color: ${WIDGET_CONFIG.primaryColor};
            }
            
            .novahouse-send {
                width: 44px;
                height: 44px;
                background: ${WIDGET_CONFIG.primaryColor};
                color: white;
                border: none;
                border-radius: 8px;
                cursor: pointer;
                display: flex;
                align-items: center;
                justify-content: center;
            }
            
            .novahouse-send:hover {
                opacity: 0.9;
            }
            
            @media (max-width: 480px) {
                .novahouse-chat {
                    width: calc(100vw - 40px);
                    height: calc(100vh - 100px);
                }
            }
        `;
        
        const styleSheet = document.createElement('style');
        styleSheet.textContent = styles;
        document.head.appendChild(styleSheet);
    }
    
    // Attach event listeners
    function attachEventListeners() {
        const button = document.getElementById('novahouse-button');
        const closeBtn = document.getElementById('novahouse-close');
        const sendBtn = document.getElementById('novahouse-send');
        const input = document.getElementById('novahouse-input');
        
        button.addEventListener('click', toggleChat);
        closeBtn.addEventListener('click', toggleChat);
        sendBtn.addEventListener('click', sendMessage);
        input.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') sendMessage();
        });
    }
    
    // Toggle chat window
    function toggleChat() {
        isOpen = !isOpen;
        const chat = document.getElementById('novahouse-chat');
        chat.classList.toggle('hidden');
        
        if (isOpen) {
            document.getElementById('novahouse-input').focus();
        }
    }
    
    // Send message
    async function sendMessage() {
        const input = document.getElementById('novahouse-input');
        const message = input.value.trim();
        
        if (!message) return;
        
        // Add user message to UI
        addMessage(message, 'user');
        input.value = '';
        
        // Show typing indicator
        const typingId = showTyping();
        
        try {
            // Send to API
            const response = await fetch(`${WIDGET_CONFIG.apiUrl}/api/chatbot/chat`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    message: message,
                    session_id: sessionId
                })
            });
            
            const data = await response.json();
            
            // Remove typing indicator
            removeTyping(typingId);
            
            // Add bot response
            if (data.response) {
                addMessage(data.response, 'bot');
            } else {
                addMessage('Przepraszam, wystąpił błąd. Spróbuj ponownie.', 'bot');
            }
            
        } catch (error) {
            console.error('Chat error:', error);
            removeTyping(typingId);
            addMessage('Przepraszam, nie mogę się połączyć. Spróbuj później.', 'bot');
        }
    }
    
    // Add message to chat
    function addMessage(content, sender) {
        const messagesDiv = document.getElementById('novahouse-messages');
        const messageDiv = document.createElement('div');
        messageDiv.className = `novahouse-message ${sender}`;
        messageDiv.innerHTML = `<div class="message-content">${content}</div>`;
        
        messagesDiv.appendChild(messageDiv);
        messagesDiv.scrollTop = messagesDiv.scrollHeight;
        
        messageHistory.push({
            content,
            sender,
            timestamp: new Date()
        });
    }
    
    // Show typing indicator
    function showTyping() {
        const id = 'typing-' + Date.now();
        const messagesDiv = document.getElementById('novahouse-messages');
        const typingDiv = document.createElement('div');
        typingDiv.id = id;
        typingDiv.className = 'novahouse-message bot';
        typingDiv.innerHTML = '<div class="message-content">...</div>';
        
        messagesDiv.appendChild(typingDiv);
        messagesDiv.scrollTop = messagesDiv.scrollHeight;
        
        return id;
    }
    
    // Remove typing indicator
    function removeTyping(id) {
        const typingDiv = document.getElementById(id);
        if (typingDiv) typingDiv.remove();
    }
    
    // Initialize widget
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', createWidget);
    } else {
        createWidget();
    }
    
})();