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
Before running the Database Chatbot, ensure you configure the necessary database connection details in a .env file. Create a .env file in the root of your project and add the following variables:

env
Copy code
# Database Configuration
DB_SERVER=your_database_server
DB_NAME=your_database_name
DB_USER=your_database_user
DB_PASSWORD=your_database_password

# Azure Keys
AZURE_SUBSCRIPTION_KEY=your_azure_subscription_key
AZURE_REGION=your_azure_region
Replace your_database_server, your_database_name, your_database_user, your_database_password, your_azure_subscription_key, and your_azure_region with your actual database and Azure subscription information.

Running the Database Chatbot
Now that your local machine's IP address is configured in the Azure database server and your database connection details are set in the .env file, you can run the Database Chatbot with confidence. Ensure that you have the necessary dependencies installed and execute the application.

Contributing
We welcome contributions! If you find any issues or have suggestions for improvement, please open an issue or submit a pull request.
