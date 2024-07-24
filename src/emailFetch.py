# import os 
# from langchain.agents import AgentType, initialize_agent, create_react_agent
# # from database import db, gmail_toolkit, llm
# from model.model import llm, gmail_toolkit

# # 1. To check if the mail has received any new mails or not

# def check_for_mail():
#     prompt_1 ="""You have access to an external system that can check email. Please use it to see if 
#     I have received a any new email in the last one hour. If there are any, filter out non-essential 
#     ones such as newsletters, Blogs, promotional content and notifications. If i have not received any
#     new mail then STOP the SEARCH. Use your expertise in email content analysis to distinguish emails 
#     from the rest, pay attention to the sender and avoid invalid emails. ALWAYS REMEMBER,
#     THE OUTPUT SHOULD BE RETURNED as a DICT not as a string  without double inverted commas in the 
#     output in the form given inside three backticks containing the sender's email address,the subject 
#     line of each email and the contents in the email,  separated by commas.
    
#     Output: ```{"emails":{
#                   "sender": "john.doe@example.com",
#                   "subject": "delivery charge?",
#                   "content": "What is the delivery charge?",
#                   "username":"john doe"
#                 }
#               }   ```
#     """
#     # prompt =""" You are provided with a input json having the following keys:
#     # 1. Subject key:  which is the subject of an email,
#     # 2. Plain_Text key: which containg email body,
#     # 3. email key: which contains sender email. 
#     # 4. username: The username of sender.
    
#     # Use your expertise in email content analysis to  distinguish spam emails from the rest
#     # Your task is explained below:
#     # 1. If the mail is non-essential ones such as newsletters, Blogs, promotional content and notifications, provide json with only one key dict("response": "NoResponse").
#     # 2. If the mail is not non-essential ones such as newsletters, Blogs, promotional content and notifications, provide response by drafting mail by  writing sweet replies to the user and  response should ALWAYS BE IN JSON THAT contains the following keys:
#     # dict("Subject"Sender emailthis is the reply subject", 
#     # "username":"username",
#     #     "Body:"the email response you drafted"
#     #     "sender_email:"Sender email")
  
#     # do not return any json tags and put no backticks in your output.  
#     # Please do not response as if you are a bot. Always respond as if you are ajeet.

#     # ### The input json is: {input_json}
#     # """
    
    
    
    
#     # If i have not received any new mail then STOP the SEARCH Use your expertise in email content analysis to distinguish emails from the rest, pay attention to the sender and avoid invalid emails. ALWAYS REMEMBER,
#     # THE OUTPUT SHOULD BE RETURNED as a DICT not as a string  without double inverted commas in the output in the form given inside three backticks containing the sender's email address,the subject line of each email and the contents in the email,  separated by commas.
    
#     # Output: ```{"emails":{
#     #               "sender": "john.doe@example.com",
#     #               "subject": "delivery charge?",
#     #               "content": "What is the delivery charge?",
#     #               "username":"john doe"
#     #             }
#     #           }   ```

#     agent = initialize_agent(agent= AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
#                             tools= gmail_toolkit.get_tools(), 
#                             llm= llm, 
#                             verbose = True, 
#                             max_execution_time = 1600,
#                             max_iterations = 1000)
#     # prompt = PromptTemplate(template=template)
#     response = agent.run(prompt_1)
#     return response




# # check_for_mail()
# # for email in email_data:
#     # result = chain.invoke({"question":email['content']})
#     # print(result)







