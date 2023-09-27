from flask import Blueprint, render_template, request, redirect, url_for, Response, flash,session
from app.models import *
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint('auth', __name__, template_folder='templates/auth')

@auth.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':

        if request.form.get('form_type') == 'register':
            # Handle registration form submission
            fname = request.form.get('fname')
            lname = request.form.get('lname')
            address = request.form.get('address')
            city = request.form.get('city')
            state = request.form.get('state')
            zip_code = request.form.get('zip')
            email = request.form.get('email')
            username = request.form.get('username')
            password = request.form.get('password')

            hashed_password = generate_password_hash(password, method='sha256')

            # Check if user already exists
            user = User.query.filter(or_(User.email == email, User.username == username)).first()


            if user:
                if user.email == email and user.username == username:
                    message = 'Email address and username already exist!'
                elif user.email == email:
                    message = 'Email address already exists!'
                elif user.username == username:
                    message = 'Username already exists!'
                else:
                    message = "An error occured while processing your request. Please try again later."
                return render_template('auth/login.html', message = message, user=user)

            new_user = User(
                first_name=fname,
                last_name=lname,
                address=address,
                city=city,
                state=state,
                zip_code=zip_code,
                email=email,
                username=username,
                password=hashed_password
            )

            db.session.add(new_user)
            db.session.commit()

            flash('Registration successful')
            return redirect(url_for('auth.index'))
        
        elif request.form.get('form_type') == 'login':
            email = request.form.get('email')
            password = request.form.get('password')

            if email and password:
                user = User.query.filter_by(email=email).first()
                if user and check_password_hash(user.password, password):
                    session['logged_in'] = True
                    session['user_id'] = user.user_id
                    return redirect(url_for('index'))
                else:
                    return render_template('auth/login.html', message='Invalid email or password', session=session.get('logged_in'))
    return render_template('auth/login.html')


@auth.route('/logout')
def logout():
    session['logged_in'] = False
    session['user_id'] = None
    return redirect(url_for('index'))
