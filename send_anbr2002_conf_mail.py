import requests
import json
import csv
import boto3


def get_last_id():
    try:
        f = open("no.json")
        data = json.load(f)
        return data["last_count"]
    except:
        return 0


def set_last_id(id):
    dict = {"last_count": id}
    json_object = json.dumps(dict, indent=4)
    with open("no.json", "w") as outfile:
        outfile.write(json_object)


def send_mail(mail, name, id):
    smtp_host = "email-smtp.us-east-1.amazonaws.com"
    port = "587"
    ses_client = boto3.client(
        "ses",
        region_name="us-east-1",
        aws_access_key_id="AKIA6L6ZKPZWTBEWNGLA",
        aws_secret_access_key="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",
    )

    CHARSET = "UTF-8"
    HTML_EMAIL_CONTENT = """
        <html>
            <head>Greetings</head>
            <h1 style='text-align:center'></h1>
            <p>Hello {}, 
            
            <br/> Thanks for registering for Annual National Believers Retreat (ANBR)2022, 
            <br/> your registration has been received and your registration number is <strong>ANBRREG{}</strong> 
            We look to forward receiving you at this year's edition.

            <p>Please do check your email for regular updates and also get your friends and family members to register as well.</p>

            <p>To prepare your spirit for the meeting, please listen to messages from past editions, click on this link below to start
            https://t.me/threshinghousemedia/238 </p>

           <p> We invite you to join the general ANBR group on Telegram to stay informed for updates before, during, and after ANBR, Click here to join https://t.me/+wWOsn1OLqTA0YzU8</p>

           <p> Even though this is a free event, please be part of it by giving as led or decided, use the account details below:

            <strong>0449875693, GTB Threshing House Ecclesia Outreach</strong> </p>

           <p> PLEASE NOTE THAT CAMP OPENS BY 12NOON ON THURSDAY, ON ARRIVAL, APPROACH THE REGISTRATION TEAM WITH YOUR REGISTRATION DETAILS

            For further enquires, send an email to threshinghouseteam@gmail.com

            God bless you.
            </p>
            <p>
        Mayowa and Esther Omoniyi
        National Coordinators
        Threshing House
            </p>
            </body>
        </html>
    """.format(
        name, id
    )

    response = ses_client.send_email(
        Destination={
            "ToAddresses": [
                mail,
            ],
        },
        Message={
            "Body": {
                "Html": {
                    "Charset": CHARSET,
                    "Data": HTML_EMAIL_CONTENT,
                }
            },
            "Subject": {
                "Charset": CHARSET,
                "Data": "Your Invitation Card to ANBR 2022",
            },
        },
        Source="Threshing House Team <threshinghouseteam@gmail.com >",
    )



url = "https://docs.google.com/spreadsheets/d/1cojypKQ-IOfHiFdclKpLrRNh9-GJKbI7KZLX29rmzMw/export?format=csv&gid=0"

local_file = "anbr.csv"
count = int(get_last_id())
row_count = 0
data = requests.get(url)
# Save file data to local copy
with open(local_file, "wb") as file:
    file.write(data.content)


with open(local_file) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=",")
    line_count = 0
    for row in csv_reader:
        print(row_count,count)
        if row_count < count:
            row_count+=1
            continue
        
        if line_count == 0:
            # print(f'Column names are {", ".join(row)}')
            line_count += 1
        else:
            # print(f'\t{row[0]} works in the {row[1]} department, and was born in {row[2]}.')
            send_mail('kaysolaniyi@gmail.com', row[1], count+1)
            line_count += 1
            print(f"Processed {row[1]} lines.",row_count,count)
        count += 1
        row_count+=1
        if count > 2:
            break
        
    print(f"Processed {line_count} lines.")



set_last_id(count)