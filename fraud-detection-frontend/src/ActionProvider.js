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
      const response = await axios.post("http://localhost:8001/chat", {
        user_message: userMessage,
      });

      const botMessage = response.data.bot_message;

      // Create a message for the bot response
      const message = this.createChatBotMessage(botMessage);
      this.setState((prevState) => ({
        ...prevState,
        messages: [...prevState.messages, message],
      }));
    } catch (error) {
      console.error("Error with OpenAI API:", error);
      const errorMessage = this.createChatBotMessage(
        "Sorry, I encountered an error. Please try again later."
      );
      this.setState((prevState) => ({
        ...prevState,
        messages: [...prevState.messages, errorMessage],
      }));
    }
  }
}

export default ActionProvider;