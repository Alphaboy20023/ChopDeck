
const chatBtn = document.getElementById('chatBtn');
const chatModal = document.getElementById('chatModal');
const closeBtn = document.getElementById('closeBtn');
const sendBtn = document.getElementById('sendBtn');
const chatInput = document.getElementById('chatInput');
const chatArea = document.getElementById('chatArea');

chatBtn.addEventListener('click', () => {
  chatModal.classList.toggle('translate-x-full');
});

closeBtn.addEventListener('click', () => {
  chatModal.classList.add('translate-x-full');
});

const appendMessage = (sender, text) => {
  const div = document.createElement("div");
  div.className= sender === 'user' ? "flex justify-end" : "flex";
  div.innerHTML = `
  <div class="${sender === "user" ? "bg-blue-600 text-white rounded-2xl rounded-br-none" : "bg-gray-200 text-gray-800 rounded-2xl rounded-bl-none" } px-4 py-2 max-w-[80%]">
  ${text}
  </div>`;

  chatArea.appendChild(div);
  chatArea.scrollTop = chatArea.scrollHeight;

}

async function sendMessage() {
  const message = chatInput.value.trim();
  if (!message) return;

  appendMessage("user", message);
  chatInput.value = "";

  try {
    const response = await fetch("/api/chat/", {  // Call Django instead
      method: "POST",
      headers: { 
        "Content-Type": "application/json",
        // "X-CSRFToken": getCookie('csrftoken') 
      },
      body: JSON.stringify({message}),
    });

    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`);
    }

    const data = await response.json();
    if (data && data.length > 0) {
      data.forEach(msg => {
        if (msg.text) {
          appendMessage("bot", msg.text);
        }
      });
    }
  } catch (err) {
    console.error("Error:", err);
    appendMessage("bot", "Could not connect to the server");
  }
}

sendBtn.addEventListener("click", sendMessage);

// send to enter key
chatInput.addEventListener("keydown", e => {
  if (e.key === "Enter") sendMessage();
});


// to test paste "http://localhost:5005/webhooks/rest/webhook" and you should get 405

