from flask import Flask, render_template, request, redirect, url_for, session, make_response, send_file
from flask_mysqldb import MySQL
import MySQLdb.cursors
import datetime
import pdfkit

from query.query_number import number_selection, query_selection

app = Flask(__name__)
# Change this to your secret key (can be anything, it's for extra protection)
app.secret_key = '12!@'

config = pdfkit.configuration(wkhtmltopdf='C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe')

# Enter your database connection details below
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '1234'
app.config['MYSQL_DB'] = 'samvedana'

# Intialize MySQL
mysql = MySQL(app)

month = datetime.datetime.now().strftime('%m')


@app.route('/', methods=['GET', 'POST'])
def login():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = %s AND password = %s', (username, password,))
        # Fetch one record and return result
        account = cursor.fetchone()
        # If account exists in accounts table in out database
        if account:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            # Redirect to home page
            return redirect(url_for('Distribution_menu'))
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'
    # Show the login form with message (if any)
    return render_template('login.html', msg=msg)


@app.route('/Distribution_menu')
def Distribution_menu():
    # Check if user is loggedin
    if 'loggedin' in session:
        # User is loggedin show them the home page
        return render_template('Distribution_menu.html', username=session['username'])
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))


@app.route("/registration", methods=['GET', 'POST'])
def registration():
    # Check if user is loggedin
    if 'loggedin' in session:
        msg = ''
        info = '0'
        account = {}
        # Check if "username" and "password" POST requests exist (user submitted form)
        if request.method == 'POST' and 'land_account' in request.form and 'name' in request.form and 'village_name' in request.form:
            # Create variables for easy access
            land_account = request.form['land_account']
            name = request.form['name']
            village_name = request.form['village_name']
            # Check if account exists using MySQL
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM beneficiary_detail WHERE land_accountnumber = %s', (land_account,))
            account = cursor.fetchone()
            # If account exists show error and validation checks
            if account:
                msg = 'Account already exists!'
                info = '3'
            elif not land_account or not name or not village_name:
                msg = 'Please fill out the form!'
                info = '2'
            else:
                # Account doesnt exists and the form data is valid, now insert new account into accounts table
                cursor.execute(
                    'INSERT INTO beneficiary_detail VALUES ("%s", "%s", "%s")' % (land_account, name, village_name))
                mysql.connection.commit()
                msg = 'You have successfully registered!'
                account = {'land_accountnumber': land_account, 'beneficiary_name': name, 'village_name': village_name}
                info = '1'
        elif request.method == 'POST':
            # Form is empty... (no POST data)
            msg = 'Please fill out the form!'
            info = '2'

        return render_template('beneficiary_registration.html', msg=msg, info=info, result=account)
    return redirect(url_for('login'))


@app.route('/ration', methods=['GET', 'POST'])
def ration():
    if 'loggedin' in session:
        msg = ''
        info = '0'
        result = {}
        land_an = land_search()

        # Check if "username" and "password" POST requests exist (user submitted form)
        if request.method == 'POST' and 'land_account' in request.form and 'type' in request.form and 'date' in request.form and 'quantity' in request.form:
            # Create variables for easy access
            land_account = request.form['land_account']
            type_ration = request.form['type']
            date = request.form['date']
            quantity = request.form['quantity']
            print(land_account)

            if type_ration == 'other':
                type_ration = request.form['type_other']

            # Check if account exists using MySQL
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor2 = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM beneficiary_detail WHERE land_accountnumber = %s', (land_account,))
            cursor2.execute('SELECT ration_details.land_accountnumber,beneficiary_detail.beneficiary_name,'
                            'beneficiary_detail.village_name,ration_details.date,ration_details.type from '
                            'samvedana.ration_details,samvedana.beneficiary_detail where '
                            'beneficiary_detail.land_accountnumber = ration_details.land_accountnumber and '
                            'ration_details.land_accountnumber= %s and month(date) = %s', (land_account, month))
            account = cursor.fetchone()
            result = cursor2.fetchone()

            print(result)
            # If account exists show error and validation checks
            if not account:
                msg = 'Land Account Number is not Register!!'
                info = '3'
            elif not land_account or not type_ration or not date or not quantity:
                msg = 'Please fill out the form!'
                info = '2'
            elif result:
                msg = 'Record Found!!'
                info = '4'
            else:
                cursor.execute(
                    'INSERT INTO ration_details VALUES ("%s", "%s", "%s","%d")' % (
                        land_account, type_ration, date, int(quantity)))
                mysql.connection.commit()
                msg = 'You have successfully registered!'
                info = '1'
        elif request.method == 'POST':
            # Form is empty... (no POST data)
            msg = 'Please fill out the form!'
            info = '2'

        return render_template('ration.html', msg=msg, info=info, result=result, landNumber=land_an)
    return redirect(url_for('login'))


