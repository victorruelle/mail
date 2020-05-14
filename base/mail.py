import email
import imaplib
from os import path, listdir
import smtplib, ssl
import mimetypes
from email.headerregistry import Address
from email.message import EmailMessage
from email.utils import make_msgid
from pathlib import Path
from jinja2 import Template
from random import randint

from utils import get_clean_stack, print_clean_stack, extract_text_from_html, decode, decode_header, process_sender

CURDIR = path.dirname(path.abspath(__file__))


EMAIL = None
DISPLAY_NAME = None
USERNAME = EMAIL.split("@")[0]
DOMAIN = EMAIL.split("@")[1]
PASSWORD = None
SERVER = 'imap.gmail.com'

if EMAIL is None:
    raise Exception("You need to setup personal email variables.")

def send_html_mail(template,to_email,data=None,subject=None):
    ''' Send an email with HTML content

    # Input
    - template : (str) name of the template to look for in templates/ directory
    - to_email : (str) receiver's email
    - (optional) data : (dict str:str )  dictionnary with the string values to insert into the template variables.
    - (optional) subject : (str) the subject for the email. Can contain variable to be filled with the data dict. If None, will look for subject.txt in templates/TEMPLATE
    '''

    # LOADING DATA
    if subject is None:
        assert path.isfile(path.join(CURDIR,"templates",template,"subject.txt")), "Please provide a subject file or specifiy the subject in the arguments."
        with open(path.join(CURDIR,"templates",template,"subject.txt"),'r') as f:
            subject = f.readline()
    
    data = data or {}

    # SETTING MAIL DETAILS
    me = Address(EMAIL)
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = [Address(display_name=DISPLAY_NAME,username=USERNAME,domain=DOMAIN)]
    msg['To'] = [Address(to_email)]
    msg["X-Entity-Ref-ID"] = "".join([str(randint(0,10)) for i in range(20)])


    # SETTING THE PLAIN TEXT CONTENT
    if path.isfile(path.join(CURDIR,"templates",template,"plain_message.txt")):
        with open(path.join(CURDIR,"templates",template,"plain_message.txt"),'r') as f:
            plain_text = "\n".join(f.readlines())
        msg.set_content(plain_text)


    # SETTING THE HTML RESPONSE
    assert path.isfile(path.join(CURDIR,"templates",template,"body.html")), "Could not find body.html in {}".format(path.join(CURDIR,"templates",template))
    
    with open(path.join(CURDIR,"templates",template,"body.html"),'r') as f:
        html_content = " ".join(f.readlines())
        html_template = Template(html_content)

    ## Replacing variables inside the html
    

    ## Configuring images
    cids = {}
    if path.isdir(path.join(CURDIR,"templates",template,"images")):
        for image in listdir(path.join(CURDIR,"templates",template,"images")):
            cids[image] = make_msgid()[1:-1]
    
    print("Rendering with",cids,data)
    html_rendered = html_template.render(**{image.split(".")[0]:cid for image,cid in cids.items()},**data)
    msg.add_alternative(html_rendered,subtype='html')

    ### attaching images
    for image,cid in cids.items():
        image_path = path.join(CURDIR,"templates",template,"images",image)
        maintype, subtype = mimetypes.guess_type(image_path)[0].split('/', 1)
        msg.get_payload()[1].add_related(  # image/png
            Path(image_path).read_bytes(), maintype, subtype, cid="<{}>".format(cid))


    ## Sending mail
    context = ssl.create_default_context()
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(EMAIL, PASSWORD)
            server.sendmail(
                EMAIL, to_email, msg.as_string()
            )
    
    except Exception as err:
        print_clean_stack(err)
        exit(1)


def get_new_mail():
    results = []

    mail = imaplib.IMAP4_SSL(SERVER)
    mail.login(EMAIL, PASSWORD)
    mail.select('inbox')

    status, data = mail.search(None, 'UNSEEN')
    # status, data = mail.search(None, 'UID 10:10000') # GMAIL OFFSETS UIDS WHEN QUERYING, ID 1 = SEARCH FOR 7, IF LOOKING LIKE N:*, search will always return the latest even if it's under N. Fix by putting really high value N:1000

    mail_ids = []
    for block in data:
        mail_ids += block.split()


    mail_ids.sort(key=lambda bite : bite.decode())
    for i in mail_ids:

        status, data = mail.fetch(i, '(RFC822)')

        for response_part in data:
            if isinstance(response_part, tuple):
                message = email.message_from_bytes(response_part[1])

                mail_author, mail_from = process_sender(message["from"])
                mail_subject = message['subject']
                mail_date = message['Date']

                if message.is_multipart():
                    mail_content = ''
                    for part in message.get_payload():
                        if part.get_content_type() == 'text/plain':
                            continue

                        if part.get_content_type() == 'text/html':
                            content = part.get_payload()
                            content = extract_text_from_html(content)
                            mail_content += decode(content)
                else:
                    part = message.get_payload()
                    if part.get_content_type() == 'text/html':
                        print("!!!simple mail")
                        content = part.get_payload()
                        content = extract_text_from_html(content)
                        # content = decodestring(content)
                        # content = content.decode("utf-8")
                        # content = str(content)
                        mail_content += decode(content)

                
                results.append({
                    "date":mail_date,
                    "mail":mail_from,
                    "author":mail_author,
                    "subject":mail_subject,
                    "body":mail_content,
                    "id":i.decode("utf-8")
                })

    mail.logout()
    return results


def send_plaintext_mail(message,to_email):

    # SETTING MAIL DETAILS
    me = Address(EMAIL)
    msg = EmailMessage()
    msg['Subject'] = "Error report"
    msg['From'] = [Address(display_name=DISPLAY_NAME,username=USERNAME,domain=DOMAIN)]
    msg['To'] = [Address(to_email)]
    msg["X-Entity-Ref-ID"] = "".join([str(randint(0,10)) for i in range(20)])

    # SETTING THE PLAIN TEXT CONTENT
    msg.set_content(message)  # text/plain

    ## Sending mail
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(EMAIL, PASSWORD)
        server.sendmail(
            EMAIL, to_email, msg.as_string()
        )