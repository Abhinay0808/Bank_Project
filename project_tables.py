import sqlite3 
conobj=sqlite3.connect(database='bank.sqlite')
curobj=conobj.cursor()

table1='''create table  if not exists accounts(
accounts_acno integer primary key autoincrement,
accounts_name text,
accounts_pass text,
accounts_email text,
accounts_mob text,
accounts_gender text,
accounts_opendate text,
accounts_bal float)
'''

table2='''create table if not exists stmts(
stmts_acn integar,
stmts_amt  float,
stmts_type  text,
stmts_date  text,
stmts_update_bal  float,
stmts_txnid text primary key)
'''

try:
    curobj.execute(table1)
    curobj.execute(table2)
    print('table created')
except Exception as msg:
    print(msg)
conobj.close()