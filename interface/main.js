// Chatbot JS functionality

const messages = [];
const chatBox = document.getElementById("chat-box");
const messageBox = document.getElementById("messageBox");
const sendButton = document.getElementById("sendButton");
const newChatBtn = document.getElementById("newChatBtn");

// Initialize Chat
function initializer() {
  addMessage("Hello! I am Virtual Assistant, how can I help you today?", "Virtual Assistant", false);
  messageBox.disabled = false;
  sendButton.disabled = false;
}

function addMessage(content, sender, loading) {
  const timestamp = new Date();
  messages.push({ content, sender, loading, timestamp });
  renderMessages();
  scrollToBottom();
}

function renderMessages() {
  // Only re-render if the number of messages has changed
  const currentMessageCount = chatBox.children.length;
  const totalMessages = messages.length;

  if (currentMessageCount === totalMessages) {
    // Just update the last message if it's loading
    updateLastMessage();
    return;
  }

  // Full re-render only when necessary
  chatBox.innerHTML = "";
  messages.forEach((msg, index) => {
    const msgDiv = document.createElement("div");
    msgDiv.className = msg.sender === "You" ? "user-message-container chat-message-box" : "chatbot-message-container chat-message-box";
    msgDiv.dataset.messageIndex = index;

    msgDiv.innerHTML = `<span><b>${msg.sender}</b></span>
                        <span class="timestamp">${msg.timestamp.toLocaleTimeString()}</span>
                        <div class="loading-content-container">
                          ${msg.loading ? "<span class=\"loading-dots\"></span>" : `<span>${msg.content}</span>`}
                        </div>`;

    chatBox.appendChild(msgDiv);
  });
}

function updateLastMessage() {
  const lastMessageDiv = chatBox.lastElementChild;
  if (!lastMessageDiv) return;

  const lastMessage = messages[messages.length - 1];
  const loadingContainer = lastMessageDiv.querySelector('.loading-content-container');

  if (loadingContainer) {
    loadingContainer.innerHTML = lastMessage.loading ?
      "<span class=\"loading-dots\"></span>" :
      `<span>${lastMessage.content}</span>`;
  }
}

function scrollToBottom() {
  chatBox.scrollTop = chatBox.scrollHeight;
}

// Send message
function sendMessage() {
  const trimmedMessage = messageBox.value.trim();
  if (!trimmedMessage) return;
  addMessage(trimmedMessage, "You", false);
  addMessage("", "Virtual Assistant", true);

  messageBox.value = "";
  messageBox.style.height = "40px";

  fetch('http://localhost:5000/query_result', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({ prompt: trimmedMessage })
  })
  .then(res => res.json())
  .then(data => {
    messages[messages.length - 1].content = data.answer;
    messages[messages.length - 1].loading = false;
    updateLastMessage();
  })
  .catch(err => {
    messages[messages.length - 1].content = "Sorry, an error occurred.";
    messages[messages.length - 1].loading = false;
    updateLastMessage();
  });
}

// Textarea auto-expand
messageBox.addEventListener("input", () => {
  messageBox.style.height = "40px";
  messageBox.style.height = messageBox.scrollHeight + 2 + "px";
});

sendButton.addEventListener("click", sendMessage);
messageBox.addEventListener("keydown", (e) => {
  if (e.key === "Enter") {
    e.preventDefault();
    sendMessage();
  }
});

// New Chat
newChatBtn.addEventListener("click", () => {
  messages.length = 0;
  messageBox.disabled = false;
  sendButton.disabled = false;
  initializer();
});

// Initialize
initializer();
