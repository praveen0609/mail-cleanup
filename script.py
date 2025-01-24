import imaplib
import email
import datetime
import sys

read_list = [
    "transactional.vanguard.com",
    "medium.com",
    "github.com",
    "messages.xoom.com",
    "e.honeywellhome.com",
    "seekingalpha.com",
    "d1training.com",
    "linkedin.com"
]

delete_list = [
    "cpk.com",
    "overstock.com",
    "fool.com", 
    "e.dcsg.com",
    "email.marcustheaters.com",
    "emails.barclaysus.com",
    "email.marinerfinance.com",
    "signaturehvac.com",
    "e.ray-ban.com",
    "o.delta.com",
    "nimbusnordic.com",
    "fhr-solutions.com",
    "ripleys.com",
    "email.legoland.com",
    "judgemobilewash.com",
    "newsletters.yahoo.net",
    "communications.sbi.co.in",
    "email-marriott.com"
]

def connect_to_yahoo_mail(username, password):
    try:
        mail = imaplib.IMAP4_SSL('imap.mail.yahoo.com', 993)
        mail.login(username, password)
        print("Connected to Yahoo Mail")
        return mail
    except imaplib.IMAP4.error as e:
        print(f"Failed to connect: {e}")
        sys.exit(1)


def get_query_string(start_date, end_date):
    return '(SINCE {start_date} BEFORE {end_date})'.format(start_date=start_date, end_date=end_date)


def email_mark_as_read(mail, start_date, end_date):
    mail.select("inbox")
    result, data = mail.search(None, get_query_string(start_date, end_date))
    if result != 'OK':
        print("No unread messages found!")
        return

    domains = read_list

    for num in data[0].split():
        result, msg_data = mail.fetch(num, '(BODY.PEEK[])')
        if result != 'OK':
            print(f"Failed to fetch email {num}")
            continue

        msg = email.message_from_bytes(msg_data[0][1])
        from_address = email.utils.parseaddr(msg['From'])[1]
        received_date = msg['Date']
        domain = from_address.split('@')[-1]

        if domain in domains:
            mail.store(num, '+FLAGS', '\\Seen')
            print(f"Marked email from {from_address} as read")


def email_delete(mail, start_date, end_date):
    mail.select("inbox")
    result, data = mail.search(None, get_query_string(start_date, end_date))
    if result != 'OK':
        print("No messages found!")
        return

    domains = delete_list

    for num in data[0].split():
        result, msg_data = mail.fetch(num, '(BODY.PEEK[])')
        if result != 'OK':
            print(f"Failed to fetch email {num}")
            continue

        msg = email.message_from_bytes(msg_data[0][1])
        from_address = email.utils.parseaddr(msg['From'])[1]
        received_date = msg['Date']
        domain = from_address.split('@')[-1]

        if domain in domains:
            mail.store(num, '+FLAGS', '\\Deleted')
            print(f"Marked email from {from_address} for deletion")

    mail.expunge()
    print("Deleted emails from the delete list")



if __name__ == "__main__":
    mail = connect_to_yahoo_mail("im.praveen@yahoo.com", 
                          "iuimgmpjwjoeaxsd")
    
    since_date = (datetime.date.today() - datetime.timedelta(60)).strftime("%d-%b-%Y")
    before_date = (datetime.date.today() - datetime.timedelta(30)).strftime("%d-%b-%Y")

    email_mark_as_read(mail, since_date, before_date)
    email_delete(mail, since_date, before_date)
    mail.close()

    print("CLEANUP COMPLETE")