@app.route('/sewingmachine', methods=['GET', 'POST'])
def sewingmachine():
    if 'loggedin' in session:
        msg = ''
        info = '0'
        result = {}
        land_an = land_search()

        # Check if "username" and "password" POST requests exist (user submitted form)
        if request.method == 'POST' and 'land_account' in request.form and 'date' in request.form and 'quantity' in request.form:
            # Create variables for easy access
            land_account = request.form['land_account']
            date = request.form['date']
            quantity = request.form['quantity']

            # Check if account exists using MySQL
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor2 = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM beneficiary_detail WHERE land_accountnumber = %s', (land_account,))
            cursor2.execute('SELECT sewingmachine_detail.land_accountnumber,beneficiary_detail.beneficiary_name,'
                            'beneficiary_detail.village_name,sewingmachine_detail.date from '
                            'samvedana.sewingmachine_detail,samvedana.beneficiary_detail where '
                            'beneficiary_detail.land_accountnumber = sewingmachine_detail.land_accountnumber and '
                            'sewingmachine_detail.land_accountnumber= %s and month(date) = %s', (land_account, month))
            account = cursor.fetchone()
            result = cursor2.fetchone()
            # If account exists show error and validation checks
            if not account:
                msg = 'Land Account Number is not Register!!'
                info = '3'
            elif not land_account or not date or not quantity:
                msg = 'Please fill out the form!'
                info = '2'
            elif result:
                msg = 'Record Found!!'
                info = '4'
            else:
                cursor.execute(
                    'INSERT INTO sewingmachine_detail (land_accountnumber,date,quantity) VALUES ("%s", "%s","%d")' % (
                        land_account, date, int(quantity)))
                mysql.connection.commit()
                msg = 'You have successfully registered!'
                info = '1'
        elif request.method == 'POST':
            # Form is empty... (no POST data)
            msg = 'Please fill out the form!'
            info = '2'

        return render_template('SewingMachine_detail.html', msg=msg, info=info, result=result, landNumber=land_an)
    return redirect(url_for('login'))


@app.route('/tadpatri', methods=['GET', 'POST'])
def tadpatri():
    if 'loggedin' in session:
        msg = ''
        info = '0'
        result = {}
        land_an = land_search()

        # Check if "username" and "password" POST requests exist (user submitted form)
        if request.method == 'POST' and 'land_account' in request.form and 'date' in request.form and 'quantity' in request.form:
            # Create variables for easy access
            land_account = request.form['land_account']
            date = request.form['date']
            quantity = request.form['quantity']

            # Check if account exists using MySQL
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM beneficiary_detail WHERE land_accountnumber = %s', (land_account,))
            cursor2 = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor2.execute('SELECT tadpatri_details.land_accountnumber,beneficiary_detail.beneficiary_name,'
                            'beneficiary_detail.village_name,tadpatri_details.date from '
                            'samvedana.tadpatri_details,samvedana.beneficiary_detail where '
                            'beneficiary_detail.land_accountnumber =tadpatri_details.land_accountnumber and '
                            'tadpatri_details.land_accountnumber = %s and month(date) = %s', (land_account, month))
            account = cursor.fetchone()
            result = cursor2.fetchone()

            # If account exists show error and validation checks
            if not account:
                msg = 'Land Account Number is not Register!!'
                info = '3'
            elif not land_account or not date or not quantity:
                msg = 'Please fill out the form!'
                info = '2'
            elif result:
                msg = 'Record Found!!'
                info = '4'
            else:
                cursor.execute(
                    'INSERT INTO tadpatri_details (land_accountnumber,date,quantity) VALUES ("%s", "%s","%d")' % (
                        land_account, date, int(quantity)))
                mysql.connection.commit()
                msg = 'You have successfully registered!'
                info = '1'
        elif request.method == 'POST':
            # Form is empty... (no POST data)
            msg = 'Please fill out the form!'
            info = '2'

        return render_template('tadpatri.html', msg=msg, info=info, result=result, landNumber=land_an)
    return redirect(url_for('login'))


