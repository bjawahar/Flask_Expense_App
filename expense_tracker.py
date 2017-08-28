from flask import Flask,render_template,request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from sqlalchemy import extract
from sqlalchemy import and_
import datetime
from send_email import send_email

app= Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root:penn#61wyo@localhost/expense_tracker_app'
db=SQLAlchemy(app)

class Data(db.Model):
    __tablename__="household_expense"
    id=db.Column(db.Integer, primary_key=True)
    date=db.Column(db.Date)
    email=db.Column(db.String(200))
    category=db.Column(db.String(200))
    sub_category=db.Column(db.String(200))
    business_name=db.Column(db.String(200))
    amount=db.Column(db.Float)

    def __init__(self,date,email,category,sub_category,business_name,amount):
        self.date=date
        self.email=email
        self.category=category
        self.sub_category=sub_category
        self.business_name=business_name
        self.amount=amount


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/success",methods=['POST'])
def success():
    if request.method=='POST':
        tran_dt=request.form["transaction_date"]
        email_addr=request.form["email_address"]
        exp_type=request.form["expense_type"]
        exp_sub_type=request.form["expense_sub_type"]
        bus_nm=request.form["business_nm"]
        amount=request.form["amount_spent"]
        data=Data(tran_dt,email_addr,exp_type,exp_sub_type,bus_nm,amount)
        db.session.add(data)
        db.session.commit()

        year=datetime.date.today().strftime("%Y")
        month=datetime.date.today().strftime("%m")


        qry=db.session.query(Data.category,func.sum(Data.amount)).filter(and_(extract('year',Data.date) == int(year),extract('month',Data.date) == int(month)))
        result=qry.group_by(Data.category).all()

        send_email(email_addr,result)

        print("Date of transaction:{}".format(tran_dt))
        print("Email Address:{}".format(email_addr))
        print("Category of spend:{}".format(exp_type))
        print("Sub-category of spend:{}".format(exp_sub_type))
        print("Amount Spent:{}".format(amount))
        return render_template("success.html")

if __name__ == '__main__':
    app.debug=True
    app.run()