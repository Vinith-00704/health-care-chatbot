document.addEventListener('DOMContentLoaded', () => {
    // ── DOM References ──────────────────────────────────────
    const chatHistory     = document.getElementById('chat-history');
    const userInput       = document.getElementById('user-input');
    const sendBtn         = document.getElementById('send-btn');
    const typingIndicator = document.getElementById('typing-indicator');
    const themeToggle     = document.getElementById('theme-toggle');
    const clearChatBtn    = document.getElementById('clear-chat');
    const newSessionBtn   = document.getElementById('new-session-btn');
    const suggestionBtns  = document.querySelectorAll('.suggestion-btn');
    const emojiBtn        = document.getElementById('emoji-btn');
    const symptomTracker  = document.getElementById('symptom-tracker');
    const trackerTags     = document.getElementById('tracker-tags');

    // ── Session Management ──────────────────────────────────
    // Generate/retrieve a session ID stored in sessionStorage
    // This resets when the browser tab is closed — perfect for "per-chat" memory
    let sessionId = sessionStorage.getItem('nlp_session_id');
    if (!sessionId) {
        sessionId = crypto.randomUUID();
        sessionStorage.setItem('nlp_session_id', sessionId);
    }

    // ── Theme ───────────────────────────────────────────────
    let isDarkMode = localStorage.getItem('theme') === 'dark';
    applyTheme(isDarkMode);

    function applyTheme(dark) {
        if (dark) {
            document.body.setAttribute('data-theme', 'dark');
            themeToggle.innerHTML = '<i class="fa-solid fa-sun"></i>';
        } else {
            document.body.removeAttribute('data-theme');
            themeToggle.innerHTML = '<i class="fa-solid fa-moon"></i>';
        }
    }

    themeToggle.addEventListener('click', () => {
        isDarkMode = !isDarkMode;
        applyTheme(isDarkMode);
        localStorage.setItem('theme', isDarkMode ? 'dark' : 'light');
    });

    // ── Timestamp Helper ────────────────────────────────────
    function formatTime(date) {
        let h = date.getHours(), m = date.getMinutes();
        const ampm = h >= 12 ? 'PM' : 'AM';
        h = h % 12 || 12;
        m = m < 10 ? '0' + m : m;
        return `${h}:${m} ${ampm}`;
    }

    // ── Welcome Message ─────────────────────────────────────
    function showWelcome() {
        chatHistory.innerHTML = `
          <div class="welcome-msg">
            <span class="welcome-icon">🩺</span>
            <h2>Hello! I'm your AI Healthcare Assistant.</h2>
            <p>Tell me your symptoms and I'll help analyse them.<br>
               You can keep describing symptoms across multiple messages — I'll remember everything!</p>
          </div>`;
    }

    // Load from localStorage or show welcome
    const savedChat = localStorage.getItem('nlp_chat_history');
    if (savedChat) {
        chatHistory.innerHTML = savedChat;
        restoreTrackerFromStorage();
    } else {
        showWelcome();
    }

    scrollToBottom();

    function scrollToBottom() {
        chatHistory.scrollTop = chatHistory.scrollHeight;
    }

    function saveChatHistory() {
        localStorage.setItem('nlp_chat_history', chatHistory.innerHTML);
    }

    // ── Messages ────────────────────────────────────────────
    function addUserMessage(text) {
        const msg = document.createElement('div');
        msg.classList.add('message', 'user-message');
        msg.innerHTML = `
          <div class="message-content">${escapeHtml(text)}</div>
          <div class="message-timestamp">${formatTime(new Date())}</div>`;
        chatHistory.appendChild(msg);
        saveChatHistory();
        scrollToBottom();
    }

    function addBotMessage(htmlContent) {
        const msg = document.createElement('div');
        msg.classList.add('message', 'bot-message');
        // Bot messages use innerHTML since the server returns trusted HTML
        msg.innerHTML = `
          <div class="message-content">${htmlContent}</div>
          <div class="message-timestamp">${formatTime(new Date())}</div>`;
        chatHistory.appendChild(msg);
        saveChatHistory();
        scrollToBottom();
    }

    function escapeHtml(text) {
        return text
            .replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;');
    }

    // ── Symptom Tracker ─────────────────────────────────────
    function updateSymptomTracker(symptoms) {
        if (!symptoms || symptoms.length === 0) return;

        // Save to localStorage
        localStorage.setItem('nlp_symptoms', JSON.stringify(symptoms));

        trackerTags.innerHTML = '';
        symptoms.forEach(sym => {
            const tag = document.createElement('span');
            tag.classList.add('sym-tag');
            tag.textContent = sym.charAt(0).toUpperCase() + sym.slice(1);
            trackerTags.appendChild(tag);
        });

        symptomTracker.style.display = 'flex';
    }

    function restoreTrackerFromStorage() {
        const saved = localStorage.getItem('nlp_symptoms');
        if (saved) {
            try {
                const symptoms = JSON.parse(saved);
                if (symptoms.length > 0) updateSymptomTracker(symptoms);
            } catch (e) {}
        }
    }

    // ── Send Message ────────────────────────────────────────
    async function handleSend() {
        const text = userInput.value.trim();
        if (!text) return;

        addUserMessage(text);
        userInput.value = '';

        if (emojiPicker && emojiPicker.style.display !== 'none') {
            emojiPicker.style.display = 'none';
        }

        typingIndicator.style.display = 'flex';
        scrollToBottom();

        try {
            const res = await fetch('/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message: text, session_id: sessionId }),
            });

            if (!res.ok) throw new Error(`HTTP ${res.status}`);

            const data = await res.json();
            typingIndicator.style.display = 'none';

            // Update session ID in case server assigned one
            if (data.session_id) {
                sessionId = data.session_id;
                sessionStorage.setItem('nlp_session_id', sessionId);
            }

            addBotMessage(data.response);

            // Update symptom tracker
            if (data.symptoms) updateSymptomTracker(data.symptoms);

        } catch (err) {
            console.error('Chat error:', err);
            typingIndicator.style.display = 'none';
            addBotMessage(`<div class="response-block mild">
              <p>⚠️ Sorry, I couldn't connect to the server. Please try again.</p>
            </div>`);
        }
    }

    sendBtn.addEventListener('click', handleSend);
    userInput.addEventListener('keypress', e => { if (e.key === 'Enter') handleSend(); });

    // ── Suggestion Buttons ──────────────────────────────────
    suggestionBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            userInput.value = btn.textContent;
            userInput.focus();
        });
    });

    // ── Clear Chat ───────────────────────────────────────────
    clearChatBtn.addEventListener('click', () => {
        if (confirm('Clear chat history? (This does NOT reset session memory on the server)')) {
            localStorage.removeItem('nlp_chat_history');
            localStorage.removeItem('nlp_symptoms');
            symptomTracker.style.display = 'none';
            trackerTags.innerHTML = '';
            showWelcome();
        }
    });

    // ── New Session ──────────────────────────────────────────
    newSessionBtn.addEventListener('click', async () => {
        if (!confirm('Start a new session? This will reset all remembered symptoms.')) return;

        try {
            // Tell the server to clear this session's memory
            await fetch('/reset_session', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ session_id: sessionId }),
            });
        } catch (e) { /* ignore network errors on reset */ }

        // Generate a new session ID
        sessionId = crypto.randomUUID();
        sessionStorage.setItem('nlp_session_id', sessionId);

        // Clear local state
        localStorage.removeItem('nlp_chat_history');
        localStorage.removeItem('nlp_symptoms');
        symptomTracker.style.display = 'none';
        trackerTags.innerHTML = '';
        showWelcome();

        showToast('🔄 New session started. Memory cleared!');
    });

    // ── Toast Notification ───────────────────────────────────
    function showToast(message) {
        const toast = document.createElement('div');
        toast.classList.add('toast');
        toast.textContent = message;
        document.body.appendChild(toast);
        requestAnimationFrame(() => {
            requestAnimationFrame(() => toast.classList.add('show'));
        });
        setTimeout(() => {
            toast.classList.remove('show');
            setTimeout(() => toast.remove(), 400);
        }, 2800);
    }

    // ── Emoji Picker ─────────────────────────────────────────
    const emojis = ['😀', '🩺', '💊', '🤧', '🤒', '🤕', '👍', '🙏', '😔', '💪'];
    let emojiPicker = document.createElement('div');
    Object.assign(emojiPicker.style, {
        position: 'absolute', bottom: '80px', left: '16px',
        background: 'var(--chat-bg)', border: '1px solid var(--border)',
        borderRadius: '10px', padding: '8px 10px', display: 'none',
        gap: '8px', flexWrap: 'wrap', width: '180px',
        boxShadow: 'var(--shadow)', zIndex: '100',
    });
    emojiPicker.style.display = 'none';

    emojis.forEach(emoji => {
        const span = document.createElement('span');
        span.textContent = emoji;
        Object.assign(span.style, { cursor: 'pointer', fontSize: '1.2rem', transition: 'transform 0.1s' });
        span.onmouseover = () => span.style.transform = 'scale(1.25)';
        span.onmouseout  = () => span.style.transform = 'scale(1)';
        span.onclick = () => {
            userInput.value += emoji;
            userInput.focus();
            emojiPicker.style.display = 'none';
        };
        emojiPicker.appendChild(span);
    });

    document.querySelector('.chat-container').appendChild(emojiPicker);

    emojiBtn.addEventListener('click', e => {
        e.stopPropagation();
        emojiPicker.style.display = emojiPicker.style.display === 'none' ? 'flex' : 'none';
    });

    document.addEventListener('click', e => {
        if (emojiPicker.style.display === 'flex' &&
            !emojiBtn.contains(e.target) &&
            !emojiPicker.contains(e.target)) {
            emojiPicker.style.display = 'none';
        }
    });

    userInput.focus();
});
