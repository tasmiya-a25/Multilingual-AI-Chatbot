/**
 * Chat UI Utilities
 */

// Generate a random session ID
function generateSessionId() {
    return 'sess_' + Math.random().toString(36).substr(2, 9);
}

// Format timestamp
function formatTime() {
    const now = new Date();
    return now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
}

// Escape HTML to prevent XSS
function escapeHTML(str) {
    return str
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#039;');
}

// Convert links in text to actual HTML links
function linkify(text) {
    const urlRegex = /(https?:\/\/[^\s]+)/g;
    return text.replace(urlRegex, function(url) {
        return `<a href="${url}" target="_blank" rel="noopener noreferrer" style="color: #6366f1; text-decoration: underline;">${url}</a>`;
    });
}

// Format message text
function formatMessageText(text) {
    let formatted = escapeHTML(text);
    formatted = linkify(formatted);
    // Replace newlines with <br>
    formatted = formatted.replace(/\n/g, '<br>');
    return formatted;
}

// Get flag emoji based on language code
function getFlagForLang(langCode) {
    const flags = {
        'en': '🇺🇸',
        'hi': '🇮🇳',
        'kn': '🇮🇳',
        'auto': '🌐'
    };
    return flags[langCode] || '🏳️';
}

// Set connection status UI
function updateConnectionStatus(isConnected) {
    const dot = document.getElementById('connectionDot');
    const text = document.getElementById('connectionText');
    
    if (isConnected) {
        dot.className = 'status-dot online';
        text.textContent = 'Connected';
    } else {
        dot.className = 'status-dot';
        text.textContent = 'Disconnected';
    }
}
