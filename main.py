import datetime
import logging
import os
import smtplib
import sys
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logger = logging.getLogger("hacker-news-email")


load_dotenv() 


now = datetime.datetime.now()


def extract_news(url):
    """Extract stories from Hacker News"""
    
    cnt = ""
    cnt += "<b>HN Top Stories:</b>\n" + "<br>" + "-" * 50 + "<br>"
    response = requests.get(url)
    content = response.content
    soup = BeautifulSoup(content, "html.parser")
    for i, tag in enumerate(
        soup.find_all("td", attrs={"class": "title", "valign": ""})
    ):
        cnt += (
            (str(i + 1) + " :: " + tag.text + "\n" + "<br>")
            if tag.text != "More"
            else ""
        )
    return cnt


def send_email(content):
    """Sends Email with scrapped content"""
    # update your email details
    # make sure to update the Google Low App Access settings before

    SERVER = os.getenv("EMAIL_HOST")
    PORT = 587
    FROM = os.getenv("EMAIL_HOST_USER")
    PASS = os.getenv("EMAIL_HOST_PASSWORD")
    TO = ""  # can be a list

    # Create a text/plain message
    msg = MIMEMultipart()
    msg["Subject"] = f"Top News Stories HN [Automated Email]"{str(now.day)}-{str(now.month)}-{str(now.year)}""
    msg["From"] = FROM
    msg["To"] = TO
    msg.attach(MIMEText(content, "html"))

    logger.info("Initiating Server...")

    server = smtplib.SMTP(SERVER, PORT)
    server.set_debuglevel(1)
    server.ehlo()
    server.starttls()
    server.login(FROM, PASS)
    server.sendmail(FROM, TO, msg.as_string())
    server.quit()


def main():
    """Main function"""
    logger.info("Extracting Hacker News Stories...")
    # email content placeholder
    content = ""
    cnt = extract_news("https://news.ycombinator.com/")
    content += cnt
    content += "<br>------<br>"
    content += "<br><br>End of Message"
    logger.info("Sending email...")
    send_email(content)
    logger.info("Email Sent!")


if __name__ == "__main__":
    main()
