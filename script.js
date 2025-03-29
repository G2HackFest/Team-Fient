document.addEventListener('DOMContentLoaded', () => {
    const dietForm = document.getElementById('dietForm');
    const planResult = document.getElementById('planResult');
    
    dietForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const btn = e.target.querySelector('button');
        btn.disabled = true;
        
        try {
            const response = await fetch('/api/generate-plan', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    username: document.getElementById('username').value,
                    condition: document.getElementById('condition').value,
                    weight: document.getElementById('weight').value
                })
            });
            
            const data = await response.json();
            
            if (data.error) throw new Error(data.error);
            
            document.getElementById('planOutput').textContent = data.diet_plan;
            document.getElementById('mealsOutput').textContent = data.meals.join('\n');
            
            const shoppingList = document.getElementById('shoppingOutput');
            shoppingList.innerHTML = '';
            data.shopping_list.forEach(item => {
                const li = document.createElement('li');
                li.textContent = item;
                shoppingList.appendChild(li);
            });
            
            planResult.classList.remove('hidden');
        } catch (error) {
            alert('Error: ' + error.message);
        } finally {
            btn.disabled = false;
        }
    });

    // Chat functionality
    const chatInput = document.getElementById('userMessage');
    const sendBtn = document.getElementById('sendBtn');
    const chatMessages = document.getElementById('chatMessages');
    
    function addMessage(text, isUser) {
        const div = document.createElement('div');
        div.className = isUser ? 'user-message' : 'bot-message';
        div.textContent = text;
        chatMessages.appendChild(div);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
    
    sendBtn.addEventListener('click', async () => {
        const message = chatInput.value.trim();
        if (!message) return;
        
        addMessage(message, true);
        chatInput.value = '';
        sendBtn.disabled = true;
        
        try {
            const response = await fetch('/api/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    message: message
                })
            });
            
            const data = await response.json();
            addMessage(data.response, false);
        } catch (error) {
            addMessage("Sorry, I'm having trouble responding.", false);
        } finally {
            sendBtn.disabled = false;
        }
    });
    
    chatInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') sendBtn.click();
    });
});