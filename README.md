Database Chatbot
Introduction
Welcome to the Database Chatbot project! This innovative solution leverages the power of Azure OpenAI services to provide a seamless and efficient way to interact with your database using natural language.

Setup Instructions
Prerequisites
Before you begin, make sure you have the following:

Azure account
Access to the Azure portal
Database server created on Azure
Configuring IP Address for Local Machine
To run the Database Chatbot from your local machine, you need to add the IP address of your machine to the Azure database server. Follow these steps:

Open the Azure portal and navigate to your database.

Click on "Set up server firewall."
In the firewall settings, locate the option to "Add your client IP address."
Enter your machine's IPv4 address in the provided field.

Click "Save" to apply the changes.

Configuring Database Connection Details
Before running the Database Chatbot, ensure you configure the necessary database connection details in a .env file. Create a .env file in the root of your project and configure the required variables.

Running the Database Chatbot
To execute the Database Chatbot, run the following command in your terminal:

bash
Copy code : python streamlit_app.py
Ensure that you have the necessary dependencies installed, and the application will launch. Visit the provided URL in your browser to interact with the Database Chatbot.

Contributing
We welcome contributions! If you find any issues or have suggestions for improvement, please open an issue or submit a pull request.
