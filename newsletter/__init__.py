from newsletter.test import test_audience,test_html,test_send_mail
from newsletter.audience import Audience
from newsletter.campaigns import insert_campaign, preview_campaign, get_subject
from newsletter.gmail import to_gmail,new_mail, set_to_mail, set_subject, select_body, send_mail_action
from chromedriver import get_driver,close_driver
from time import sleep

def launch_campaign(campaign_name,tag_and=None,tag_or=None,formality=None,language=None,lastname = None,skip_verification=False):
    audience = select_audience(tag_and,tag_or,formality,language,lastname)
    send_newsletter(campaign_name,audience,skip_verification)

def select_audience(tag_and=None,tag_or=None,formality=None,language=None,lastname = None):
    audience = Audience()
    if tag_and is not None:
        audience.restrict_tag_and(tag_and)
    if tag_or is not None:
        audience.restrict_tag_or(tag_or)
    if formality is not None:
        audience.restrict_formality(formality)
    if language is not None:
        audience.restrict_language(language)
    if lastname is not None:
        audience.restrict_lastname(lastname)
    return audience

def send_newsletter(campaign_name,audience,skip_verification=False):

    assert len(audience.contacts)>0

    # Print audience
    print("The target audience is:\n"+audience.repr())

    cont = None
    while cont not in ["y","n"]:
        cont = input("\nContinue with target audience? (y/n): ")

    if cont == "n":
        exit(0)

    if not skip_verification:
        preview_campaign(campaign_name,audience)

        cont = None
        while cont not in ["y","n"]:
            cont = input("Look at the sample email, is everything good? (y/n): ")
        close_driver()

        if cont == "n":
            exit(0)

    to_gmail()

    for contact in audience.iterator():
        new_mail()
        set_to_mail(contact.email)
        set_subject(get_subject(campaign_name,contact))
        select_body()
        insert_campaign(campaign_name,contact)
        send_mail_action()
        sleep(2)
    
    close_driver()
    