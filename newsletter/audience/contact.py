from utils import clean_spaces

languages = {
    "fr":"french",
    "en":"english"
}

genders = {
    "m":"male",
    "f":"female"
}

class Contact():

    def __init__(self,firstname,lastname,email,tags,language,formality,gender):
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.tags = tags
        self.language = language
        self.formality = formality
        self.gender = gender

    @staticmethod
    def from_row(row):
        firstname,lastname,email,tags,language,formality,gender = row
        tags = tags.split(",")
        for i in range(len(tags)):
            tags[i] = clean_spaces(tags[i])
        return Contact(clean_spaces(firstname),clean_spaces(lastname),clean_spaces(email),tags,clean_spaces(language),clean_spaces(formality),clean_spaces(gender))

    def __repr__(self):
        return "{} {}".format(self.firstname,self.lastname)

    def repr(self):
        return "{} {}, {}, {}, {}, {}, {}".format(self.firstname,self.lastname,self.email,self.tags,languages[self.language],"formal" if self.formality=="yes" else "informal",genders[self.gender])
