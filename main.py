from emailSRC.emailFilter import check_for_new_emails
import time
import time


def main():
    while True:
        # check_for_mail()
        check_for_new_emails()
        time.sleep(5)

if __name__ == "__main__":
    main()
