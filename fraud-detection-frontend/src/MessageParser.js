class MessageParser {
    constructor(actionProvider) {
      this.actionProvider = actionProvider;
    }
  
    parse(message) {
      // Here, you can add more logic for parsing user input if needed
      this.actionProvider.handleUserMessage(message);
    }
  }
  
  export default MessageParser;