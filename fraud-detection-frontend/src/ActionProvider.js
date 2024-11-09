import axios from "axios";

class ActionProvider {
  constructor(createChatBotMessage, setStateFunc) {
    this.createChatBotMessage = createChatBotMessage;
    this.setState = setStateFunc;
  }

  // Handle the user message and call the OpenAI backend
  async handleUserMessage(userMessage) {
    try {
      // Send the user message to the backend
      // Changed user_message to message to match the backend Pydantic model
      const response = await axios.post("http://localhost:8001/chat", {
        message: userMessage,
      });

      // Changed bot_message to response to match the backend response format
      const botMessage = response.data.response;

      // Create a message for the bot response
      const message = this.createChatBotMessage(botMessage);

      this.setState((prevState) => ({
        ...prevState,
        messages: [...prevState.messages, message],
      }));
    } catch (error) {
      console.error("Error with OpenAI API:", error);
    }
  }
}

export default ActionProvider;