@app.route('/logout')
def logout():
    # Remove session data, this will log the user out
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    # Redirect to login page
    return redirect(url_for('login'))


# Fetch land_account number
def land_search():
    an_cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    an_cursor.execute("SELECT land_accountnumber FROM samvedana.beneficiary_detail")
    land_an = an_cursor.fetchall()
    an_list = []
    for x in land_an:
        an_list.append(x['land_accountnumber'])
    return an_list


@app.route('/report', methods=['GET', 'POST'])
def report():
    info = '0'
    if 'loggedin' in session:
        land_an = land_search()
        return render_template('report.html', landNumber=land_an, info=info)
    return redirect(url_for('login'))


@app.route('/result', methods=['GET', 'POST'])
def result():
    ration_query = ''
    tadpatri_query = ''
    sewingMachine_query = ''
    ration_result = ''
    tadpatri_result = ''
    sewingMachine_result = ''
    msg = ''
    info = '0'
    land_number = ''
    distribution_number = ''
    date_number = ''
    if 'loggedin' in session:
        if request.method == 'POST':

            land_account = request.form['land_account']
            startdate = request.form['startdate']
            enddate = request.form['enddate']
            distribution_option = request.form['disop']

            if land_account == 'All' or land_account == 'all' or land_account == '':
                pass
            else:
                cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                cursor.execute('SELECT * FROM beneficiary_detail WHERE land_accountnumber = %s', (land_account,))
                account = cursor.fetchone()
                if not account:
                    land_an = land_search()
                    msg = "Enter Valid Land Account Number"
                    info = '1'
                    return render_template('report.html', landNumber=land_an, msg=msg, info=info)

            number_list = number_selection(land_account, distribution_option, startdate, enddate)

            if number_list[0] == '0':
                msg = 'Land Account Number IS Not Entered\nDefault Value Is All'
            elif number_list[2] == '1':
                info = 'Select Date Option\nDefault Value Is No Date Selection'

            land_number = number_list[0]
            distribution_number = number_list[1]
            date_number = number_list[2]

            query_list = query_selection(land_number, distribution_number, date_number, land_account, startdate,
                                         enddate)
            if len(query_list[0]) > 1:
                ration_query = query_list[0]

            if len(query_list[1]) > 1:
                tadpatri_query = query_list[1]

            if len(query_list[2]) > 2:
                sewingMachine_query = query_list[2]

            if ration_query:
                cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                cursor.execute(ration_query)
                ration_result = cursor.fetchall()

            if tadpatri_query:
                cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                cursor.execute(tadpatri_query)
                tadpatri_result = cursor.fetchall()

            if sewingMachine_query:
                cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                cursor.execute(sewingMachine_query)
                sewingMachine_result = cursor.fetchall()

            global rendered
            rendered = render_template('report_download.html', ration=ration_result, tadpatri=tadpatri_result,
                                       sewingMachine=sewingMachine_result, )

        return render_template('result.html', ration=ration_result, tadpatri=tadpatri_result,
                               sewingMachine=sewingMachine_result, msg=msg, info=info)
    return redirect(url_for('login'))


@app.route('/download')
def download():
    css = ['static/bootstrap.min.css']
    pdf = pdfkit.from_string(rendered, False, configuration=config, css=css)
    response = make_response(pdf)

    response.headers.set('Content-Disposition', 'inline', filename='output.pdf')
    response.headers.set('Content-Type', 'application/pdf')
    return response



if __name__ == '__main__':
    app.run(debug=True)
