from tkinter import Tk,Label,Frame,Entry,Button,messagebox,filedialog
from tkinter.ttk import Combobox
import os,shutil
import time
from PIL import Image,ImageTk
import random
import project_tables
import sqlite3
import project_mails 


def generate_captcha():
    captcha=[]
    for i in range(3):
        c=chr(random.randint(65,90))
        captcha.append(c)


        n=random.randint(0,9)
        captcha.append(str(n))


    random.shuffle(captcha)
    captcha=''.join(captcha)
    return(captcha)

def refresh():
    captcha=generate_captcha()
    captcha_lbl.configure(text=captcha)


root=Tk()
root.state("zoomed")
root.configure(bg='powder blue')
root.title("ABC Bank")
root.resizable(width=False,height=False)

title_lbl=Label(root,text="Banking Automation",bg="powder blue",font=('Arial',40,"bold","underline") )
title_lbl.pack()

today_lbl=Label(root,text=time.strftime("%A,%d %B %Y"),bg="powder blue",font=('Arial',15,"bold"),fg='blue' )
today_lbl.pack(pady=10)

img=Image.open("images/logo.jpg.png").resize((180,180))
img_bitmap=ImageTk.PhotoImage(img,master=root)

logo_lbl=Label(root,image=img_bitmap)
logo_lbl.place(relx=0,rely=0)

footer_lbl=Label(root,text="Developed by Kapil",bg='powder blue',fg='blue',font=('Arial',15,"bold"))
footer_lbl.pack(side='bottom',pady=10)

def main_screen():
    def forgot():
        frm.destroy()
        forgot_screen()


    def login():
        uacn=acn_entry.get()
        upass=pass_entry.get()
        ucap=inputcap_entry.get()
        utype=user_combo.get()
        actual_cap=captcha_lbl.cget("text")
        actual_cap=actual_cap.replace(' ','')
        

        if utype=="Admin": 
            if uacn=='0' and upass=="admin":
                if ucap==actual_cap:
                   frm.destroy()
                   admin_screen()
                else:
                    messagebox.showerror('login','invalid captcha')
            else:
               messagebox.showerror('login','invalid ACN/PASS/TYPE')
       
        elif utype=="User":
            if ucap==actual_cap:
                conobj=sqlite3.connect(database='bank.sqlite')
                curobj=conobj.cursor()
                query='select * from accounts where accounts_acno=? and accounts_pass=?'
                curobj.execute(query,(uacn,upass))

                tup=curobj.fetchone()
                conobj.close()
                if tup==None:
                    messagebox.showerror("User Login","Invalid ACN/PASS")
                else:
                    frm.destroy()
                    user_screen(uacn)
            else:
                messagebox.showerror('login','invalid captcha')

            
        else:
            messagebox.showerror("login","Kindely Select Valid User Type")



    frm=Frame(root)
    frm.configure(bg='pink')
    frm.place(relx=0,rely=.17,relwidth=1,relheight=.78)

    user_lbl=Label(frm,text="User Type",bg='pink',font=('Arial',20,"bold"))
    user_lbl.place(relx=.3,rely=.1)

    user_combo=Combobox(frm,values=['Admin','User','---Select---'],font=('',20),state='readonly')
    user_combo.current(2)
    user_combo.place(relx=.45,rely=.1)


    acn_lbl=Label(frm,text="ACN",bg='pink',font=('Arial',20,"bold"))
    acn_lbl.place(relx=.3,rely=.2)

    acn_entry=Entry(frm,font=('Arial',20),bd=5)
    acn_entry.place(relx=.45,rely=.2)
    acn_entry.focus()

    pass_lbl=Label(frm,text="PASS",bg='pink',font=('Arial',20,"bold"))
    pass_lbl.place(relx=.3,rely=.3)



    pass_entry=Entry(frm,font=('Arial',20),bd=5,show="*")
    pass_entry.place(relx=.45,rely=.3)

    global captcha_lbl
    captcha_lbl=Label(frm,text=generate_captcha(),bg='white',font=('Arial',20,"bold"))
    captcha_lbl.place(relx=.47,rely=.5)


    refresh_btn=Button(frm,text="refresh",fg="blue",command=refresh)
    refresh_btn.place(relx=.58,rely=.5)


    inputcap_lbl=Label(frm,text="Captcha",bg='pink',font=('Arial',20,"bold"))
    inputcap_lbl.place(relx=.3,rely=.6)

    inputcap_entry=Entry(frm,font=('Arial',20),bd=5)
    inputcap_entry.place(relx=.45,rely=.6)

    login_btn=Button(frm,text="login",bg="powder blue",font=('Arial',15,"bold"),bd=5,command=login)
    login_btn.place(relx=.48,rely=.7)

    reset_btn=Button(frm,text="reset",bg="powder blue",font=('Arial',15,"bold"),bd=5)
    reset_btn.place(relx=.61,rely=.7)

    forgot_btn=Button(frm,width=18,text="forgot password",bg="powder blue",font=('Arial',17,"bold"),command=forgot)
    forgot_btn.place(relx=.47,rely=.85)

    
