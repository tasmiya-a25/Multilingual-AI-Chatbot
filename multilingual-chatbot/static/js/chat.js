/**
 * Core Chat Logic and Socket.IO Integration
 */

document.addEventListener('DOMContentLoaded', () => {
    // State
    let sessionId = localStorage.getItem('chat_session_id');
    if (!sessionId) {
        sessionId = generateSessionId();
        localStorage.setItem('chat_session_id', sessionId);
    }
    
    let isConnected = false;
    let selectedLang = 'auto';
    
    // DOM Elements
    const chatForm = document.getElementById('chatForm');
    const messageInput = document.getElementById('messageInput');
    const messagesWrapper = document.getElementById('messagesWrapper');
    const chatContainer = document.getElementById('chatContainer');
    const welcomeScreen = document.getElementById('welcomeScreen');
    const typingIndicator = document.getElementById('typingIndicator');
    const langSelector = document.getElementById('langSelector');
    const newChatBtn = document.getElementById('newChatBtn');
    const clearHistoryBtn = document.getElementById('clearHistoryBtn');
    const voiceBtn = document.getElementById('voiceBtn');
    
    // Initialize Socket.IO
    const socket = io();
    
    // Socket Events
    socket.on('connect', () => {
        isConnected = true;
        updateConnectionStatus(true);
        console.log('Connected to server');
    });
    
    socket.on('disconnect', () => {
        isConnected = false;
        updateConnectionStatus(false);
        console.log('Disconnected from server');
    });
    
    socket.on('typing_status', (data) => {
        if (data.is_typing) {
            typingIndicator.classList.remove('hidden');
            scrollToBottom();
        } else {
            typingIndicator.classList.add('hidden');
        }
    });
    
    socket.on('bot_response', (data) => {
        addMessage(data.response, 'bot', data.language);
    });
    
    socket.on('error', (data) => {
        addMessage(`Error: ${data.message}`, 'bot', 'en');
    });
    
    // Event Listeners
    chatForm.addEventListener('submit', (e) => {
        e.preventDefault();
        const text = messageInput.value.trim();
        if (text) {
            sendMessage(text);
        }
    });
    
    langSelector.addEventListener('change', (e) => {
        selectedLang = e.target.value;
    });
    
    newChatBtn.addEventListener('click', () => {
        sessionId = generateSessionId();
        localStorage.setItem('chat_session_id', sessionId);
        messagesWrapper.innerHTML = '';
        welcomeScreen.style.display = 'flex';
    });
    
    clearHistoryBtn.addEventListener('click', async () => {
        try {
            await fetch(`/api/session/${sessionId}/clear`, { method: 'POST' });
            messagesWrapper.innerHTML = '';
            welcomeScreen.style.display = 'flex';
        } catch (err) {
            console.error('Failed to clear history', err);
        }
    });
    
    // Speech Recognition (Web Speech API)
    if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        const recognition = new SpeechRecognition();
        
        recognition.continuous = false;
        recognition.interimResults = false;
        
        voiceBtn.addEventListener('click', () => {
            // Set recognition language based on selection if possible, default to English
            let langMap = {'en': 'en-US', 'hi': 'hi-IN', 'kn': 'kn-IN', 'auto': 'en-US'};
            recognition.lang = langMap[selectedLang] || 'en-US';
            
            voiceBtn.classList.add('recording');
            messageInput.placeholder = "Listening...";
            recognition.start();
        });
        
        recognition.onresult = (event) => {
            const transcript = event.results[0][0].transcript;
            messageInput.value = transcript;
            // Auto send
            setTimeout(() => {
                if (messageInput.value) {
                    sendMessage(messageInput.value);
                }
            }, 500);
        };
        
        recognition.onspeechend = () => {
            recognition.stop();
            voiceBtn.classList.remove('recording');
            messageInput.placeholder = "Type a message... (Auto-detects language)";
        };
        
        recognition.onerror = (event) => {
            console.error('Speech recognition error', event.error);
            voiceBtn.classList.remove('recording');
            messageInput.placeholder = "Type a message... (Auto-detects language)";
        };
    } else {
        voiceBtn.style.display = 'none';
    }
    
    // Global function for suggestion chips
    window.sendSuggestedMessage = function(text) {
        sendMessage(text);
    };
    
    // Functions
    function sendMessage(text) {
        if (!text || !isConnected) return;
        
        // Hide welcome screen on first message
        if (welcomeScreen.style.display !== 'none') {
            welcomeScreen.style.display = 'none';
        }
        
        // Add user message to UI
        addMessage(text, 'user');
        
        // Clear input
        messageInput.value = '';
        messageInput.focus();
        
        // Send via WebSocket
        const payload = {
            message: text,
            session_id: sessionId
        };
        
        if (selectedLang !== 'auto') {
            payload.language = selectedLang;
        }
        
        socket.emit('chat_message', payload);
    }
    
    function addMessage(text, sender, lang = null) {
        const time = formatTime();
        const formattedText = formatMessageText(text);
        
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}`;
        
        const avatarIcon = sender === 'bot' ? 'fa-robot' : 'fa-user';
        
        let metaHtml = `<div class="msg-meta">`;
        if (sender === 'bot' && lang) {
            const flag = getFlagForLang(lang);
            metaHtml += `<span class="lang-badge">${flag} ${lang}</span>`;
        }
        metaHtml += `<span>${time}</span></div>`;
        
        messageDiv.innerHTML = `
            <div class="avatar"><i class="fa-solid ${avatarIcon}"></i></div>
            <div>
                <div class="bubble">
                    ${formattedText}
                </div>
                ${metaHtml}
            </div>
        `;
        
        messagesWrapper.appendChild(messageDiv);
        scrollToBottom();
    }
    
    function scrollToBottom() {
        chatContainer.scrollTop = chatContainer.scrollHeight;
    }
    
    // Load history if exists
    async function loadHistory() {
        try {
            const res = await fetch(`/api/session/${sessionId}/history`);
            const data = await res.json();
            
            if (data.history && data.history.length > 0) {
                welcomeScreen.style.display = 'none';
                
                data.history.forEach(interaction => {
                    // Add user message
                    addMessage(interaction.user_message, 'user');
                    // Add bot message
                    addMessage(interaction.response, 'bot', interaction.language);
                });
            }
        } catch (err) {
            console.error("Failed to load history", err);
        }
    }
    
    // Initial load
    loadHistory();
});
