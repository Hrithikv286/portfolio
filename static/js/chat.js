/**
 * ElectroStore - AI Chat Widget JavaScript
 * Handles: Chat toggle, message sending, typing indicator, suggestions, feedback
 */

const chatWidget = {
  isOpen: false,
  isTyping: false,
  lastLogId: null,

  elements: {
    toggle: document.getElementById('chat-toggle'),
    window: document.getElementById('chat-window'),
    close: document.getElementById('chat-close'),
    messages: document.getElementById('chat-messages'),
    input: document.getElementById('chat-input'),
    send: document.getElementById('chat-send'),
    suggestions: document.getElementById('chat-suggestions'),
    iconOpen: document.querySelector('.chat-icon-open'),
    iconClose: document.querySelector('.chat-icon-close'),
  },

  init() {
    const { toggle, close, input, send } = this.elements;

    if (!toggle) return; // Chat widget not on this page

    toggle.addEventListener('click', () => this.toggleChat());
    close.addEventListener('click', () => this.closeChat());

    // Send on button click
    send.addEventListener('click', () => this.handleSend());

    // Send on Enter (Shift+Enter for newline)
    input.addEventListener('keydown', (e) => {
      if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        this.handleSend();
      }
    });

    // Auto-resize textarea
    input.addEventListener('input', () => {
      input.style.height = 'auto';
      input.style.height = Math.min(input.scrollHeight, 100) + 'px';
    });

    // Suggestion chips
    document.querySelectorAll('.suggestion-chip').forEach(chip => {
      chip.addEventListener('click', () => {
        const question = chip.dataset.question;
        input.value = question;
        this.handleSend();
      });
    });

    // Close on outside click
    document.addEventListener('click', (e) => {
      if (this.isOpen && !e.target.closest('#chat-widget')) {
        // Keep open for better UX - don't auto close
      }
    });

    // Open chat if error page is present
    if (document.querySelector('[data-open-chat]')) {
      setTimeout(() => this.openChat(), 1000);
    }
  },

  toggleChat() {
    if (this.isOpen) this.closeChat();
    else this.openChat();
  },

  openChat() {
    this.isOpen = true;
    const { window: chatWindow, toggle, iconOpen, iconClose } = this.elements;
    chatWindow.classList.add('open');
    chatWindow.setAttribute('aria-hidden', 'false');
    toggle.setAttribute('aria-expanded', 'true');
    iconOpen.style.display = 'none';
    iconClose.style.display = 'flex';
    this.elements.input.focus();
    this.scrollToBottom();
  },

  closeChat() {
    this.isOpen = false;
    const { window: chatWindow, toggle, iconOpen, iconClose } = this.elements;
    chatWindow.classList.remove('open');
    chatWindow.setAttribute('aria-hidden', 'true');
    toggle.setAttribute('aria-expanded', 'false');
    iconOpen.style.display = 'flex';
    iconClose.style.display = 'none';
  },

  handleSend() {
    const message = this.elements.input.value.trim();
    if (!message || this.isTyping) return;

    // Clear input
    this.elements.input.value = '';
    this.elements.input.style.height = 'auto';

    // Hide suggestions
    if (this.elements.suggestions) {
      this.elements.suggestions.style.display = 'none';
    }

    // Add user message
    this.addMessage('user', message);

    // Show typing indicator
    this.showTyping();

    // Send to backend
    this.sendMessage(message);
  },

  addMessage(type, content, timestamp = null) {
    const { messages } = this.elements;
    const time = timestamp || new Date().toLocaleTimeString('en-IN', { hour: '2-digit', minute: '2-digit' });

    const div = document.createElement('div');
    div.className = `message ${type}`;

    // Convert markdown-like formatting
    const formatted = this.formatMessage(content);

    div.innerHTML = `
      <div>
        <div class="message-bubble">${formatted}</div>
        <div class="message-time">${time}</div>
      </div>
    `;

    messages.appendChild(div);
    this.scrollToBottom();
    return div;
  },

  formatMessage(text) {
    // Escape HTML first
    let formatted = text
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;');

    // Bold: **text**
    formatted = formatted.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');

    // Bullet points: lines starting with •
    formatted = formatted.replace(/^[•·]\s(.+)$/gm, '<span style="display:block; margin-left:8px;">• $1</span>');

    // Numbered lines
    formatted = formatted.replace(/^(\d+)\.\s(.+)$/gm, '<span style="display:block; margin-left:8px;">$1. $2</span>');

    // Line breaks
    formatted = formatted.replace(/\n/g, '<br>');

    return formatted;
  },

  showTyping() {
    this.isTyping = true;
    this.elements.send.disabled = true;

    const { messages } = this.elements;
    const div = document.createElement('div');
    div.className = 'message bot';
    div.id = 'typing-indicator';
    div.innerHTML = `
      <div>
        <div class="typing-indicator">
          <div class="typing-dot"></div>
          <div class="typing-dot"></div>
          <div class="typing-dot"></div>
        </div>
      </div>
    `;
    messages.appendChild(div);
    this.scrollToBottom();
  },

  hideTyping() {
    this.isTyping = false;
    this.elements.send.disabled = false;
    const indicator = document.getElementById('typing-indicator');
    if (indicator) indicator.remove();
  },

  async sendMessage(message) {
    try {
      const response = await fetch('/chat/message/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': getCsrfToken(),
        },
        body: JSON.stringify({ message }),
      });

      const data = await response.json();

      this.hideTyping();

      if (data.success) {
        const msgEl = this.addMessage('bot', data.response);
        this.lastLogId = data.log_id;

        // Show ticket notification
        if (data.ticket_created && data.ticket_id) {
          showToast(`Support ticket ${data.ticket_id} created!`, 'info', 5000);
        }

        // Show feedback buttons after bot response
        if (data.log_id) {
          setTimeout(() => this.showFeedback(data.log_id), 500);
        }
      } else {
        this.addMessage('bot', data.error || 'Sorry, something went wrong. Please try again.');
      }
    } catch (err) {
      console.error('Chat error:', err);
      this.hideTyping();
      this.addMessage('bot', 'Connection error. Please check your internet and try again.');
    }
  },

  showFeedback(logId) {
    const { messages } = this.elements;
    const div = document.createElement('div');
    div.className = 'message bot';
    div.innerHTML = `
      <div>
        <div style="display:flex; gap:6px; align-items:center;">
          <span style="font-size:0.75rem; color:var(--text-muted);">Was this helpful?</span>
          <button onclick="chatWidget.submitFeedback('${logId}', 5, this)" style="background:var(--bg-700); border:1px solid var(--border); border-radius:6px; padding:3px 8px; color:var(--text-secondary); cursor:pointer; font-size:0.75rem;" title="Helpful">👍</button>
          <button onclick="chatWidget.submitFeedback('${logId}', 1, this)" style="background:var(--bg-700); border:1px solid var(--border); border-radius:6px; padding:3px 8px; color:var(--text-secondary); cursor:pointer; font-size:0.75rem;" title="Not helpful">👎</button>
        </div>
      </div>
    `;
    messages.appendChild(div);
    this.scrollToBottom();
  },

  async submitFeedback(logId, rating, btn) {
    try {
      await fetch('/chat/feedback/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': getCsrfToken(),
        },
        body: JSON.stringify({ log_id: logId, rating }),
      });

      // Update UI
      const parent = btn.closest('div');
      parent.innerHTML = `<span style="font-size:0.75rem; color:var(--success);">✓ Thanks for your feedback!</span>`;
    } catch (err) {
      console.error('Feedback error:', err);
    }
  },

  scrollToBottom() {
    const { messages } = this.elements;
    requestAnimationFrame(() => {
      messages.scrollTop = messages.scrollHeight;
    });
  },
};

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', () => chatWidget.init());

// Expose globally for inline handlers
window.chatWidget = chatWidget;

// Error page: auto-open chat with pre-filled question
document.addEventListener('DOMContentLoaded', () => {
  const errorCode = document.querySelector('[data-error-code]')?.dataset.errorCode;
  if (errorCode) {
    const askBtn = document.getElementById('ask-assistant-btn');
    if (askBtn) {
      askBtn.addEventListener('click', () => {
        chatWidget.openChat();
        setTimeout(() => {
          chatWidget.elements.input.value = `What does error ${errorCode} mean and how do I fix it?`;
          chatWidget.elements.input.focus();
        }, 400);
      });
    }
  }
});
