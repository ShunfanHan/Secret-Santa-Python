import pandas as pd
import random
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def read_csv(file_path):
    try:
        data = pd.read_csv(file_path)
        return data
    except Exception as e:
        return str(e)

def assign_secret_santa(participants):
    people = participants['name'].tolist()
    santa_pairs = {}
    receivers = people.copy()

    for person in people:
        available_receivers = [r for r in receivers if r != person]
        if not available_receivers:
            return assign_secret_santa(participants)
        receiver = random.choice(available_receivers)
        santa_pairs[person] = receiver
        receivers.remove(receiver)

    return santa_pairs

def send_emails(santa_pairs, participants):
    smtp_user = 'youneedtoputyouremailhere@qq.com'
    smtp_password = 'you need to put your smtp password here(not your email password)'

    try:
        server = smtplib.SMTP_SSL('smtp.qq.com', 465)
        server.login(smtp_user, smtp_password)

        for santa, receiver in santa_pairs.items():
            email = participants[participants['name'] == santa]['email'].iloc[0]
            msg = MIMEMultipart()
            msg['From'] = smtp_user
            msg['To'] = email
            msg['Subject'] = "Your Secret Santa Assignment"
           
            body = f"Hello {santa},\n\nYou are the Secret Santa for {receiver}!"
            msg.attach(MIMEText(body, 'plain'))

            server.send_message(msg)

        server.quit()
        return "Emails sent successfully"
    except Exception as e:
        return str(e)

csv_file_path = 'player.csv'
participants_data = read_csv(csv_file_path)

if isinstance(participants_data, pd.DataFrame):
    santa_pairs = assign_secret_santa(participants_data)
    send_emails(santa_pairs,participants_data)
else:
    print(participants_data)
