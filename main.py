from flask import Flask, render_template, request
import pymysql as pm

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/result', methods=["GET", "POST"])
def result():
	if request.method == "POST":
		authors = request.form['author']
		con = pm.connect('localhost', 'root', '', 'polling')
		cursor = con.cursor()
		query = "insert into user_author values('%s')" % (authors)
		cursor.execute(query) 
		try:
			con.commit()
		except:
			con.rollback()		
		con.close()
	return render_template('index.html')

@app.route('/output', methods=['GET', 'POST'])
def view():
	con = pm.connect('localhost', 'root', '', 'polling')
	cursor = con.cursor()
	query = "Select count(authors), authors from user_author group by authors"
	cursor.execute(query)
	result = cursor.fetchall()
	con.commit()
	con.close()
	return render_template('result.html',  data = result)


if __name__ == '__main__':
    app.run(debug=True)
