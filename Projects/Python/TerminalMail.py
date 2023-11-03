import smtplib
import imaplib
import getpass
import re
from email.header import decode_header
import email
from email import message_from_bytes

def send_mail_protocol():
    global send_mail
    send_mail = smtplib.SMTP('smtp.gmail.com', 587)
    send_mail.ehlo()
    send_mail.starttls()


def get_mail_protocol():
    global get_mail
    get_mail = imaplib.IMAP4_SSL('imap.gmail.com')


def check_mail(email):
    regmail = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+.[A-Z|a-z]{2,7}\b'
    if re.match(regmail,email):
        return True
    else:
        return False
        

def obtain_header(msg):
    # decodew the email subject
    subject, encoding = decode_header(msg["Subject"])[0]
    if isinstance(subject,bytes):
        try:    #Reason for Try/Except: Python Returning Error[Decode needs to be 'str' not 'None', despite program working. Breaks while loop]
            subject = subject.decode(encoding)
        except:
            i=0
        # if len(subject) == 0:            NOT WORKING
        #     subject = '<No Subject>'     NOT WORKING

    # decode email sender
    From, encoding = decode_header(msg.get("From"))[0]
    if isinstance(From, bytes):
        try:
            From = From.decode(encoding)
        except:
            i=0

    print("Subject:", subject)
    print("From:", From,'\n')
    return subject, From


def check_mail_category():
    # global num_of_messages
    category_list = ['RECENT','BEFORE','AFTER','SINCE','FROM','TO','SUBJECT','SEEN','UNSEEN']
    print('Which Messages would you like to see?(Just type in capitalized options)(Press "exit to leave")\n')
    global mail_category_input
    mail_category_input = input('RECENT \nBEFORE [date] \nAFTER [date] \nSINCE [date] \nFROM [address] \nTO [address] \nSUBJECT(type subject) \nSEEN Messages \nUNSEEN Messages \n').upper()

    while True:
        if mail_category_input =='EXIT':
            break
        elif mail_category_input in category_list:
            if mail_category_input == 'RECENT':
                return 'ALL'

            elif mail_category_input in ['BEFORE','AFTER','SINCE']:
                try:
                    check_date = input('\nEnter Date(in DD-MMM-YYYY format(type first three letter of month):\n')
                    get_mail.search(None,f'{mail_category_input} {check_date}')
                except:
                    print("Please Try Again")
                    continue

                return f'{mail_category_input} {check_date}'

            elif mail_category_input in['FROM','TO']:
                while True:
                    check_address = input(f'{mail_category_input.lower().capitalize()}:')
                    if check_mail(check_address):
                        if len(get_mail.search(None,f'{mail_category_input} {check_address}')[1][0]) !=0:
                            break
                        else:
                            print("No emails on this address")
                    else:
                        print('Please enter email again:\n')
                return f'{mail_category_input} {check_address}'
            
            elif mail_category_input =='SUBJECT':
                while True:
                    check_subject = input('Type Subject\n')
                    if len(get_mail.search(None,f'{mail_category_input} {check_subject}')[1][0]) !=0:
                            break
                    else:
                        print("No emails on this address")
                return f'{mail_category_input} {check_subject}'

            elif mail_category_input in ['SEEN','UNSEEN']:
                return f'{mail_category_input} {mail_category_input}'
        else:
            while mail_category_input not in category_list and mail_category_input != 'EXIT':
                mail_category_input = input("Please Try Again: \n").upper()

            
    




#App Password: 

# Connects to Mail server using SMTP
send_mail_protocol()
get_mail_protocol()
print('Note: Currently only works with gmail accounts. If done with gmail account, app password must be made to use this application')

# Here you login to your mail account(Gmail)
while True:
    try:
        
        # email,password = 'muhd.ayman.haque@gmail.com','sjvoisflccfgvimz'
        input('Enter Email:\n'),input('Enter Password:\n')
        send_mail.login(email,password)
        get_mail.login(email,password)
        break
    except:
        print('Please Try again')
        continue

print("Welcome To Terminal Mail!")
mail_runner = True


# Endless Loop where you can send mail, check mail, or quit the loop
while mail_runner:
    choice_input = input("\nWhat would you like to do?\n(Send Mail, Check Mail, Quit):\n")

    # Quit
    if ('QUIT' in choice_input.upper()):
        print("Thank you for using Terminal Mail. Goodbye")
        mail_runner = False
        send_mail.quit()
        continue



    # Check Mail
    elif('CHECK' in choice_input.upper()):
        while True:
            status,messages = get_mail.select('inbox')
            try:
                typ,data = get_mail.search(None,check_mail_category())
            except:
                break
            num_of_messages = int(data[0].split()[0])
            if mail_category_input in ['BEFORE','SEEN','UNSEEN','FROM','TO','SUBJECT','RECENT']:
                data[0] = data[0].split()
                data[0].reverse()
            else:
                data[0] = data[0].split()
            # for i in range(num_of_messages, num_of_messages - 3, -1):
            while True:
                try:
                    num_of_shown_messages = int(input("How many messages do you want to see?"))
                    break
                except:
                    print("Please Type a number")
            for i in data[0][0:num_of_shown_messages]:
                res, msg = get_mail.fetch(str(int(i)),"(RFC822)")

                for response in msg:
                    if isinstance(response,tuple):
                        msg = message_from_bytes(response[1])
                        obtain_header(msg)
            break

        
    # Send Mail
    elif('SEND' in choice_input.upper()):
        print('\n\nSending Mail(Type exit if you would like to exit mail sender)')
        from_address = email
        while True:
            to_address = input("To:")
            if to_address.lower() == 'exit':
                break
            if check_mail(to_address):
                send_subject = input("Enter Subject Line: ")
                send_body = input("Enter Body Message: ")
                msg = "Subject: "+send_subject+'\n'+send_body
                send_mail.sendmail(from_address,to_address,msg)
                break
            else:
                print("Invalid Email. Try Again\n")
                continue
            

    else:
        print('Sorry Please Try Again')
