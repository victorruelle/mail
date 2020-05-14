from chromedriver import get_driver
from newsletter.commands import select_all,copy,paste, new_tab, go_to_tab
import os
import re
from time import sleep

CURDIR = os.path.dirname(os.path.abspath(__file__))
PARDIR = os.path.dirname(CURDIR)

def insert_campaign(campaign_name,contact):
    personalized_campaign_url = create_personalized_campaign(campaign_name,contact)
    driver = get_driver()
    current_page = driver.current_window_handle
    new_page = new_tab("")
    driver.switch_to.window(new_page)
    driver.get(personalized_campaign_url)
    select_all()
    copy()
    driver.close()
    driver.switch_to.window(current_page)
    paste()
    sleep(0.5)

def get_campaign_url(campaign_name,contact):
    campaign_dir = os.path.join(CURDIR,"data",campaign_name)
    url = os.path.join(campaign_dir,contact.language,"body.html")
    return url

def get_subject_url(campaign_name,contact):
    campaign_dir = os.path.join(CURDIR,"data",campaign_name)
    url = os.path.join(campaign_dir,contact.language,"subject.txt")
    return url

def create_personalized_campaign(campaign_name,contact):
    url = get_campaign_url(campaign_name,contact)
    with open(url,'r') as html:
        html = "\n".join(html.readlines())
        html_perso = personalize(html,contact)
    output_url = os.path.join(CURDIR,"data","tmp.html")
    with open(output_url,'w') as output:
        output.write(html_perso)
    return output_url

def personalize(content,contact):
    content = re.sub("{"+"firstname}",contact.firstname,content)
    content = re.sub("{"+"lastname}",contact.lastname,content)
    
    # catch gender formating
    for match in reversed(list(re.finditer(r"\{gender\}", content))):
        start,end = match.start(),match.end()
        assert content[end:end+2] == "(("
        end_2 = content.index("))",end)
        options = content[end+2:end_2].split("|")
        right_option = options[0] if contact.gender == "m" else options[1]
        content = content[:start]+right_option+content[end_2+2:]
    
    # catch formality formating
    for match in reversed(list(re.finditer(r"\{formal\}", content))):
        start,end = match.start(),match.end()
        assert content[end:end+2] == "((", content[start-10:end+10]
        end_2 = content.index("))",end)
        options = content[end+2:end_2].split("|")
        assert len(options)==2, content[start-20:end+30]
        right_option = options[0] if contact.formality == "yes" else options[1]
        content = content[:start]+right_option+content[end_2+2:]
    
    return content


def preview_campaign(campaign_name,audience):
    
    us_contact, fr_m_contact, fr_f_contact, fr_m_formal_contact, fr_f_formal_contact = None,None,None,None,None
    for contact in audience.iterator():
        if us_contact is None and contact.language=="en":
            us_contact = contact
        if fr_m_contact is None and contact.language=="fr" and contact.formality=="no" and contact.gender=="m":
            fr_m_contact = contact
        if fr_f_contact is None and contact.language=="fr" and contact.formality=="no" and contact.gender=="f":
            fr_f_contact = contact
        if fr_m_formal_contact is None and contact.language=="fr" and contact.formality=="yes" and contact.gender=="m":
            fr_m_formal_contact = contact
        if fr_f_formal_contact is None and contact.language=="fr" and contact.formality=="yes" and contact.gender=="f":
            fr_f_formal_contact = contact
        if fr_m_contact is not None and fr_f_contact is not None and fr_m_formal_contact is not None and fr_f_formal_contact is not None and us_contact is not None:
            break

    contacts = [contact for contact in [us_contact,fr_m_formal_contact,fr_f_formal_contact,fr_m_contact,fr_f_contact] if contact is not None]

    driver = get_driver()
    print("Starting preview for the campaign")

    for i,contact in enumerate(contacts):
        print("Example contact : {}".format(contact.repr()))
        print("Mail subject is : {}".format(get_subject(campaign_name,contact)))
        personalized_campaign_url = create_personalized_campaign(campaign_name,contact)
        driver.get(personalized_campaign_url)
        if i<len(contacts)-1:
            new_page = new_tab("")
            driver.switch_to.window(new_page)


def get_subject(campaign_name,contact):
    subject_path = get_subject_url(campaign_name,contact)
    with open(subject_path,'r',encoding='utf8') as subject:
        subject = "\n".join(subject.readlines())
        return subject if contact is None else personalize(subject,contact)

    