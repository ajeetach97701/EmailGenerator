"""
This file contains the code that fetches unread emails and makes tham as read after fetching them.

"""


import psutil 
from email_listener import EmailListener, email_responder, helpers
from imapclient import IMAPClient, SEEN
import email
from pprint import pprint
import html2text
import os
from email_listener.helpers import calc_timeout, get_time
from email_listener.email_processing import write_txt_file

class CustomEmailListener(EmailListener):
    
    """EmailListener object for listening to an email folder and processing emails.

    Attributes:
        email (str): The email to listen to.
        app_password (str): The password for the email.
        folder (str): The email folder to listen in.
        attachment_dir (str): The file path to the folder to save scraped
            emails and attachments to.
        server (IMAPClient): The IMAP server to log into. Defaults to None.

    """
    



    def __get_from(self, email_message):
        """Helper function for getting who an email message is from.

        Args:
            email_message (email.message): The email message to get sender of.

        Returns:
            A string containing the username of the from email address.

        """

        from_raw = email_message.get_all('From', [])
        from_list = email.utils.getaddresses(from_raw)

        if len(from_list) == 0:
            from_email = "UnknownEmail"
        elif len(from_list[0]) == 1:
            from_email = from_list[0][0]
        elif len(from_list[0]) == 2:
            from_email = from_list[0][1]
        else:
            from_email = "UnknownEmail"

        # Extract the username from the email address
        username, _ = from_email.split('@', 1) if '@' in from_email else (from_email, "")

        return from_email, username


    def __get_subject(self, email_message):
        """

        """

        # Get the subject
        subject = email_message.get("Subject")
        # If there isn't a subject
        if subject is None:
            return "No Subject"
        return subject
    
    
    def __parse_multipart_message(self, email_message, val_dict):
        """Helper function for parsing multipart email messages.

        Args:
            email_message (email.message): The email message to parse.
            val_dict (dict): A dictionary containing the message data from each
                part of the message. Will be returned after it is updated.

        Returns:
            The dictionary containing the message data for each part of the
            message.

        """

        # For each part
        for part in email_message.walk():
            # If the part is an attachment
            file_name = part.get_filename()
            if bool(file_name):
                # Generate file path
                file_path = os.path.join(self.attachment_dir, file_name)
                file = open(file_path, 'wb')
                file.write(part.get_payload(decode=True))
                file.close()
                # Get the list of attachments, or initialize it if there isn't one
                attachment_list = val_dict.get("attachments") or []
                attachment_list.append("{}".format(file_path))
                val_dict["attachments"] = attachment_list

            # If the part is html text
            # elif part.get_content_type() == 'text/html':
            #     # Convert the body from html to plain text
            #     val_dict["Plain_HTML"] = html2text.html2text(
            #             part.get_payload())
            #     val_dict["HTML"] = part.get_payload()

            # If the part is plain text
            elif part.get_content_type() == 'text/plain':
                # Get the body
                val_dict["Message_Body"] = part.get_payload()

        return val_dict

    def __is_valid_email(self, email_message):
        spam_keywords = ["unsubscribe", "sale", "discount", "promotion", "newsletter"]
        notification_keywords = ["notification", "alert", "reminder"]

        subject = self.__get_subject(email_message)
        lower_subject = subject.lower()

        is_spam = any(keyword in lower_subject for keyword in spam_keywords)
        is_notification = any(keyword in lower_subject for keyword in notification_keywords)

        return not (is_spam or is_notification)

    def __parse_singlepart_message(self, email_message, val_dict):
        """Helper function for parsing singlepart email messages.

        Args:
            email_message (email.message): The email message to parse.
            val_dict (dict): A dictionary containing the message data from each
                part of the message. Will be returned after it is updated.

        Returns:
            The dictionary containing the message data for each part of the
            message.

        """

        # Get the message body, which is plain text
        val_dict["Plain_Text"] = email_message.get_payload()
        return val_dict


    def __execute_options(self, uid, move, unread, delete):
        """Loop through optional arguments and execute any required processing.

        Args:
            uid (int): The email ID to process.
            move (str): The folder to move the emails to. If None, the emails
                are not moved. Defaults to None.
            unread (bool): Whether the emails should be marked as unread.
                Defaults to False.
            delete (bool): Whether the emails should be deleted. Defaults to
                False.

        Returns:
            None

        """

        # If the message should be marked as unread
        if bool(unread):
            self.server.remove_flags(uid, [SEEN])

        # If a move folder is specified
        if move is not None:
            try:
                # Move the message to another folder
                self.server.move(uid, move)
            except:
                # Create the folder and move the message to the folder
                self.server.create_folder(move)
                self.server.move(uid, move)
        # If the message should be deleted
        elif bool(delete):
            # Move the email to the trash
            self.server.set_gmail_labels(uid, "\\Trash")
        return


    def scrape(self, move=None, unread=False, delete=False):
        if type(self.server) is not IMAPClient:
            raise ValueError("server attribute must be type IMAPClient")

        msg_dict = {}

        # Search for unseen messages
        messages = self.server.search('UNSEEN')
        # Fetch the unseen messages
        for uid, message_data in self.server.fetch(messages, 'RFC822').items():
            email_message = email.message_from_bytes(message_data[b'RFC822'])

            # Filter out spam, promotional, and notification emails
            if not self.__is_valid_email(email_message):
                continue

            from_email = self.__get_from(email_message)
            key = "{}_{}".format(uid, from_email)
            val_dict = {}

            print("PROCESSING: Email UID = {} from {}".format(uid, from_email))

            val_dict["Subject"] = self.__get_subject(email_message).strip()

            if email_message.is_multipart():
                val_dict = self.__parse_multipart_message(email_message, val_dict)
            else:
                val_dict = self.__parse_singlepart_message(email_message, val_dict)

            msg_dict[key] = val_dict

            self.__execute_options(uid, move, unread, delete)

        return msg_dict


    # def get_email(self):
    #     sender_email = None
    #     messages = self.server.search("UNSEEN")
    #     # For each unseen message
    #     for uid, message_data in self.server.fetch(messages, 'RFC822').items():
    #         # Get the message
    #         email_message = email.message_from_bytes(message_data[b'RFC822'])
    #         # Get who the message is from
    #         sender_email = self.__get_from(email_message)

        
    #     return sender_email
   

    def listen(self, timeout, process_func=write_txt_file, **kwargs):
        """Listen in an email folder for incoming emails, and process them.

        Args:
            timeout (int or list): Either an integer representing the number
                of minutes to timeout in, or a list, formatted as [hour, minute]
                of the local time to timeout at.
            process_func (function): A function called to further process the
                emails. The function must take only the list of file paths
                returned by the scrape function as an argument. Defaults to the
                example function write_txt_file in the email_processing module.
            **kwargs (dict): Additional arguments for processing the email.
                Optional arguments include:
                    move (str): The folder to move emails to. If not set, the
                        emails will not be moved.
                    unread (bool): Whether the emails should be marked as unread.
                        If not set, emails are kept as read.
                    delete (bool): Whether the emails should be deleted. If not
                        set, emails are not deleted.

        Returns:
            None

        """

        # Ensure server is connected
        if type(self.server) is not IMAPClient:
            raise ValueError("server attribute must be type IMAPClient")

        # Get the timeout value
        outer_timeout = calc_timeout(timeout)

        # Run until the timeout is reached
        while (get_time() < outer_timeout):
            self.__idle(process_func=process_func, **kwargs)
        return
    
    def __idle(self, process_func=write_txt_file, **kwargs):
        """Helper function, idles in an email folder processing incoming emails.

        Args:
            process_func (function): A function called to further process the
                emails. The function must take only the list of file paths
                returned by the scrape function as an argument. Defaults to the
                example function write_txt_file in the email_processing module.
            **kwargs (dict): Additional arguments for processing the email.
                Optional arguments include:
                    move (str): The folder to move emails to. If not set, the
                        emails will not be moved.
                    unread (bool): Whether the emails should be marked as unread.
                        If not set, emails are kept as read.
                    delete (bool): Whether the emails should be deleted. If not
                        set, emails are not deleted.

        Returns:
            None

        """

        # Set the relevant kwarg variables
        move = kwargs.get('move')
        unread = bool(kwargs.get('unread'))
        delete = bool(kwargs.get('delete'))
        # Start idling
        self.server.idle()
        print("Connection is now in IDLE mode.")
        # Set idle timeout to 5 minutes
        inner_timeout = get_time() + 60*5
        # Until idle times out
        while get_time() < inner_timeout:
            # Check for a new response every 30 seconds
            responses = self.server.idle_check(timeout=30)
            if responses:
                print("Response is received")
            else:
                print("SERVER SENT: nothing")
            
            # If there is a response
            if responses:
                # Suspend the idling
                self.server.idle_done()
                # Process the new emails
                msgs = self.scrape(move=move, unread=unread)
                # Run the process function
                process_func(self, msgs)
                # Restart idling
                self.server.idle()
        # Stop idling
        self.server.idle_done()
        return
