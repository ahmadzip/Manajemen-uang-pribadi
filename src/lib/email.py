from flask_mail import Message
import requests
from src import app, mail


def send_email(to, subject, template):
    return requests.post(
        "https://api.mailgun.net/v3/sandbox311bb16fa39d43e48bc850b9e918c351.mailgun.org/messages",
        auth=("api", "8aa6df250c801600eadefd87ac6a285e-7ecaf6b5-27dbd202"),
        data={"from": "SAVE.MO <mailgun@sandbox311bb16fa39d43e48bc850b9e918c351.mailgun.org>",
              "to": [to],
              "subject": subject,
              "html": template})
