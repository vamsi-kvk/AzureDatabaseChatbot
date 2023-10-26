import pandas as pd
from DBFiles.Database import query_database
from Model.PastMessages import add_message, get_past_messages
from Model.AzureOpenAi import  ResultToSummary, get_completion_from_messages
from utils.Logger import logging
import streamlit as st
from utils.Converter import ResponseToQuerry
from utils.utils import convert_df


def LaunchUI():
        
    ##---------- Getting started with streamlit ----------------------  # 

    st.title(" Query Bike Store DataBase")
    st.write("Enter your message to generate SQL results.")

    ## initializing a empty list to store the history of the Chat Bot
    if "st_messages" not in st.session_state:
        st.session_state.st_messages = []
        
    #  iterating over a list of chat messages stored in the st_messages attribute
    for message in st.session_state.st_messages:
        with st.chat_message(message["role"]):
            # st.markdown function to display the content of the message.
            st.markdown(message["content"])



    ## Taking user input from the UI
    if user_message := st.chat_input("Enter your query?"):
        
    
    
         # Display user message in chat message container
        st.chat_message("user").markdown(user_message)
        ## Adding the user message to the Message List to store the previous Messages.
        st.session_state.st_messages.append({"role":"user","content":user_message})
        
        
        ## Adding the user message to the Message List to store the previous Messages.
        # default the past mesages value is set to 10 "n=10"
        logging.info("The question asked by the user{}".format({'role': 'user', 'content': f"{user_message}"}))
        
        # Get The Messages list to pass into the  Model
        messages = get_past_messages(USER_MESSAGE = user_message)
        
        # TO use Gpt-3 Model Response
        # The Model returns response as a  Json Format, Ex :  { "query": "SELECT * FROM stores", "error": null}
        response = get_completion_from_messages(messages,temperature=0.45)   
         
         
        logging.info("The response genrated by the Model {}".format({'role': 'assistant', 'content': f"{response}"}))
        
        ## Adding Model genrated response To the Messages list.
        add_message(message={'role': 'assistant', 'content': f"{response}"})

        
        ## After getting a Json response from the Model, Will pass to the ResponseToQuerry Function, To seprate error message and query from the Model
        FinalQuerry,MessagefromModel = ResponseToQuerry(response)
        
        logging.info(FinalQuerry)

        # If the error message is none then passing it to query_database function to execute it.
        if MessagefromModel is None: 
            ## After getting querry Then passing it to query_database function, to execute the query in the database.
            sql_results = query_database(FinalQuerry)
            
            logging.info("The result genrated by sql {}".format(sql_results))
            
            ## Passing the UserMessage and Sql result(data Frame)  to the Model To Summerize it.
            output = ResultToSummary(user_message,sql_results)
            
            ## Display Model message in chat message container
            st.chat_message("assistant").markdown(output)
            
            # adding Messages to session List
            st.session_state.st_messages.append({"role":"assistant","content":output})
                
            # Converting DataFrame TO CSV    
            csv = convert_df(sql_results)   
            if csv is not None:
                st.download_button(
                    label="Click Here get CSV",
                    data=csv,
                    file_name="sql_results.csv",
                    key="sql_results_download_button",
                )
        ## This triggers when there is an error while genrating sql query                 
        else :
            logging.info("The Message from the Model {}".format(MessagefromModel))
            print("CHATBOT :",MessagefromModel)
            st.chat_message("assistant").markdown(MessagefromModel)
            st.session_state.st_messages.append({"role":"assistant","content":MessagefromModel})
                
                
if __name__ == "__main__":
    st.markdown("<h1 style='text-align: center; color: Blue;'>Capgemini</h1>", unsafe_allow_html=True)
    LaunchUI()
            
            
            
        
            
    
        
        


