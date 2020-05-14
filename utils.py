import re
from html import unescape
from quopri import decodestring
from email.header import decode_header as _decode_header
import traceback


def clean_spaces(text):
    text = re.sub(' +', ' ', text)
    text = re.sub('(^ )|( $)','',text)
    return text


def print_clean_stack(err):
    print("Error stack:\n"+"\n".join(["{}\{}".format(s.filename,s.name) for s in traceback.extract_tb(err.__traceback__)])+"\nException caught : {}".format(err))

def get_clean_stack(err):
    return "Error stack:\n"+"\n".join(["{}\{}".format(s.filename,s.name) for s in traceback.extract_tb(err.__traceback__)])+"\nException caught : {}".format(err)

def extract_text_from_html(html):
    html = re.sub("=\r\n","",html)
    html = re.sub("\r\n","\n",html)
    html = re.sub("</span>","\n",html)
    while "<" in html:
        start = html.index("<")
        end = html.index(">")
        html = html[:start]+html[end+1:]
    return unescape(html)

def decode(text):
    text = decodestring(text)
    text = text.decode("utf-8")
    text = str(text)
    return text

def process_sender(sender):
    ''' Process sender to extract an author and an email
    '''
    if " <" in sender:
        # we have a specific name
        author = clean_spaces(sender[:sender.index(" <")])
        mail = clean_spaces(sender[sender.index(" <")+2:sender.index(">")])
    else:
        author = clean_spaces(sender.split("@")[0])
        mail = clean_spaces(sender)
    author,mail = decode_header(author),decode_header(mail)
    author = re.sub("\"","",author)
    return author,mail

def decode_header(text):
    parts = _decode_header(text)
    decoded_parts = []
    for part in parts:
        content,encoding = part
        if encoding is not None:
            content = content.decode(encoding)
        decoded_parts.append(content)
    return " ".join(decoded_parts)

def contains(big,small):
    ''' Big contains small
    '''
    for el in small:
        if not el in big:
            return False
    return True

def has(big,small):
    ''' Small has one element in big
    '''
    for el in small:
        if el in big:
            return True
    return False