from flask import Flask, render_template, request

app=Flask(__name__)


import mysql.connector

con=mysql.connector.connect(host='localhost',database='bank',user='root',password='')
cursor=con.cursor()


@app.route('/')
def index():
	return render_template('indexpg.html')

@app.route('/reg')
def reg():
	return render_template('regist.html')

@app.route('/log',methods=['GET','POST'])
def login():
	if request.method == 'POST':
		user=request.form['u']
		passw=request.form['p']
		query="select Name,pass from scsbank"

		cursor.execute(query)
		result=cursor.fetchall()

		for u,p in result:
			if u==user and p==passw:
				query="select * from scsbank"
				cursor.execute(query)
				result=cursor.fetchall()
				for i in result:
					if i[0] == u:
						return render_template('welcome.html',name=u,ac=i[1],bal=i[2],pan=i[3],tp=i[4],mob=i[5])
		return render_template('indexpg.html')
	return render_template('indexpg.html')

@app.route('/trans',methods=['POST','GET'])
def tran():
	if request.method == 'POST':
		p=request.form['payee']
		s=request.form['accc']
		amnt=request.form['bal']

		s=int(s)
		p=int(p)
		amnt=int(amnt)

		query="select * from scsbank"
		cursor.execute(query)
		result=cursor.fetchall()
		x=y=''
		for i in result:
			if i[1]==s:
				x=i
			elif i[1]==p:
				y=i
		
		x1=x[2]-amnt
		query="update scsbank set Balence=%s where ACno=%s"
		cursor.execute(query,(x1,x[1]))
		y1=y[2]+amnt
		cursor.execute(query,(y1,y[1]))
		con.commit()

		query="insert into transac (Sender,Receiver,Amnt) values (%s,%s,%s)"
		cursor.execute(query,(s,p,amnt))
		con.commit()
		
	return render_template('welcome.html',name=x[0],ac=x[1],bal=x1,pan=x[3],tp=x[4],mob=x[5])

@app.route('/admin')
def admin():
	query="select * from  transac"
	cursor.execute(query)
	result=cursor.fetchall()
	result=list(result)

	return render_template("admin.html",details=result)

@app.route('/db', methods=['GET','POST'])
def create():
	if request.method == 'POST':
		name=request.form['n1']
		pan=request.form['n2']
		mob=request.form['n4']
		actype=request.form['n3']
		bal=request.form['n5']
		passw=request.form['n6']
		query="insert into scsbank(Name,Balence,PAN,Type,mob,pass) values (%s,%s,%s,%s,%s,%s)"

		args=(name,bal,pan,actype,mob,passw)

		cursor.execute(query,args)
		con.commit()
		return render_template('indexpg.html')

if __name__ == '__main__':
	app.run()