def admin_screen():
   def open_acn():
       def open_acn_db():
           uname=name_entry.get()
           uemail=email_entry.get()
           umob=mob_entry.get()
           ugender=gender_combo.get()
           ubal=0.0
           uopendate=time.strftime("%A,%d %B %y")
           upass=generate_captcha().replace(' ','')

           conobj=sqlite3.connect(database='bank.sqlite')
           curobj=conobj.cursor()
           

           query='insert into accounts values(null,?,?,?,?,?,?,?)'
           curobj.execute(query,(uname,upass,uemail,umob,ugender,uopendate,ubal))
           conobj.commit()
           conobj.close()
          # messagebox.showinfo('open Account','Account opened succesfully')
      
           conobj=sqlite3.connect(database='bank.sqlite')
           curobj=conobj.cursor()
           
           query="select max(accounts_acno)from accounts"
           curobj.execute(query)

           uacno=curobj.fetchone()[0]
           conobj.close()

           try:

               project_mails.send_mails_for_openacn(uemail,uacno,uname,upass,uopendate)
               msg=f'Account opened with ACN= {uacno} and mail sent {uemail},Kindly check spam also'
               messagebox.showinfo('Open Account',msg)

           except Exception as msg:
               messagebox.showerror("Open Account",msg)
        
       def reset():
           name_entry.delete(0,"end")
           email_entry.delete(0,"end")
           mob_entry.delete(0,"end")
           gender_combo.current(3)
           name_entry.focus()


       ifrm=Frame(frm,highlightthickness=2,highlightbackground='black')
       ifrm.configure(bg='white')
       ifrm.place(relx=.15,rely=.2,relwidth=.7,relheight=.7)

       title_lbl=Label(ifrm,text="This is open account screen",bg='white',font=('Arial',20,"bold"),fg='purple')
       title_lbl.pack()
       
       name_lbl=Label(ifrm,text="Name",bg='white',font=('Arial',15,"bold"))
       name_lbl.place(relx=.1,rely=.1)

       name_entry=Entry(ifrm,font=('Arial',15),bd=5)
       name_entry.place(relx=.1,rely=.18)
       name_entry.focus()

       email_lbl=Label(ifrm,text="Email",bg='white',font=('Arial',15,"bold"))
       email_lbl.place(relx=.1,rely=.4)

       email_entry=Entry(ifrm,font=('Arial',15),bd=5)
       email_entry.place(relx=.1,rely=.48)
        
       mob_lbl=Label(ifrm,text="Mob",bg='white',font=('Arial',15,"bold"))
       mob_lbl.place(relx=.6,rely=.1)

       mob_entry=Entry(ifrm,font=('Arial',15),bd=5)
       mob_entry.place(relx=.6,rely=.18)
       
       gender_lbl=Label(ifrm,text="Gender",bg='white',font=('Arial',15,"bold"))
       gender_lbl.place(relx=.6,rely=.4)

       gender_combo=Combobox(ifrm,values=['Male','Female','Other','---Select---'],font=('',15),state='readonly')
       gender_combo.current(3)
       gender_combo.place(relx=.6,rely=.48)

       opn_btn=Button(ifrm,text="Open Account",bg="powder blue",font=('Arial',15,"bold"),bd=5,command=open_acn_db)
       opn_btn.place(relx=.45,rely=.8)

       reset_btn=Button(ifrm,text="reset",bg="powder blue",font=('Arial',15,"bold"),bd=5,command=reset)
       reset_btn.place(relx=.75,rely=.8)


   def delete_acn():
       
       def send_otp():
           uacn=acn_entry.get()
    

           conobj=sqlite3.connect(database='bank.sqlite')
           curobj=conobj.cursor()
           query='select * from accounts where accounts_acno=?'
           curobj.execute(query,(uacn))

           tup=curobj.fetchone()
           conobj.close()
           if tup==None:
                messagebox.showerror("Delete Account","Record not found")
           else:
               otp=str(random.randint(1000,9999))
               project_mails.send_otp(tup[3],tup[1],otp)
               messagebox.showinfo('Delete Account','otp sent to given/registered mail id')

               otp_entry=Entry(ifrm,font=('Arial',15),bd=5)
               otp_entry.place(relx=.45,rely=.6)

               def verify():
                uotp=otp_entry.get()
                if otp==uotp:
                    resp=messagebox.askyesno("Delete Account",f"Do want to delete this Account ?")
                    if not resp:
                        frm.destroy()
                        admin_screen()
                        return
                    conobj=sqlite3.connect(database='bank.sqlite')
                    curobj=conobj.cursor()
                    query='delete  from accounts where accounts_acno=?'
                    curobj.execute(query,(uacn))
                    conobj.commit()
                    conobj.close()
                    messagebox.showinfo("Delete Account","Account Deleted")
                    frm.destroy()
                    admin_screen()

                    
                else:
                    messagebox.showerror("Delete Account","Incorrect OTP")

               verify_btn=Button(ifrm,text="verify",bg="powder blue",font=('Arial',14,"bold"),bd=5,command=verify)
               verify_btn.place(relx=.72,rely=.6)


       ifrm=Frame(frm,highlightthickness=2,highlightbackground='black')
       ifrm.configure(bg='white')
       ifrm.place(relx=.15,rely=.2,relwidth=.7,relheight=.7)

       title_lbl=Label(ifrm,text="This is delete account screen",bg='white',font=('Arial',20,"bold"),fg='purple')
       title_lbl.pack()
    
       acn_lbl=Label(ifrm,text="ACN",bg='white',font=('Arial',15,"bold"))
       acn_lbl.place(relx=.3,rely=.2)

       acn_entry=Entry(ifrm,font=('Arial',15),bd=5)
       acn_entry.place(relx=.45,rely=.2)
       acn_entry.focus()

       otp_btn=Button(ifrm,text="send OTP",bg="powder blue",font=('Arial',14,"bold"),bd=5,command=send_otp)
       otp_btn.place(relx=.45,rely=.4)

      
   def view_acn():
       def view_details():
           uacn=acn_entry.get()
           conobj=sqlite3.connect(database='bank.sqlite')
           curobj=conobj.cursor()
           query='select * from accounts where accounts_acno=?'
           curobj.execute(query,(uacn))

           tup=curobj.fetchone()
           conobj.close()
           if tup==None:
               messagebox.showerror("View Account","Record not Found")
           else:
               details=f"""User Name= {tup[1]}
                Aval Bal= {tup[7]}
                ACN Open date ={tup[6]}
                Email ={tup[3]}
                Mob ={tup[4]}
                """
               messagebox.showinfo("view account",details)
             
       
       ifrm=Frame(frm,highlightthickness=2,highlightbackground='black')
       ifrm.configure(bg='white')
       ifrm.place(relx=.15,rely=.2,relwidth=.7,relheight=.7)

       title_lbl=Label(ifrm,text="This is view account screen",bg='white',font=('Arial',20,"bold"),fg='purple')
       title_lbl.pack()

       acn_lbl=Label(ifrm,text="ACN",bg='white',font=('Arial',15,"bold"))
       acn_lbl.place(relx=.3,rely=.2)

       acn_entry=Entry(ifrm,font=('Arial',15),bd=5)
       acn_entry.place(relx=.45,rely=.2)
       acn_entry.focus()

       view_btn=Button(ifrm,text="View",bg="powder blue",font=('Arial',14,"bold"),bd=5,command=view_details)
       view_btn.place(relx=.45,rely=.4)




   def logout():
        resp=messagebox.askyesno("logout","Do you want to logout ?")
        if resp:
           frm.destroy()
           main_screen()


     
   frm=Frame(root)
   frm.configure(bg='pink')
   frm.place(relx=0,rely=.17,relwidth=1,relheight=.78)


   wel_lbl=Label(frm,text="Welcome,Admin",bg='pink',font=('Arial',20,"bold"),fg='green')
   wel_lbl.place(relx=0,rely=0)


   logout_btn=Button(frm,text="logout",bg="powder blue",font=('Arial',15,"bold"),bd=5,command=logout)
   logout_btn.place(relx=.9,rely=0)


   open_btn=Button(frm,text="open account",bg="green",font=('Arial',15,"bold"),fg='white',bd=5,command=open_acn)
   open_btn.place(relx=.2,rely=0)


   delete_btn=Button(frm,text="delete account",bg="red",font=('Arial',15,"bold"),fg='white',bd=5,command=delete_acn)
   delete_btn.place(relx=.4,rely=0)


   view_btn=Button(frm,text="view account",bg="yellow",font=('Arial',15,"bold"),fg='black',bd=5,command=view_acn)
   view_btn.place(relx=.6,rely=0)


