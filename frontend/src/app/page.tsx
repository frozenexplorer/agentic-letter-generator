"use client";
import { useState } from "react";
import axios from "axios";
const BACKEND_URI =
  process.env.NEXT_PUBLIC_BACKEND_URI || "https://random-production.up.railway.app";
export default function Home() {
  const [chat, setChat] = useState<{ sender: string; text: string }[]>([]);
  const [input, setInput] = useState("");
  const [darkMode, setDarkMode] = useState(true);

  const extractNameFromMessage = (message: string): string | null => {
    const pattern = /(?:for|generate offer for|create offer for)\s+(.*)/i;
    const match = message.match(pattern);
    return match ? match[1].trim() : null;
  };

  const handleSend = async () => {
    const userMessage = input.trim();
    if (!userMessage) return;

    setChat((prev) => [...prev, { sender: "user", text: userMessage }]);
    setInput("");

    const extractedName = extractNameFromMessage(userMessage);
    if (!extractedName) {
      setChat((prev) => [
        ...prev,
        {
          sender: "bot",
          text: "❌ Please say something like: 'Generate offer for John Doe'",
        },
      ]);
      return;
    }

    setChat((prev) => [
      ...prev,
      {
        sender: "bot",
        text: `🔄 Generating offer letter for ${extractedName}...`,
      },
    ]);

    try {
      const res = await axios.post(`${BACKEND_URI}/generate-offer`, {
        name: extractedName,
      });

      if (res.data.success) {
        const links = res.data.paths;
        setChat((prev) => [
          ...prev,
          {
            sender: "bot",
            text: `✅ Offer letter generated for <strong>${extractedName}</strong><br><br>
            📄 <a href="${BACKEND_URI}/files/${links.pdf}" download=${links.pdf}  target="_blank">Download PDF</a><br>
            📄 <a href="${BACKEND_URI}/files/${links.txt}" download=${links.pdf}  target="_blank">View Text</a>`,
          },
        ]);
      } else {
        setChat((prev) => [
          ...prev,
          {
            sender: "bot",
            text: `❌ No employee found named "${extractedName}".`,
          },
        ]);
      }
    } catch (error) {
      console.log("Error : ", error);
      setChat((prev) => [
        ...prev,
        { sender: "bot", text: `❌ Error generating the offer letter.` },
      ]);
    }
  };

  return (
    <main
      style={{
        fontFamily: "sans-serif",
        background: darkMode ? "#1e293b" : "#f8fafc",
        minHeight: "100vh",
        padding: "2rem",
        color: darkMode ? "#f8fafc" : "#1e293b",
        transition: "all 0.3s ease",
      }}
    >
      <div
        style={{
          maxWidth: "700px",
          margin: "0 auto",
          background: darkMode ? "#0f172a" : "#ffffff",
          padding: "2rem",
          borderRadius: "12px",
          boxShadow: "0 4px 20px rgba(0,0,0,0.08)",
        }}
      >
        <div
          style={{
            display: "flex",
            justifyContent: "space-between",
            marginBottom: "1rem",
          }}
        >
          <h2 style={{ fontSize: "1.5rem" }}>🤖 HR Chat Assistant</h2>
          <button
            onClick={() => setDarkMode(!darkMode)}
            style={{
              padding: "0.5rem 1rem",
              background: "transparent",
              border: "1px solid gray",
              borderRadius: "6px",
              cursor: "pointer",
              color: darkMode ? "#f8fafc" : "#1e293b",
            }}
          >
            {darkMode ? "🌙 Dark" : "🌞 Light"}
          </button>
        </div>

        <div
          style={{
            background: darkMode ? "#1e293b" : "#f1f5f9",
            padding: "1rem",
            height: "350px",
            overflowY: "auto",
            marginBottom: "1rem",
            borderRadius: "8px",
            border: "1px solid #ccc",
          }}
        >
          {chat.map((msg, idx) => (
            <div
              key={idx}
              style={{
                textAlign: msg.sender === "user" ? "right" : "left",
                marginBottom: "1rem",
              }}
            >
              <div
                style={{
                  display: "inline-block",
                  background:
                    msg.sender === "user"
                      ? "#3b82f6"
                      : darkMode
                      ? "#334155"
                      : "#e2e8f0",
                  color:
                    msg.sender === "user"
                      ? "#fff"
                      : darkMode
                      ? "#f8fafc"
                      : "#000",
                  padding: "0.75rem 1rem",
                  borderRadius: "10px",
                  maxWidth: "80%",
                }}
                dangerouslySetInnerHTML={{
                  __html: msg.text.replace(/\n/g, "<br>"),
                }}
              />
            </div>
          ))}
        </div>

        <div style={{ display: "flex", gap: "0.5rem" }}>
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="e.g., Generate offer for Martha Bennett"
            style={{
              flex: 1,
              padding: "0.75rem",
              borderRadius: "8px",
              border: "1px solid gray",
              fontSize: "1rem",
            }}
          />
          <button
            onClick={handleSend}
            style={{
              padding: "0.75rem 1.5rem",
              backgroundColor: "#3b82f6",
              color: "#fff",
              borderRadius: "8px",
              border: "none",
              cursor: "pointer",
            }}
          >
            Send
          </button>
        </div>
      </div>
    </main>
  );
}
