const config = {
    initialMessages: [
      {
        text: "Hello! I can help you with fraud detection. How can I assist you?",
        id: 1,
      },
    ],
    botName: "FraudBot",
    customStyles: {
      botMessageBox: {
        backgroundColor: "#3b3b3b", // Dark gray for bot message box
        color: "#fff", // White text color
        borderRadius: "8px", // Rounded corners
        padding: "10px", // Padding for the message box
        fontSize: "16px", // Adjust font size for better readability
      },
      userMessageBox: {
        backgroundColor: "#4CAF50", // Green for user message box
        color: "#fff", // White text color
        borderRadius: "8px", // Rounded corners
        padding: "10px", // Padding for the user message box
        fontSize: "16px", // Adjust font size for better readability
      },
      chatButton: {
        backgroundColor: "#3b3b3b", // Dark button color
        borderRadius: "50%", // Circular button
        padding: "10px", // Add some padding for button size
        boxShadow: "0px 2px 6px rgba(0, 0, 0, 0.1)", // Subtle shadow effect
      },
      headerTitle: {
        color: "#4CAF50", // Green color for header
        fontSize: "18px", // Adjust font size for header
        fontWeight: "bold", // Bold header title
      },
      headerSubtitle: {
        color: "#fff", // White color for subtitle
        fontSize: "14px", // Subtitle font size
      },
      messageList: {
        padding: "20px", // Add padding to the message area
        backgroundColor: "#f5f5f5", // Light gray background for messages area
      },
      chatContainer: {
        border: "2px solid #4CAF50", // Border color for the entire chatbot container
        borderRadius: "10px", // Rounded corners for the container
        maxWidth: "500px", // Limit the chatbot width
        margin: "20px auto", // Center the chatbot
        overflow: "hidden", // Prevent elements from overflowing
        boxShadow: "0 4px 12px rgba(0, 0, 0, 0.1)", // Shadow for the container
      },
    },
  };
  
  export default config;