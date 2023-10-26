from dotenv import load_dotenv
import os
import openai
from prompts import prompt3,prompt1
from utils.Logger import logging


load_dotenv()

openai.api_type = "azure"
openai.api_base = os.getenv("OPENAI_API_BASE") 
openai.api_version = "2023-07-01-preview"
openai.api_key = os.getenv("OPENAI_API_KEY")


system_message = prompt3.SYSTEM_MESSAGE_ERROR

making_query_correct_messages = [
        {'role': 'system', 'content': system_message},
        {'role': 'user', 'content': 'SELECT customers.customer_id, customers.first_name, customers.last_name, COUNT(order_items.item_id) AS total_purchases FROM customers JOIN orders ON customers.customer_id = orders.customer_id JOIN order_items ON orders.order_id = order_items.order_id GROUP BY customers.customer_id ORDER BY total_purchases DESC'},
        {'role': 'user', 'content': 'customers.first_name is invalid in the select list because it is not contained in either an aggregate function or the GROUP BY clause.'},
        {'role': 'assistant', 'content': 'SELECT customers.customer_id, MAX(customers.first_name) AS first_name, MAX(customers.last_name) AS last_name, COUNT(order_items.item_id) AS total_purchases FROM customers JOIN orders ON customers.customer_id = orders.customer_id JOIN order_items ON orders.order_id = order_items.order_id GROUP BY customers.customer_id ORDER BY total_purchases DESC'},

        {'role': 'user', 'content': 'SELECT stores.store_id, stores.store_name, COUNT(orders.order_id) AS total_orders FROM stores JOIN orders ON stores.store_id = orders.store_id GROUP BY stores.store_id ORDER BY total_orders DESC LIMIT 1'},
        {'role': 'user', 'content': 'Incorrect syntax near \'LIMIT\'.'},
        {'role': 'assistant', 'content': 'SELECT TOP 1 s.store_id, s.store_name, COUNT(o.order_id) as order_count FROM stores s INNER JOIN orders o ON s.store_id = o.store_id GROUP BY s.store_id, s.store_name ORDER BY order_count DESC'},
        
        
    ]
    

## initializing a ChatCompletion Model to genrate Sql Query.
def get_completion_from_messages(messages, model="gpt-35-turbo-16k", temperature=0, max_tokens=500) -> str:
    
    
    messages = messages
    
    response = openai.ChatCompletion.create(
        engine=model,
        messages=messages,
        temperature=temperature, 
        max_tokens=max_tokens, 
     
        
    ) 
    return response.choices[0].message["content"]


## initializing a CorrectSqlQuery function to create a  Model to re-genrate correct Sql Query 
def CorrectSqlQuery(model_query,model_error) -> str:
  
  making_query_correct_messages.append({'role': 'user', 'content': f"{model_query}"})
  making_query_correct_messages.append({'role': 'user', 'content': f"{model_error}"})

  response = get_completion_from_messages(making_query_correct_messages,temperature=0.3)
  
  logging.info(response)
  
  return response
    
    

## initializing a ResultToSummary function to create  Model to re-genrate correct Sql Query  
def ResultToSummary(user_message,SqlResult):
    formatted_system_message_db = prompt1.db_prompt_1.format(question=user_message,table=SqlResult)
    
    
    messages_db = [
       {'role': 'system', 'content': formatted_system_message_db},
       {'role': 'user', 'content': 'Give Proper Humman Understatable response'},
        
    ]
    
    ModelResponse = get_completion_from_messages(messages_db)
    
    return ModelResponse
    
    
    

if __name__ == "__main__":
    system_message = "You are a AI assistant"
    user_message = "Hello"
    print(get_completion_from_messages(system_message, user_message))