def forgot_screen():
    def back():
        frm.destroy()
        main_screen()

    def send_otp():
        uacn=acn_entry.get()
        uemail=email_entry.get()
        ucaptcha=inputcap_entry.get()
        if ucaptcha==forgot_captcha.replace(' ',''):
                  messagebox.showerror('Forgot password','Invalid captcha')
                  return

        #authnticate acn & email
        conobj=sqlite3.connect(database='bank.sqlite')
        curobj=conobj.cursor()
        query='select * from accounts where accounts_acno=? and accounts_email=?'
        curobj.execute(query,(uacn,uemail))

        tup=curobj.fetchone()
        curobj.close()
        if tup==None:
            messagebox.showerror("Forgot Password","Record not found")
        else:
            otp=str(random.randint(1000,9999))
            project_mails.send_otp(uemail,tup[1],otp)
            messagebox.showinfo('Forgot Pass','otp sent to given/registered mail id')

            otp_entry=Entry(frm,font=('Arial',15),bd=5)
            otp_entry.place(relx=.45,rely=.7)

            def verify():
                uotp=otp_entry.get()
                if otp==uotp:
                    messagebox.showinfo("Forgot Password",f"Your Pass={tup[2]}")
                else:
                    messagebox.showerror("Forgot Password","Incorrect OTP")

            verify_btn=Button(frm,text="verify",bg="powder blue",font=('Arial',14,"bold"),bd=5,command=verify)
            verify_btn.place(relx=.7,rely=.7)


        #send otp
        #generate entry to enter otp


    frm=Frame(root)
    frm.configure(bg='pink')
    frm.place(relx=0,rely=.17,relwidth=1,relheight=.78)

    back_btn=Button(frm,text="back",bg="powder blue",font=('Arial',15,"bold"),bd=5,command=back)
    back_btn.place(relx=0,rely=0)

    acn_lbl=Label(frm,text="ACN",bg='pink',font=('Arial',15,"bold"))
    acn_lbl.place(relx=.3,rely=.2)

    acn_entry=Entry(frm,font=('Arial',15),bd=5)
    acn_entry.place(relx=.45,rely=.2)
    acn_entry.focus()

    email_lbl=Label(frm,text="Email",bg='pink',font=('Arial',15,"bold"))
    email_lbl.place(relx=.3,rely=.3)

    email_entry=Entry(frm,font=('Arial',15),bd=5)
    email_entry.place(relx=.45,rely=.3)
    

    global captcha_lbl
    forgot_captcha=generate_captcha()
    captcha_lbl=Label(frm,text=forgot_captcha,bg='white',font=('Arial',15,"bold"))
    captcha_lbl.place(relx=.47,rely=.5)


    refresh_btn=Button(frm,text="refresh",fg="blue",command=refresh)
    refresh_btn.place(relx=.58,rely=.5)
     
    inputcap_entry=Entry(frm,font=('Arial',15),bd=5)
    inputcap_entry.place(relx=.45,rely=.6)

    
    otp_btn=Button(frm,text="send OTP",bg="powder blue",font=('Arial',14,"bold"),bd=5,command=send_otp)
    otp_btn.place(relx=.45,rely=.78)

    reset_btn=Button(frm,text="reset",bg="powder blue",font=('Arial',15,"bold"),bd=5)
    reset_btn.place(relx=.58,rely=.78)


