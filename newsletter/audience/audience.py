import csv
import os

from newsletter.audience.contact import Contact
from utils import contains,has

CURDIR = os.path.dirname(os.path.abspath(__file__))

class Audience():

    def __init__(self):
        path = os.path.join(CURDIR,"data","contacts.csv")
        contacts = csv.reader(open(path, 'r', encoding='utf-8-sig'),delimiter=";")
        next(contacts) # skipping the header
        self.contacts = [Contact.from_row(row) for row in contacts]

    def restrict_language(self,lan):
        self.contacts = [contact for contact in self.contacts if contact.language == lan]
        # print("Audience has now {} contacts".format(len(self.contacts)))

    def restrict_formality(self,formality):
        self.contacts = [contact for contact in self.contacts if contact.formality == formality]
        # print("Audience has now {} contacts".format(len(self.contacts)))

    def restrict_tag_and(self,tags):
        self.contacts = [contact for contact in self.contacts if contains(contact.tags,tags)]
        # print("Audience has now {} contacts".format(len(self.contacts)))

    def restrict_tag_or(self,tags):
        self.contacts = [contact for contact in self.contacts if has(contact.tags,tags)]
        # print("Audience has now {} contacts".format(len(self.contacts)))

    def restrict_lastname(self,lastname):
        self.contacts = [contact for contact in self.contacts if contact.lastname == lastname]

    def iterator(self):
        return (self.contacts)

    def repr(self):
        return "\n".join([contact.repr() for contact in self.contacts])


