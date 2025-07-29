import gmail
email = 'xxxxxxxx@gmail.com' #mention your gmail id
app_pass ='xxxxxxxxxx'       #mention app pass of same gmail account

def send_mails_for_openacn(to_mail,uacno,uname,upass,udate):

        con = gmail.GMail(email,app_pass)
        sub='Account Opened with ABC Bank'
        
        body = f"""Dear {uname},

Your account has been opened successfully with ABC Bank. Details are:
Account No: {uacno}
Password: {upass}
Opening Date: {udate}

Kindly change your password when you login for the first time.

Thanks,
ABC Bank
Noida
"""
        msg = gmail.Message(to=to_mail,subject=sub,text=body)
        con.send(msg)
       

def send_otp(to_mail,uname,uotp):
    con = gmail.GMail(email,app_pass)
    sub='Otp to get password recovery'
    body=f"""Dear {uname},
        your OTP to get password = {uotp}  
    

    Kindly verify this otp to application.

    Thanks,
    ABC Bank
    Noida
    """

    msg = gmail.Message(to=to_mail, subject=sub, text=body)
    con.send(msg)