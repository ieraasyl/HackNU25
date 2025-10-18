"use client";

import { Box, ScrollArea } from "@mantine/core";
import { ChatMessage, type Message } from "./chat-message";
import { ChatInput } from "./chat-input";
import { ChatHeader } from "./chat-header";

// Mock data
const mockMessages: Message[] = [
  {
    id: "1",
    content: "Hello! How can I help you today?",
    role: "assistant",
    timestamp: new Date(Date.now() - 1000 * 60 * 5),
  },
  {
    id: "2",
    content: "I need help with my account settings",
    role: "user",
    timestamp: new Date(Date.now() - 1000 * 60 * 4),
  },
  {
    id: "3",
    content:
      "I'd be happy to help you with your account settings. What specifically would you like to change?",
    role: "assistant",
    timestamp: new Date(Date.now() - 1000 * 60 * 3),
  },
  {
    id: "4",
    content: "I want to update my email address",
    role: "user",
    timestamp: new Date(Date.now() - 1000 * 60 * 2),
  },
];

export function Chatbot() {
  const handleSendMessage = (message: string) => {
    console.log("Sending message:", message);
    // State management will be added later
  };

  return (
    <Box
      style={{
        width: "100vw",
        height: "100vh",
        margin: "0 auto",
        display: "flex",
        flexDirection: "column",
        border: "1px solid #e9ecef",
        borderRadius: "12px",
        overflow: "hidden",
        backgroundColor: "white",
        boxShadow: "0 2px 8px rgba(0, 0, 0, 0.1)",
      }}
    >
      <ChatHeader />

      <ScrollArea
        style={{
          flex: 1,
          backgroundColor: "#f8f9fa",
        }}
      >
        <Box style={{ padding: "8px 0" }}>
          {mockMessages.map((message) => (
            <ChatMessage key={message.id} message={message} />
          ))}
        </Box>
      </ScrollArea>

      <ChatInput onSend={handleSendMessage} />
    </Box>
  );
}
