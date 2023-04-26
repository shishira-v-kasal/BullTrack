from flask import Flask, render_template, jsonify, request,send_file, url_for, flash, redirect
from services.data_service import DataService
from forms import RegistrationForm, LoginForm
import services.bullsdatabase as connection

app = Flask(__name__)
app.config['SECRET_KEY'] = '21c879ef1a404fe8cc172681bb290b9f'

dataService = DataService()

@app.route("/home")
def home():

    return render_template('home.html', data=dataService.getData(), displayWish=connection.get_data('wishlistdata'), \
                            displayInp=connection.get_data('inprocessdata'), \
                            displayApp=connection.get_data('applieddata'), \
                            displayOff=connection.get_data('offerdata'), \
                           upcoming_events=dataService.getUpcomingEvents())

@app.route('/image')
def serve_image():
    return send_file('./static/images/fullusflogo.png', mimetype='image/png')

@app.route('/view', methods=['GET'])
def view():
    return render_template('view_list.html', data=dataService.getAllJobData())

@app.route('/addJob', methods=['POST'])
def addNewJob():
    company_name = request.form['company_name']
    job_role = request.form['job_profile']
    applied_on = request.form['date_applied']
    location = request.form['location']
    salary = request.form['salary']
    job_status = request.form['status']
    dataTable = ""
    if job_status == 'WISHLIST':
        dataTable = "wishlistdata"
    if job_status == 'IN_PROCESS':
        dataTable = "inprocessdata"
    if job_status == 'APPLIED':
        dataTable = "applieddata"
    if job_status == 'OFFER':
        dataTable = "offerdata"
    connection.insert_data(dataTable, company_name, job_role, applied_on, location, salary, job_status)
    return redirect(url_for('home'))

@app.route('/viewWishlist')
def viewWishlist():
    displayData = connection.get_data('wishlistdata')
    return render_template('view_wishlist.html', display=displayData)

@app.route('/viewInprocess')
def viewInprocess():
    displayData = connection.get_data('inprocessdata')
    return render_template('view_wishlist.html', display=displayData)

@app.route('/viewApplied')
def viewApplied():
    displayData = connection.get_data('applieddata')
    return render_template('view_wishlist.html', display=displayData)

@app.route('/viewOffers')
def viewOffers():
    displayData = connection.get_data('offerdata')
    return render_template('view_wishlist.html', display=displayData)

@app.route('/viewEvents')
def viewEvents():
    displayData = connection.get_data('eventsdata')
    return render_template('view_wishlist.html', display=displayData)

@app.route('/deleteJob', methods=['POST'])
def delete():
    job_data = request.get_json()
    dataService.deleteJob(job_id=job_data['job_id'])
    print('delete called')
    response = {"status": "Success"}
    return jsonify(response)

@app.route('/updateJobStatus', methods=['POST'])
def updateJobStatus():
    job_data = request.get_json()
    print(job_data)
    job_id = job_data['job_id']
    job_status = job_data['job_status']
    dataService.updateJobStatus(job_id, newStatus=job_status)
    response = {"status": job_status}
    return jsonify(response)

@app.route("/")
@app.route("/index")
def index():
    return render_template('index.html')


@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash('You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)

if __name__ == '__main__':
    app.run(debug=True, port=7778)