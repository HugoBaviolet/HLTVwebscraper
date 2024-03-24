import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent


# Function to send email
def send_email(subject, message):
    sender_email = ""  # Replace with your email
    receiver_email = ""  # Replace with recipient's email
    password = ""  # Replace with your email password

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject

    body = message
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
        print("Email sent successfully")
    except Exception as e:
        print("Error:", e)
    finally:
        server.quit()


user_agent = UserAgent()
headers = {'User-Agent': user_agent.random}
url = 'https://www.hltv.org/matches'
response = requests.get(url, headers=headers)

if response.status_code == 200:
    soup = BeautifulSoup(response.content, 'html.parser')
    upcoming_matches = soup.find('div', class_='upcomingMatchesAll')

    if upcoming_matches:
        matches_text = upcoming_matches.get_text().strip()
        matches_list = [match.strip() for match in matches_text.split('\n\n') if
                        match.strip()]  # Split matches and remove extra spaces

        output = ""
        for match in matches_list:
            match_lines = match.split('\n')
            for i, line in enumerate(match_lines):
                if ':' in line:  # Check if the line contains a colon
                    if i == 0:  # Add a space above the time if it's not the first line
                        output += "\n"
                if "Odds" not in line:  # Check if the line does not contain "Odds"
                    output += line.strip().center(80) + "\n"

        # Send the output via email
        subject = "Upcoming CS2 Matches"
        send_email(subject, output)
    else:
        # Element not found
        print("Div not found")
else:
    # Webpage not found
    print("Failed to retrieve webpage:", response.status_code)
