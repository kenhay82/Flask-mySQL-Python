from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

# Definiendo App
app = Flask(__name__)

# MySQL connnection
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'flask_mysql_python'
mysql = MySQL(app)

# Session Setting
app.secret_key = 'mysecretkey'

# Rutas
@app.route('/')
def index():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM contacts')
    data = cur.fetchall()
    return render_template('index.html', contacts = data)

@app.route('/add_contact', methods=['POST'])
def add_contact():
    if request.method == 'POST':
        fullname = request.form['fullname']
        phone = request.form['phone']
        email = request.form['email']
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO contacts (fullname, phone, email) VALUES (%s,%s,%s)',(fullname,phone,email))
        mysql.connection.commit()
        cur.close()
        flash('Contact Added Successfully')
        return redirect(url_for('index'))

@app.route('/edit_contact/<string:id>') # El tipo de dato se puede obviar al momento de pasar el parametro
def get_contact(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM contacts WHERE id = {0}'.format(id))
    data = cur.fetchall()    
    return render_template('edit_contact.html',contact = data[0])

@app.route('/update/<id>', methods = ['POST'])
def update_contact(id):
    if request.method == 'POST':
        fullname = request.form['fullname']
        phone = request.form['phone']
        email = request.form['email']
    cur = mysql.connection.cursor()
    cur.execute("""
        UPDATE contacts
        SET fullname = %s,
            phone = %s,
            email = %s
        WHERE id = %s
    """,(fullname,phone,email,id))
    mysql.connection.commit()
    cur.close()
    flash('Contact Updated Successfully')
    return redirect(url_for('index'))

@app.route('/delete_contact/<id>')
def delete_contact(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM contacts WHERE id = {0}'.format(id))
    mysql.connection.commit()
    cur.close()
    flash('Contact Removed Succesfully')
    return redirect(url_for('index'))
    

if __name__ == '__main__':
    app.run(port = 3000,debug = True)