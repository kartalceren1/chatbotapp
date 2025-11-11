const answerForm = document.getElementById("chat-form");
const chatInput = document.getElementById("answer");
const chatBox = document.querySelector(".chatbox");

// Helper function to create chat messages for both user and assistant
function createChat(message, type, label = "") {
    const li = document.createElement("li");
    li.classList.add(type);

    const chatBody = document.createElement("div");
    chatBody.classList.add("chat-body");

    if (label) {
        const header = document.createElement("strong");
        header.textContent = label;
        chatBody.appendChild(header);
    }

    const text = document.createElement("p");
    text.textContent = message;
    chatBody.appendChild(text);

    li.appendChild(chatBody);
    return li;
}

answerForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    const question = document.getElementById("question").textContent;
    const persona = document.getElementById("persona").value;
    const answer = chatInput.value.trim();
    if (!answer) return;

    // Append user message
    const userChat = createChat(answer, "right", "You:");
    chatBox.querySelector(".chat").appendChild(userChat);
    chatInput.value = "";

    try {

        const aiResponse = await fetch("/evaluate", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ persona, question, answer })
        });

        const data = await aiResponse.json();
        const aiReply = data.reply || "No response from assistant.";
        const personaLabel = persona.charAt(0).toUpperCase() + persona.slice(1);

        // Append assistant message
        const aiChat = createChat(aiReply, "left", personaLabel + ":");
        chatBox.querySelector(".chat").appendChild(aiChat);

        chatBox.scrollTop = chatBox.scrollHeight;

    } catch (error) {
        console.error(error);
        const errorBubble = createChat("Error contacting server.", "left", personaLabel + ":");
        chatBox.querySelector(".chat").appendChild(errorBubble);
    }
});


