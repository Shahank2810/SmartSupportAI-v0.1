  import { useState, useRef, useEffect } from "react";
  import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
  import { Button } from "@/components/ui/button";
  import { Input } from "@/components/ui/input";
  import { Badge } from "@/components/ui/badge";
  import { User, Bot, Paperclip, Send, Smile, MoreVertical } from "lucide-react";
  import { apiRequest } from "@/lib/queryClient";
  import { useToast } from "@/hooks/use-toast";
  import type { Message, Conversation } from "@shared/schema";

  interface ChatInterfaceProps {
    conversationId: number;
    conversation?: Conversation;
  }

  export default function ChatInterface({ conversationId, conversation }: ChatInterfaceProps) {
    const [messageInput, setMessageInput] = useState("");
    const [isTyping, setIsTyping] = useState(false);
    const messagesEndRef = useRef<HTMLDivElement>(null);
    const queryClient = useQueryClient();
    const { toast } = useToast();

    const { data: messages, isLoading } = useQuery({
      queryKey: ["/api/conversations", conversationId, "messages"],
      enabled: !!conversationId,
    });

    const sendMessageMutation = useMutation({
      mutationFn: async (content: string) => {
        const response = await apiRequest("POST", `/api/conversations/${conversationId}/messages`, {
          content,
          sender: "customer",
        });
        return response.json();
      },
      onSuccess: () => {
        queryClient.invalidateQueries({ queryKey: ["/api/conversations", conversationId, "messages"] });
        setMessageInput("");
        setIsTyping(true);
        
        // Simulate AI response delay
        setTimeout(() => {
          setIsTyping(false);
          queryClient.invalidateQueries({ queryKey: ["/api/conversations", conversationId, "messages"] });
        }, 2000);
      },
      onError: () => {
        toast({
          title: "Error",
          description: "Failed to send message. Please try again.",
          variant: "destructive",
        });
      },
    });

    const handleSendMessage = () => {
      if (messageInput.trim() && !sendMessageMutation.isPending) {
        sendMessageMutation.mutate(messageInput.trim());
      }
    };

    const handleKeyPress = (e: React.KeyboardEvent) => {
      if (e.key === "Enter" && !e.shiftKey) {
        e.preventDefault();
        handleSendMessage();
      }
    };

    useEffect(() => {
      messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    }, [messages, isTyping]);

    const formatTime = (timestamp: string) => {
      return new Date(timestamp).toLocaleTimeString("en-US", {
        hour: "numeric",
        minute: "2-digit",
        hour12: true,
      });
    };

    return (
      <div className="flex-1 flex flex-col bg-white">
        {/* Chat Header */}
        <div className="border-b border-border px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <div className="w-10 h-10 bg-gradient-to-br from-primary to-blue-600 rounded-full flex items-center justify-center">
                <User className="text-primary-foreground" size={20} />
              </div>
              <div>
                <h3 className="font-semibold text-foreground">
                  {conversation?.customerName || "Customer"}
                </h3>
                <p className="text-sm text-muted-foreground">
                  {conversation?.customerEmail || "Customer since March 2024"}
                </p>
              </div>
            </div>
            <div className="flex items-center space-x-2">
              <Badge 
                variant="secondary" 
                className="bg-secondary/10 text-secondary hover:bg-secondary/20"
              >
                {conversation?.status || "Active"}
              </Badge>
              <Button variant="ghost" size="icon" className="text-muted-foreground">
                <MoreVertical size={16} />
              </Button>
            </div>
          </div>
        </div>

        {/* Chat Messages */}
        <div className="flex-1 overflow-y-auto p-6 space-y-4">
          {isLoading ? (
            <div className="flex justify-center py-8">
              <div className="text-muted-foreground">Loading conversation...</div>
            </div>
          ) : (
            <>
              {messages?.map((message: Message) => (
                <div
                  key={message.id}
                  className={`flex items-start space-x-3 ${
                    message.sender === "ai" ? "flex-row-reverse" : ""
                  }`}
                >
                  <div className="w-8 h-8 rounded-full flex items-center justify-center flex-shrink-0">
                    {message.sender === "ai" ? (
                      <div className="w-8 h-8 bg-primary rounded-full flex items-center justify-center">
                        <Bot className="text-primary-foreground" size={16} />
                      </div>
                    ) : (
                      <div className="w-8 h-8 bg-muted rounded-full flex items-center justify-center">
                        <User className="text-muted-foreground" size={16} />
                      </div>
                    )}
                  </div>
                  <div className={`flex-1 ${message.sender === "ai" ? "flex flex-col items-end" : ""}`}>
                    <div className={`message-bubble ${message.sender}`}>
                      <p className="text-sm leading-relaxed">{message.content}</p>
                    </div>
                    <p className="text-xs text-muted-foreground mt-2">
                      {formatTime(message.timestamp)}
                      {message.metadata?.confidence && (
                        <span className="ml-2">
                          • {Math.round(message.metadata.confidence * 100)}% confidence
                        </span>
                      )}
                    </p>
                  </div>
                </div>
              ))}

              {isTyping && (
                <div className="flex items-start space-x-3 flex-row-reverse">
                  <div className="w-8 h-8 bg-primary rounded-full flex items-center justify-center flex-shrink-0">
                    <Bot className="text-primary-foreground" size={16} />
                  </div>
                  <div className="flex-1 flex flex-col items-end">
                    <div className="bg-primary/10 border border-primary/20 rounded-2xl rounded-tr-sm p-4 max-w-md">
                      <div className="typing-indicator">
                        <div className="typing-dot animate-bounce-1"></div>
                        <div className="typing-dot animate-bounce-2"></div>
                        <div className="typing-dot animate-bounce-3"></div>
                      </div>
                    </div>
                    <p className="text-xs text-muted-foreground mt-2">AI is typing...</p>
                  </div>
                </div>
              )}
              <div ref={messagesEndRef} />
            </>
          )}
        </div>

        {/* Message Input */}
        <div className="border-t border-border p-4">
          <div className="flex items-center space-x-3">
            <Button variant="ghost" size="icon" className="text-muted-foreground">
              <Paperclip size={16} />
            </Button>
            <div className="flex-1 relative">
              <Input
                value={messageInput}
                onChange={(e) => setMessageInput(e.target.value)}
                onKeyPress={handleKeyPress}
                placeholder="Type your message..."
                className="pr-12"
                disabled={sendMessageMutation.isPending}
              />
              <Button
                onClick={handleSendMessage}
                variant="ghost"
                size="icon"
                className="absolute right-1 top-1/2 transform -translate-y-1/2 text-muted-foreground hover:text-primary"
                disabled={!messageInput.trim() || sendMessageMutation.isPending}
              >
                <Send size={16} />
              </Button>
            </div>
            <Button variant="ghost" size="icon" className="text-muted-foreground">
              <Smile size={16} />
            </Button>
          </div>
        </div>
      </div>
    );
  }
