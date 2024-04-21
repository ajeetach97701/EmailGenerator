import os 
from langchain.agents import AgentType, initialize_agent, create_react_agent
from database import db, gmail_toolkit, llm

# 1. To check if the mail has received any new mails or not
def check_for_mail():
    prompt ="""You have access to an external system that can check email. Please use it to see if I have received a new email. If there are any, filter out non-essential ones such as newsletters, Blogs, promotional content and notifications.Use your expertise in email content analysis to distinguish emails from the rest, pay attention to the sender and avoid invalid emails. Return the response as a DICT containing the sender's email address,the subject line of each email and the contents in the email,  separated by commas without double inverted commas in the output."""

    agent = initialize_agent(agent= AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
                            tools= gmail_toolkit.get_tools(), 
                            llm= llm, 
                            verbose = True, 
                            max_execution_time = 1600,
                            max_iterations = 1000)
    gmail_toolkit.mark_as_read(os.getenv('MY_EMAIL'))
    
    # prompt = PromptTemplate(template=template)
    response = agent.run(prompt)
    return response




# for email in email_data:
#     result = chain.invoke({"question":email['content']})
#     print(result)