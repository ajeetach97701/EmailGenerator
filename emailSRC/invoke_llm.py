from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain.schema.runnable import RunnableMap
from langchain.agents import AgentType, initialize_agent
from model.model import llm
from src.emailSend import send_email
def invoke_llm(input_json):
    prompt = """
    You are  virtual assistant whose name is Ajeet Acharya. You are expert at drafting emails and writing the response in json format and giving sweet replies to the user.  Based on the input provided to you in double backticks which is a input json having the following keys:
    1. Subject key:  which is the subject of an email,
    2. Message_Body key: which containg email body in html format,
    3. email key: which contains sender email. 
    4. username: The username of sender
    Ignore other keys. 
    
    
    Use your expertise in email content analysis to  distinguish spam emails from the rest
    Your task is explained below:
    1. If the mail is non-essential ones such as newsletters, Blogs, promotional content and notifications, provide json with only one key dict("response": "NoResponse").
    2. If the mail is not non-essential ones such as newsletters, Blogs, promotional content and notifications, provide response by drafting an email response based on the subject and Plain_Text given to you with a reply subject and message body. Greet the user with the username. Your response should ALWAYS BE IN JSON THAT contains proper HTML format which should be beautiful. the following are the keys:
    dict(
        "Subject":"this is the reply subject", 
        "username":"username",
        "Body:"the email response you drafted which should be in html form not plain text"
        "sender_email:"Sender email"
        )
        
    
    
    
    
  
    do not return any json tags and put no backticks in your output.  
    Please do not response as if you are a bot. Always respond as if you are ajeet and write Best Regards, Ajeet Acharya at last.

    ### The input json is: {input_json}
    

    """

    output_parser = JsonOutputParser()

    template = ChatPromptTemplate.from_template(prompt)



    chain = RunnableMap(
        {
            "input_json": lambda x:x['input_json']
        }
    )|template|llm|output_parser



    response = chain.invoke({"input_json":input_json})
    print("Response is:")
    print(response)
    if "response" in response:
        print("NO mails")
    else:
        sender = response.get("sender_email")
        subject = response.get("Subject")
        Body = response.get("Body")
        username = response.get("username")
        reply = ["notifications-noreply", "no-reply", "notification","messages-noreply"]
        if username != "no-reply":
            send_email(to_email=sender, subject= subject, message=Body)
        else:
            print("Reply cannot be sent")
        return f"Reply sent to {sender}"