from email.mime.text import MIMEText
import datetime
import smtplib

def send_email(email,query_result):

    from_email="householdapp84@gmail.com"
    from_pwd="python61collegeville"
    to_email=email

    today=datetime.date.today()

    subject="Household Spendings-%s" %today
    ctr=0

    for result in query_result:
        if ctr==0:
            op=result[0]+" "+str(result[1])+"\n"
        else:
            op=op+result[0]+" "+str(result[1])+"\n"
        ctr+=1

    greeting="Hey there, see below your total spendings by category for current month\n\n"
    message=greeting+op

    print(message)

    msg=MIMEText(message,'plain')
    msg['Subject']=subject
    msg['To']=to_email
    msg['From']=from_email

    gmail=smtplib.SMTP('smtp.gmail.com',587)
    gmail.ehlo()
    gmail.starttls()
    gmail.login(from_email,from_pwd)
    gmail.send_message(msg)


if __name__=="__main__":
    rs=[("abc",56.78),("def",89.78)]
    send_email("bharathramj@yahoo.com",rs)