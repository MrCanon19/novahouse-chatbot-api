"""
Logika panelu administracyjnego NovaHouse
"""

document.addEventListener("DOMContentLoaded", function() {
    const API_BASE_URL = "/api";

    // Funkcje pomocnicze
    const fetchData = async (endpoint) => {
        try {
            const response = await fetch(`${API_BASE_URL}${endpoint}`);
            if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
            return await response.json();
        } catch (error) {
            console.error(`Fetch error for ${endpoint}:`, error);
            return [];
        }
    };

    const postData = async (endpoint, data) => {
        try {
            const response = await fetch(`${API_BASE_URL}${endpoint}`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            });
            if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
            return await response.json();
        } catch (error) {
            console.error(`Post error for ${endpoint}:`, error);
            return { success: false, error: error.message };
        }
    };

    // Ładowanie danych
    const loadConversations = async () => {
        const conversations = await fetchData("/analytics/conversations");
        const tableBody = document.getElementById("conversations-table");
        tableBody.innerHTML = conversations.map(c => `
            <tr>
                <td>${c.session_id.substring(0, 8)}</td>
                <td>${c.user_message}</td>
                <td>${c.bot_response}</td>
                <td>${c.intent || 'N/A'}</td>
                <td>${new Date(c.timestamp).toLocaleString()}</td>
            </tr>
        `).join('');
    };

    const loadIntents = async () => {
        const intents = await fetchData("/chatbot/intents");
        const tableBody = document.getElementById("intents-table");
        tableBody.innerHTML = intents.map(i => `
            <tr>
                <td>${i.name}</td>
                <td>${i.training_phrases.join(', ')}</td>
                <td><button class="btn btn-sm btn-warning">Edytuj</button></td>
            </tr>
        `).join('');
    };

    const loadEntities = async () => {
        const entities = await fetchData("/chatbot/entities");
        const tableBody = document.getElementById("entities-table");
        tableBody.innerHTML = entities.map(e => `
            <tr>
                <td>${e.name}</td>
                <td>${e.values.join(', ')}</td>
                <td><button class="btn btn-sm btn-warning">Edytuj</button></td>
            </tr>
        `).join('');
    };

    const loadKnowledgeBase = async () => {
        const knowledge = await fetchData("/chatbot/knowledge");
        document.getElementById("knowledge-base-content").value = knowledge.content || '';
    };

    // Inicjalizacja
    const initAdminPanel = () => {
        // Ładowanie dashboardu analitycznego
        fetch("/static/dashboard.html")
            .then(response => response.text())
            .then(html => {
                const parser = new DOMParser();
                const doc = parser.parseFromString(html, "text/html");
                document.getElementById("analytics-dashboard-content").innerHTML = doc.body.innerHTML;
            });

        // Ładowanie danych do zakładek
        const tabs = document.querySelectorAll('.nav-link');
        tabs.forEach(tab => {
            tab.addEventListener('shown.bs.tab', event => {
                const targetId = event.target.getAttribute('href');
                if (targetId === '#conversations') loadConversations();
                if (targetId === '#intents') loadIntents();
                if (targetId === '#entities') loadEntities();
                if (targetId === '#knowledge') loadKnowledgeBase();
            });
        });

        // Domyślne ładowanie dashboardu
        loadConversations(); // Załaduj rozmowy na start
    };

    initAdminPanel();
});


