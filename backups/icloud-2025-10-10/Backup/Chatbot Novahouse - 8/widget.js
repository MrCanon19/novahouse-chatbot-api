"""
NovaHouse Chatbot Widget
Gotowy do wstawienia na stronę klienta
"""

(function() {
    // Konfiguracja widgetu
    const config = {
        chatbotUrl: 'https://glass-core-467907-e9.ey.r.appspot.com/static/chatbot.html',
        buttonColor: '#667eea',
        buttonIcon: '💬',
        position: 'bottom-right', // bottom-right, bottom-left, top-right, top-left
        size: 'medium', // small, medium, large
        title: 'Cześć! Jak mogę pomóc?',
        autoShow: 5000, // Pokaż po 5 sekundach (ms)
        showOnScroll: 20, // Pokaż po 20% scrolla
        closeable: true,
        soundNotification: true,
        customCss: ''
    };

    // Pobranie konfiguracji ze skryptu
    const scriptTag = document.currentScript;
    if (scriptTag) {
        for (const key in config) {
            if (scriptTag.hasAttribute('data-' + key)) {
                const value = scriptTag.getAttribute('data-' + key);
                if (typeof config[key] === 'boolean') {
                    config[key] = (value === 'true');
                } else if (typeof config[key] === 'number') {
                    config[key] = parseInt(value, 10);
                } else {
                    config[key] = value;
                }
            }
        }
    }

    // Tworzenie elementów widgetu
    const widgetContainer = document.createElement('div');
    widgetContainer.id = 'novahouse-widget-container';
    widgetContainer.style.position = 'fixed';
    widgetContainer.style.zIndex = '9999';
    widgetContainer.style.transition = 'all 0.3s ease-in-out';

    const chatButton = document.createElement('div');
    chatButton.id = 'novahouse-chat-button';
    chatButton.style.width = '60px';
    chatButton.style.height = '60px';
    chatButton.style.borderRadius = '50%';
    chatButton.style.backgroundColor = config.buttonColor;
    chatButton.style.color = 'white';
    chatButton.style.display = 'flex';
    chatButton.style.justifyContent = 'center';
    chatButton.style.alignItems = 'center';
    chatButton.style.fontSize = '30px';
    chatButton.style.cursor = 'pointer';
    chatButton.style.boxShadow = '0 4px 12px rgba(0,0,0,0.15)';
    chatButton.innerHTML = config.buttonIcon;

    const chatWindow = document.createElement('div');
    chatWindow.id = 'novahouse-chat-window';
    chatWindow.style.width = '400px';
    chatWindow.style.height = '600px';
    chatWindow.style.position = 'absolute';
    chatWindow.style.display = 'none';
    chatWindow.style.flexDirection = 'column';
    chatWindow.style.border = '1px solid #ddd';
    chatWindow.style.borderRadius = '10px';
    chatWindow.style.boxShadow = '0 8px 24px rgba(0,0,0,0.15)';
    chatWindow.style.overflow = 'hidden';
    chatWindow.style.backgroundColor = 'white';

    const chatHeader = document.createElement('div');
    chatHeader.style.padding = '15px';
    chatHeader.style.backgroundColor = config.buttonColor;
    chatHeader.style.color = 'white';
    chatHeader.style.display = 'flex';
    chatHeader.style.justifyContent = 'space-between';
    chatHeader.style.alignItems = 'center';
    chatHeader.innerHTML = `<span>${config.title}</span>`;

    if (config.closeable) {
        const closeButton = document.createElement('span');
        closeButton.style.cursor = 'pointer';
        closeButton.style.fontSize = '20px';
        closeButton.innerHTML = '&times;';
        closeButton.onclick = toggleChat;
        chatHeader.appendChild(closeButton);
    }

    const chatIframe = document.createElement('iframe');
    chatIframe.src = config.chatbotUrl;
    chatIframe.style.flex = '1';
    chatIframe.style.border = 'none';

    // Składanie widgetu
    chatWindow.appendChild(chatHeader);
    chatWindow.appendChild(chatIframe);
    widgetContainer.appendChild(chatButton);
    widgetContainer.appendChild(chatWindow);
    document.body.appendChild(widgetContainer);

    // Pozycjonowanie
    function setPosition() {
        const margin = '20px';
        if (config.position.includes('bottom')) {
            widgetContainer.style.bottom = margin;
            chatWindow.style.bottom = '80px';
        } else {
            widgetContainer.style.top = margin;
            chatWindow.style.top = '80px';
        }
        if (config.position.includes('right')) {
            widgetContainer.style.right = margin;
            chatWindow.style.right = '0';
        } else {
            widgetContainer.style.left = margin;
            chatWindow.style.left = '0';
        }
    }
    setPosition();

    // Rozmiar
    function setSize() {
        if (config.size === 'small') {
            chatWindow.style.width = '320px';
            chatWindow.style.height = '480px';
        } else if (config.size === 'large') {
            chatWindow.style.width = '450px';
            chatWindow.style.height = '700px';
        }
    }
    setSize();

    // Logika otwierania/zamykania
    let isOpen = false;
    function toggleChat() {
        isOpen = !isOpen;
        chatWindow.style.display = isOpen ? 'flex' : 'none';
        chatButton.innerHTML = isOpen ? '&times;' : config.buttonIcon;
        if (isOpen && config.soundNotification) {
            // playSound();
        }
    }
    chatButton.onclick = toggleChat;

    // Auto-show
    if (config.autoShow > 0) {
        setTimeout(() => {
            if (!isOpen) toggleChat();
        }, config.autoShow);
    }

    // Show on scroll
    if (config.showOnScroll > 0) {
        window.addEventListener('scroll', () => {
            const scrollPercent = (window.scrollY / (document.documentElement.scrollHeight - window.innerHeight)) * 100;
            if (scrollPercent >= config.showOnScroll && !isOpen) {
                toggleChat();
            }
        });
    }

    // Custom CSS
    if (config.customCss) {
        const styleSheet = document.createElement("style");
        styleSheet.type = "text/css";
        styleSheet.innerText = config.customCss;
        document.head.appendChild(styleSheet);
    }

    // Dźwięk powiadomienia
    function playSound() {
        const audio = new Audio('data:audio/mpeg;base64,SUQzBAAAAAAAI1RTU0UAAAAPAAADTGF2ZjU4LjI5LjEwMAAAAAAAAAAAAAAA//tAwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA');
        audio.play();
    }

    console.log('NovaHouse Chatbot Widget loaded!');
})();


