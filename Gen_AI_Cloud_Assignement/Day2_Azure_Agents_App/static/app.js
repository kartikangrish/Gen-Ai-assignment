const endpoints = {
    chat: {
        url: "/api/chat",
        input: "chat-message",
        output: "chat-output",
        bodyKey: "message",
    },
    policy: {
        url: "/api/policy-helper",
        input: "policy-question",
        output: "policy-output",
        bodyKey: "question",
    },
    rent: {
        url: "/api/house-rent",
        input: "rent-query",
        output: "rent-output",
        bodyKey: "query",
    },
};

async function runAgent(agentName) {
    const config = endpoints[agentName];
    const input = document.getElementById(config.input);
    const output = document.getElementById(config.output);
    const text = input.value.trim();

    if (!text) {
        output.textContent = "Please enter a question first.";
        return;
    }

    output.textContent = "Working...";

    try {
        const response = await fetch(config.url, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ [config.bodyKey]: text }),
        });
        const data = await response.json();

        if (!response.ok) {
            output.textContent = data.error || "Request failed.";
            return;
        }

        output.textContent = data.answer;
    } catch (error) {
        output.textContent = error.message;
    }
}

document.querySelectorAll("button[data-agent]").forEach((button) => {
    button.addEventListener("click", () => runAgent(button.dataset.agent));
});