let isProcessing = false;

document.addEventListener('DOMContentLoaded', function() {
    const messageInput = document.getElementById('messageInput');
    
    messageInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });
    
    // Remove welcome message and add initial bot message
    setTimeout(() => {
        addMessage(`Hello! I'm your MCP Medical Assistant connected to the live database.

I can help you with:
• **Search patients**: "Show all patients" or "Find patient John Smith"
• **Patient details**: "Get details for patient 123"
• **Filtered searches**: "Find patients by Dr. Johnson"

Try asking: "Show all patients" to see all patients in the database!`, 'bot');
    }, 500);
});

function sendMessage() {
    if (isProcessing) return;
    
    const input = document.getElementById('messageInput');
    const message = input.value.trim();
    
    if (!message) return;
    
    addMessage(message, 'user');
    input.value = '';
    isProcessing = true;
    
    // Show typing indicator
    const typingDiv = document.createElement('div');
    typingDiv.className = 'message bot-message typing-indicator';
    typingDiv.innerHTML = `
        <div class="message-avatar">🤖</div>
        <div class="message-content">
            <div class="message-bubble">
                <div class="typing-dots">
                    <span></span><span></span><span></span>
                </div>
            </div>
        </div>
    `;
    document.getElementById('chatMessages').appendChild(typingDiv);
    scrollToBottom();
    
    fetch('/chat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: message }),
        timeout: 30000  // 30 second timeout
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`Server error: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        typingDiv.remove();
        
        if (data.response) {
            addMessage(data.response, 'bot');
        } else {
            addMessage('❌ Sorry, I received an empty response. Please try again.', 'bot');
        }
    })
    .catch(error => {
        typingDiv.remove();
        console.error('Error:', error);
        
        let errorMessage = '❌ Sorry, I encountered an error. ';
        if (error.message.includes('502')) {
            errorMessage += 'The server is temporarily unavailable. Please try again in a moment.';
        } else if (error.message.includes('timeout')) {
            errorMessage += 'The request timed out. Please try a simpler question.';
        } else {
            errorMessage += 'Please try again.';
        }
        
        addMessage(errorMessage, 'bot');
    })
    .finally(() => {
        isProcessing = false;
    });
}

function sendQuickMessage(message) {
    if (isProcessing) return;
    
    document.getElementById('messageInput').value = message;
    sendMessage();
}

function addMessage(message, sender) {
    const chatMessages = document.getElementById('chatMessages');
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}-message`;
    messageDiv.style.animation = 'fadeIn 0.3s ease-in';
    
    const isUser = sender === 'user';
    const avatarBg = isUser ? '#3182ce' : '#4a5568'; /* Blue for user, gray for bot */
    const messageBg = isUser ? '#3182ce' : '#ffffff'; /* Blue for user, white for bot */
    const textColor = isUser ? '#ffffff' : '#2d3748'; /* White for user, dark for bot */
    const avatar = isUser ? '👤' : '🤖';
    
    // Format the message content
    const formattedMessage = formatMessage(message);
    
    // Use full width for tables with 13 columns
    const messageWidth = formattedMessage.includes('patient-table') ? '98%' : '70%';
    
    messageDiv.innerHTML = `
        <div class="message-avatar" style="width: 36px; height: 36px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 16px; background: ${avatarBg}; color: white; ${isUser ? 'margin-left: 12px;' : 'margin-right: 12px;'} flex-shrink: 0;">
            ${avatar}
        </div>
        <div class="message-content" style="max-width: ${messageWidth}; width: ${messageWidth}; background: ${messageBg}; border: 1px solid #e2e8f0; border-radius: 16px; padding: 16px 20px;">
            <div class="message-bubble" style="color: ${textColor}; line-height: 1.5;">
                ${formattedMessage}
            </div>
        </div>
    `;
    
    if (isUser) {
        messageDiv.style.flexDirection = 'row-reverse';
    }
    
    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function formatMessage(content) {
    // Check if content is already HTML table - don't double format
    if (content.includes('<table class="patient-table">')) {
        return content; // Return as-is for HTML tables
    }
    
    // Enhanced formatting for regular text messages
    let formatted = content
        .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
        .replace(/\*(.*?)\*/g, '<em>$1</em>')
        .replace(/`(.*?)`/g, '<code>$1</code>');
    
    // Only add <br> for non-HTML content that doesn't already have HTML tags
    if (!formatted.includes('<table>') && !formatted.includes('<div>') && !formatted.includes('<br>')) {
        formatted = formatted.replace(/\n/g, '<br>');
    }
    
    return formatted;
}

function convertToHTMLTable(content) {
    const lines = content.split('<br>');
    let tableHTML = '';
    let inTable = false;
    let headers = [];
    
    for (let i = 0; i < lines.length; i++) {
        const line = lines[i].trim();
        
        if (line.includes('|') && !line.includes('---')) {
            if (!inTable) {
                // Start table
                tableHTML += '<table class="patient-table"><thead><tr>';
                headers = line.split('|').map(h => h.trim()).filter(h => h);
                headers.forEach(header => {
                    tableHTML += `<th>${header}</th>`;
                });
                tableHTML += '</tr></thead><tbody>';
                inTable = true;
            } else {
                // Table row
                const cells = line.split('|').map(c => c.trim()).filter(c => c);
                if (cells.length > 0) {
                    tableHTML += '<tr>';
                    cells.forEach(cell => {
                        tableHTML += `<td>${cell}</td>`;
                    });
                    tableHTML += '</tr>';
                }
            }
        } else if (line.includes('---') && inTable) {
            // Skip separator line
            continue;
        } else {
            if (inTable) {
                // End table
                tableHTML += '</tbody></table>';
                inTable = false;
            }
            if (line) {
                tableHTML += line + '<br>';
            }
        }
    }
    
    if (inTable) {
        tableHTML += '</tbody></table>';
    }
    
    return tableHTML;
}

function scrollToBottom() {
    const messagesContainer = document.getElementById('chatMessages');
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}







