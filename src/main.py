import time
from emailSend import send_email
from emailFetch import check_for_mail
from queryResponse import chain

import time

def main():
    i = 0
    while i<= 2:
        time.sleep(30)
        print(f"-------------------------------Iteration number:{i}----------------------------")
        i += 1
        response = check_for_mail()  
        # print(response)
        # print(type(response))
        if response:
            email_data = response['emails']
            for email in email_data:
                # print("--------")
                # print("Email Content is ")
                # print("--------")
                # print(email['content'])
                # print("--------")
                result = chain.invoke({"question": email['content']})  
                print(email['sender'])
                send_email(to_email=email['sender'], subject=email['subject'], message=result) 
                print(result)
        else:
            print("No new email received")
            
            
            
if __name__ == "__main__":
    main()