def user_screen(uacn=None):
    def logout():
        resp=messagebox.askyesno("logout","Do you want to logout ?")
        if resp:
           frm.destroy()
           main_screen()

    def update_btn_screen():
       def update_db():
           uname=name_entry.get()
           upass=name_entry.get()
           uemail=name_entry.get()
           umob=name_entry.get()

           conobj=sqlite3.connect(database='bank.sqlite')
           curobj=conobj.cursor()

           query='update accounts set accounts_name=?,accounts_pass=?,accounts_email=?,accounts_mob=? ,where accounts_acno=?'
           curobj.execute(query,(uname,upass,uemail,umob,uacn))
           conobj.commit()
           conobj.close()
           messagebox.showinfo("Update details","Profile Updated")
           frm.destroy()
           user_screen(uacn)



       ifrm=Frame(frm,highlightthickness=2,highlightbackground='black')
       ifrm.configure(bg='white')
       ifrm.place(relx=.2,rely=.2,relwidth=.7,relheight=.7)

       title_lbl=Label(ifrm,text="This is update screen",bg='white',font=('Arial',20,"bold"),fg='purple')
       title_lbl.pack()

       conobj=sqlite3.connect(database='bank.sqlite')
       curobj=conobj.cursor()
       curobj.execute('select * from accounts where accounts_acno=?',(uacn)) 
       tup=curobj.fetchone()
       conobj.close()
       

       name_lbl=Label(ifrm,text="Name",bg='white',font=('Arial',15,"bold"))
       name_lbl.place(relx=.1,rely=.1)

       name_entry=Entry(ifrm,font=('Arial',15),bd=5)
       name_entry.place(relx=.1,rely=.18)
       name_entry.insert(0,tup[1])
       name_entry.focus()

       email_lbl=Label(ifrm,text="Email",bg='white',font=('Arial',15,"bold"))
       email_lbl.place(relx=.1,rely=.4)

       email_entry=Entry(ifrm,font=('Arial',15),bd=5)
       email_entry.place(relx=.1,rely=.48)
       email_entry.insert(0,tup[3])
        
       mob_lbl=Label(ifrm,text="Mob",bg='white',font=('Arial',15,"bold"))
       mob_lbl.place(relx=.6,rely=.1)

       mob_entry=Entry(ifrm,font=('Arial',15),bd=5)
       mob_entry.place(relx=.6,rely=.18)
       mob_entry.insert(0,tup[4])
       
       pass_lbl=Label(ifrm,text="pass",bg='white',font=('Arial',15,"bold"))
       pass_lbl.place(relx=.6,rely=.4)

       pass_entry=Entry(ifrm,font=('Arial',15),bd=5)
       pass_entry.place(relx=.6,rely=.48)
       pass_entry.insert(0,tup[2])

       update_btn=Button(ifrm,text="update",bg="powder blue",font=('Arial',15,"bold"),bd=5,command=update_db)
       update_btn.place(relx=.45,rely=.8)


    def deposit_btn_screen():
       def deposit():
           uamt=float(amt_entry.get())
           conobj=sqlite3.connect(database='bank.sqlite')
           curobj=conobj.cursor()
           query='update accounts set accounts_bal=accounts_bal+? where accounts_acno=?'
           curobj.execute(query,(uamt,uacn))
           conobj.commit()
           conobj.close()

           conobj=sqlite3.connect(database='bank.sqlite')
           curobj=conobj.cursor()
           query='select accounts_bal from accounts where accounts_acno=?'
           curobj.execute(query,(uacn,))
           ubal=curobj.fetchone()[0]
           conobj.close()

           t=str(time.time())
           utxnid='txn'+t[:t.index('.')]
           conobj=sqlite3.connect(database='bank.sqlite')
           curobj=conobj.cursor()
           query='insert into stmts values(?,?,?,?,?,?)'
           curobj.execute(query,(uacn,uamt,'CR.',time.strftime("%d-%m-%Y %r"),ubal,utxnid))
           conobj.commit()
           conobj.close()

           messagebox.showinfo("Deposit",f"{uamt} Amount Deposited")
           frm.destroy()
           user_screen(uacn)



       ifrm=Frame(frm,highlightthickness=2,highlightbackground='black')
       ifrm.configure(bg='white')
       ifrm.place(relx=.2,rely=.2,relwidth=.7,relheight=.7)

       title_lbl=Label(ifrm,text="This is deposit screen",bg='white',font=('Arial',20,"bold"),fg='purple')
       title_lbl.pack()

       amt_lbl=Label(ifrm,text="Amount",bg='white',font=('Arial',15,"bold"))
       amt_lbl.place(relx=.3,rely=.2)

       amt_entry=Entry(ifrm,font=('Arial',15),bd=5)
       amt_entry.place(relx=.45,rely=.2)
       amt_entry.focus()

       dep_btn=Button(ifrm,text="deposit",bg="powder blue",font=('Arial',14,"bold"),bd=5,command=deposit)
       dep_btn.place(relx=.45,rely=.4)
   
    def withdraw_btn_screen():
       def withdraw():
            uamt=float(amt_entry.get())
            conobj=sqlite3.connect(database='bank.sqlite')
            curobj=conobj.cursor()
            query='select accounts_bal from accounts where accounts_acno=?'
            curobj.execute(query,(uacn,))
            ubal=curobj.fetchone()[0]
            conobj.close()

            if ubal>=uamt:
                
                
                conobj=sqlite3.connect(database='bank.sqlite')
                curobj=conobj.cursor()
                query='update accounts set accounts_bal=accounts_bal-? where accounts_acno=?'
                curobj.execute(query,(uamt,uacn))
                conobj.commit()
                conobj.close()

                

                t=str(time.time())
                utxnid='txn'+t[:t.index('.')]
                conobj=sqlite3.connect(database='bank.sqlite')
                curobj=conobj.cursor()
                query='insert into stmts values(?,?,?,?,?,?)'
                curobj.execute(query,(uacn,uamt,'DB.',time.strftime("%d-%m-%Y %r"),ubal-uamt,utxnid))
                conobj.commit()
                conobj.close()

                messagebox.showinfo("Deposit",f"{uamt} Amount Withdrawn")
                frm.destroy()
                user_screen(uacn)
            else:
                messagebox.showerror("Withdraw",f"Insufficient Bal {ubal}")



       ifrm=Frame(frm,highlightthickness=2,highlightbackground='black')
       ifrm.configure(bg='white')
       ifrm.place(relx=.2,rely=.2,relwidth=.7,relheight=.7)

       title_lbl=Label(ifrm,text="This is withdraw screen",bg='white',font=('Arial',20,"bold"),fg='purple')
       title_lbl.pack()

       amt_lbl=Label(ifrm,text="Amount",bg='white',font=('Arial',15,"bold"))
       amt_lbl.place(relx=.3,rely=.2)

       amt_entry=Entry(ifrm,font=('Arial',15),bd=5)
       amt_entry.place(relx=.45,rely=.2)
       amt_entry.focus()

       dep_btn=Button(ifrm,text="Withdraw",bg="powder blue",font=('Arial',14,"bold"),bd=5,command=withdraw)
       dep_btn.place(relx=.45,rely=.4)


    def check_btn_screen():
       ifrm=Frame(frm,highlightthickness=2,highlightbackground='black')
       ifrm.configure(bg='white')
       ifrm.place(relx=.2,rely=.2,relwidth=.7,relheight=.7)

       title_lbl=Label(ifrm,text="This is details screen",bg='white',font=('Arial',20,"bold"),fg='purple')
       title_lbl.pack()

       conobj=sqlite3.connect(database='bank.sqlite')
       curobj=conobj.cursor()
       curobj.execute('select * from accounts where accounts_acno=?',(uacn)) 
       tup=curobj.fetchone()
       conobj.close()

       details=f'''Account No. = {tup[0]}

             Opening Date = {tup[6]}

            Available Bal = {tup[7]}

             Email = {tup[3]}
                    
             mob = {tup[4]}
                    ''' 
       details_lbl=Label(ifrm,text=details,bg='white',fg='purple',font=('arial',16,'bold'))
       details_lbl.place(relx=.2,rely=.2)
    
    def transfer_btn_screen():
       def transfer():
            toacn=to_entry.get()
            uamt=float(amt_entry.get())

            conobj=sqlite3.connect(database='bank.sqlite')
            curobj=conobj.cursor()
            query='select * from accounts where accounts_acno=?'
            curobj.execute(query,(toacn,))
            to_tup=curobj.fetchone()
            conobj.close()

            if to_tup==None:
                messagebox.showerror("Transfer","To ACN does not exist")
                return
            

            conobj=sqlite3.connect(database='bank.sqlite')
            curobj=conobj.cursor()
            query='select accounts_bal from accounts where accounts_acno=?'
            curobj.execute(query,(uacn,))
            ubal=curobj.fetchone()[0]
            conobj.close()

            if ubal>=uamt:
                
                
                conobj=sqlite3.connect(database='bank.sqlite')
                curobj=conobj.cursor()
                query_deduct='update accounts set accounts_bal=accounts_bal-? where accounts_acno=?'
                query_credit='update accounts set accounts_bal=accounts_bal+? where accounts_acno=?'
                
                curobj.execute(query_deduct,(uamt,uacn))
                curobj.execute(query_credit,(uamt,toacn))


                conobj.commit()
                conobj.close()

                

                t=str(time.time())
                utxnid1='txn_db'+t[:t.index('.')]
                utxnid2='txn_cr'+t[:t.index('.')]
                conobj=sqlite3.connect(database='bank.sqlite')
                curobj=conobj.cursor()
                query1='insert into stmts values(?,?,?,?,?,?)'
                query2='insert into stmts values(?,?,?,?,?,?)'


                curobj.execute(query1,(uacn,uamt,'DB.',time.strftime("%d-%m-%Y %r"),ubal-uamt,utxnid1))
                curobj.execute(query2,(toacn,uamt,'CR.',time.strftime("%d-%m-%Y %r"),ubal+uamt,utxnid2))

                conobj.commit()
                conobj.close()

                messagebox.showinfo("transfer",f"{uamt} Amount Transferred")
                frm.destroy()
                user_screen(uacn)
            else:
                messagebox.showerror("Transfer",f"Insufficient Bal {ubal}")
           
       ifrm=Frame(frm,highlightthickness=2,highlightbackground='black')
       ifrm.configure(bg='white')
       ifrm.place(relx=.2,rely=.2,relwidth=.7,relheight=.7)

       title_lbl=Label(ifrm,text="This is transfer screen",bg='white',font=('Arial',20,"bold"),fg='purple')
       title_lbl.pack()

       to_lbl=Label(ifrm,text="TO ACN",bg='white',font=('Arial',15,"bold"))
       to_lbl.place(relx=.3,rely=.2)

       to_entry=Entry(ifrm,font=('Arial',15),bd=5)
       to_entry.place(relx=.45,rely=.2)
       to_entry.focus()

       amt_lbl=Label(ifrm,text="Amount",bg='white',font=('Arial',15,"bold"))
       amt_lbl.place(relx=.3,rely=.4)

       amt_entry=Entry(ifrm,font=('Arial',15),bd=5)
       amt_entry.place(relx=.45,rely=.4)
       

       tr_btn=Button(ifrm,text="transfer",bg="powder blue",font=('Arial',14,"bold"),bd=5,command=transfer)
       tr_btn.place(relx=.55,rely=.6)


    def history_btn_screen():
       
       ifrm=Frame(frm,highlightthickness=2,highlightbackground='black')
       ifrm.configure(bg='white')
       ifrm.place(relx=.2,rely=.2,relwidth=.7,relheight=.7)

       title_lbl=Label(ifrm,text="This is txn history screen",bg='white',font=('Arial',20,"bold"),fg='purple')
       title_lbl.pack()
       
       import tktable_project
        
       Table_headers = ("Txn ID","Amount","Txn Type","Updated Bal","Date")
       mytable = tktable.Table(ifrm,Table_headers,col_width=150,headings_bold=True)
       mytable.pack(pady=10)

       conobj=sqlite3.connect(database='bank.sqlite')
       curobj=conobj.cursor()
       query='select stmts_txnid,stmts_amt,stmts_type,stmts_update_bal,stmts_date from stmts where stmts_acn=? '
       curobj.execute(query,(uacn,))
       for tup in curobj:
           mytable.insert_row(tup)
       conobj.close()

       import sys
       del sys.modules['tktable']
 

    def getdetail():
        conobj=sqlite3.connect(database='bank.sqlite')
        curobj=conobj.cursor()
        query='select * from accounts where accounts_acno=? '
        curobj.execute(query,(uacn,))
        tup=curobj.fetchone()
        conobj.close()
        return tup
    

    def update_picture():
        path=filedialog.askopenfilename()
        shutil.copy(path,f'images/{uacn}.png')

        profile_img=Image.open(f"images/{uacn}.png").resize((130,140))
        bitmap_profile_img=ImageTk.PhotoImage(profile_img,master=root)
        profile_img_lbl.image=bitmap_profile_img
        profile_img_lbl.configure(image=bitmap_profile_img)
           
    
    frm=Frame(root)
    frm.configure(bg='pink')
    frm.place(relx=0,rely=.17,relwidth=1,relheight=.78)

    wel_lbl=Label(frm,text=f"Welcome,{getdetail()[1]}",bg='pink',font=('Arial',20,"bold"),fg='green')
    wel_lbl.place(relx=0,rely=0)


    logout_btn=Button(frm,text="logout",bg="powder blue",font=('Arial',15,"bold"),bd=5,command=logout)
    logout_btn.place(relx=.93,rely=0)
 
    if os.path.exists(f'images/{uacn}.png'):
        path=f"images/{uacn}.png"
    else:
        path="images/default picture.webp"   


    profile_img=Image.open(path).resize((130,140))
    bitmap_profile_img=ImageTk.PhotoImage(profile_img,master=root)
    profile_img_lbl=Label(frm,image=bitmap_profile_img)
    profile_img_lbl.image=bitmap_profile_img
    profile_img_lbl.place(relx=0.01,rely=.07)
    
    update_pic_btn = Button(frm, text="Update Picture", width=12, bg="yellow", font=('Arial', 12, "bold"), bd=5, fg='black',command=update_picture)
    update_pic_btn.place(relx=0.01, rely=0.35)


    check_btn = Button(frm,text="Check details", width=12, bg="yellow", font=('Arial', 12, "bold"), bd=5, fg='black',command=check_btn_screen)
    check_btn.place(relx=0.01, rely=0.44)

    deposit_btn = Button(frm, text="Deposit", width=12, bg="green", font=('Arial', 12, "bold"), bd=5, fg='black',command=deposit_btn_screen)
    deposit_btn.place(relx=0.01, rely=0.53)

    withdraw_btn = Button(frm, text="Withdraw", width=12, bg="red", font=('Arial', 12, "bold"), bd=5, fg='black',command=withdraw_btn_screen)
    withdraw_btn.place(relx=0.01, rely=0.62)

    update_btn = Button(frm, text="Update", width=12, bg="powder blue", font=('Arial', 12, "bold"), bd=5, fg='black',command=update_btn_screen)
    update_btn.place(relx=0.01, rely=0.71)

    transfer_btn = Button(frm, text="Transfer", width=12, bg="red", font=('Arial', 12, "bold"), bd=5, fg='black',command=transfer_btn_screen)
    transfer_btn.place(relx=0.01, rely=0.80)

    history_btn = Button(frm, text="History", width=12, bg="powder blue", font=('Arial', 12, "bold"), bd=5, fg='black',command=history_btn_screen)
    history_btn.place(relx=0.01, rely=0.89)


main_screen()
root.mainloop()