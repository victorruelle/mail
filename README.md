# Mail
Collection of two related libraries:
- base : common mailing methods to read and send plaintext and html mails using SMPTlib
- newsletter : complete mailing engine using selenium and GMail client that includes advanced templating and userbase management

## Base

Base contains three key methods : ```get_new_mail```,```send_plain_mail```,```send_html_mail```. To use these methods, you will need to replace the global mail varialbes (email, password) in the base/mail.py file. To make this safe, use os.environ and place your credentials in your environment variables. Alternatively, you can use python's input method for testing.

### HTML mail

To send html mails, you first need to define an html template to be sent. Within the ```base/templates``` directory, create a new directory named after your template and respect the following structure

```
template_name
|--- body.html : html content to be sent
|--- plain_message.txt : plain text alternative to the html content. This is required by the mail servers.
|--- subject.txt : (optional) one line text to define the mail subject
|--- images
     |--- image1.jpg
     |--- image2.jpg
```

To send the email
```python
from base import send_html_mail
send_html_mail("temaplte_name","receiver@gmail.com")
```

### Using variables
The HTML is formatted using Jinja2 and the data dictionnary given as optional parameter to the ```send_html_mail``` method. Just include ```{{key}}``` in the html and run ```send_html_mail(template_name,receiver_email,{key:"value"})```.

### Including images
Any image added in the images folder will be attached to the email. If they are used in the HTML template, they will not appear as attachments.
To include an image in your template the image tag with a cid source. You should use the name of the image (ie: filename without the extension)
```html
<img src="cid:{{image1}}>">
```


## Newsletter

Here's how to send a newsletter
1. Populate your audience dataset in ```newsletter/audience/data/contacts.csv```
2. Define your campaign by creating a new directory in ```newsletter/campaigns/data``` named after your campaign and filling it with, for each language in your target audience, a directory with as name the language code (eg : "en" for english) and within each language subdirectory two files : body.html and subject.txt. Look at the sample campaign for an example.
3. Run ```launch_campaign("campaign name")``` with optional audience filtering arguments. This will start an interactive process to select your target audience, create presonalized HTML contents and send them using Selenium and GMail.

### Mail personalisation

We use custom HTML formatting to allow for in-depth message personalisation. For each email sent, the HTML will be formatted using the data specific to the target person as defined in ```contacts.csv```. So far, we support the following variables:
- {first_name}
- {last_name}
- {gender}((content if male|content if female))
- {formal}((content if formal|content if informal))

### Defining a target audience
When launching a campaign, you can add the following filtering options: 
- tag_and : ([str]) only contacts who have all the correspondings tags will be selected
- tag_or : ([str]) contacts who have any of the correspondings tags will be selected
- formality : (str) "yes" or "no"; only contacts with corresponding formality are selected
- language : (str) language code, "en" or "fr" for English and French for instance; only contacts with corresponding language are selected
- last_name : (Str) a specific last name, for testing purposes.