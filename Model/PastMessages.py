from prompts import prompt,prompt1,prompt3
from DBFiles.Database import get_schema_representation



# Schema of the database
schemas = get_schema_representation()



# Format the system message with the schema
formatted_system_message = prompt.SYSTEM_MESSAGE_1.format(schema=schemas)



## Few Shot Examples for  User Assistant Chat for the Model.
messages = [
          {'role': 'system', 'content': formatted_system_message},
          {'role': 'user', 'content': 'Show me all stores'},
          {'role': 'assistant', 'content': '{ "query": "SELECT * FROM stores", "error": null}'},


          {'role': 'user', 'content': 'Hello,How are you?'},
          {'role': 'assistant', 'content': '{ "query": null, "error": "I\'m your AI Assistant how can i Help you to query Bike Store Database"}'},

          {'role': 'user', 'content': 'What is the weather today'},
          {'role': 'assistant', 'content': '{ "query": null, "error": "I dont have Idea on external data"}'},


          {'role': 'user', 'content': 'Write a SQL query to update the name column in the customers table to John Doe for all customers whose id is 12345.'},
            {'role': 'assistant', 'content': '{ "query": "UPDATE customers SET first_name = "John", last_name = "Doe" WHERE customer_id = 12345", "error": null}'},
            
            {'role': 'user', 'content': 'on whcih store the employee kali is working'},
            {'role': 'assistant', 'content': '{ "query": "SELECT store_name FROM stores WHERE store_id IN (SELECT store_id FROM staffs WHERE first_name = \'Kali\')", "error": null}'},
            
            {'role': 'user', 'content': 'calculate the total number of orders placed by  customer  Johnathan Velazquez'},
            {'role': 'assistant', 'content': '{ "query": "SELECT COUNT(*) FROM orders WHERE customer_id IN (SELECT customer_id FROM customers WHERE first_name = \'Johnathan\' AND last_name = \'Velazquez\')", "error": null}'},
            
          {'role': 'user', 'content': 'Hi'},
          {'role': 'assistant', 'content': '{ "query": null, "error": "I\'m your AI Assistant how can i Help you to query Bike Store Database"}'},


            {'role': 'user', 'content': 'Which customers have purchased the most products?'},
            {'role': 'assistant', 'content': '{ "query": "SELECT c.first_name, c.last_name, COUNT(*) as total_products_purchased FROM customers c INNER JOIN orders o ON c.customer_id = o.customer_id INNER JOIN order_items oi ON o.order_id = oi.order_id GROUP BY c.first_name, c.last_name ORDER BY total_products_purchased DESC", "error": null}'},
            
            {'role': 'user', 'content': 'get the name of the employee who has the most sales.'},
            {'role': 'assistant', 'content': '{ "query": "SELECT TOP 1 s.first_name, s.last_name, COUNT(*) as total_sales FROM staffs s INNER JOIN orders o ON s.staff_id = o.staff_id GROUP BY s.first_name, s.last_name ORDER BY total_sales DESC", "error": null}'},
            
            {'role': 'user', 'content': 'The name of all products that have been ordered more than 10 times.'},
            {'role': 'assistant', 'content': '{ "query": "SELECT p.product_name FROM products p INNER JOIN order_items oi ON p.product_id = oi.product_id GROUP BY p.product_name HAVING COUNT(*) > 10", "error": null}'},
            
            {'role': 'user', 'content': 'Find the total quantity of all products available in all stores.'},
            {'role': 'assistant', 'content': '{ "query": "SELECT SUM(quantity) as total_quantity FROM stocks", "error": null}'},
            
            
            {'role': 'user', 'content': 'what is the staff name who has sold more products of Electra Girl\'s Hawaii 1 (16-inch) - 2015/2016 in the store Santa Cruz Bikes'},
            {'role': 'assistant', 'content': '{ "query": "SELECT s.first_name, s.last_name, COUNT(*) as total_sales FROM staffs s INNER JOIN orders o ON s.staff_id = o.staff_id INNER JOIN order_items oi ON o.order_id = oi.order_id INNER JOIN products p ON oi.product_id = p.product_id INNER JOIN stores st ON o.store_id = st.store_id WHERE p.product_name = \'Electra Girl\'s Hawaii 1 (16-inch) - 2015/2016\' AND st.store_name = \'Santa Cruz Bikes\' GROUP BY s.first_name, s.last_name ORDER BY total_sales DESC", "error": null}'}
            
          
      ]


## It will remember past 10 messages in the list.
def get_past_messages(n=20,USER_MESSAGE=""):
  
  message={'role': 'assistant', 'content': f"{USER_MESSAGE}"}
  messages.append(message)
  if len(messages) > (n*2):
    del messages[1:3]
    return messages
  else:
    return messages
    

def add_message(message=""):
  messages.append(message)
  