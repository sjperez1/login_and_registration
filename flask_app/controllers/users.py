from flask import render_template, redirect, request, session, flash
from flask_app import app
from flask_app.models.user import User
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route("/")
def display_login_registration():
    if User.validate_user_session() == True:
        return redirect("/success")
    else:
        return render_template("login_registration.html")

@app.route("/register", methods = ['POST'])
def register_user():
    if User.validate_user_registration(request.form) == False:
        return redirect("/")
    else:
        # The following is saying if there is no matching email stored in the database, then create it. The else statement will say that there already is one and you need to use a different one.
        if User.get_one_user_email({"email" : request.form['email']}) == None:
            data = {
                "first_name" : request.form['first_name'],
                "last_name" : request.form['last_name'],
                "email" : request.form['email'],
                "password" : bcrypt.generate_password_hash(request.form['password']),
                "confirm_password" : request.form['confirm_password']
            }
            user_id = User.create_user(data)
            # result is one instance of a user. Look at the function to understand this better.
            session['first_name'] =  request.form['first_name']
            session['last_name'] = request.form['last_name']
            session['email'] = request.form['email']
            # Needed to add the session id part here so that def get_user_by_id can get the user id
            session['id'] = user_id
            return redirect("/success")
        else:
            flash("This email is already in use. Use a different email to register or log in.", "error_email_registration")
            return redirect("/")

@app.route("/login", methods = ['POST'])
def login_user():
    user_login = User.get_one_user_email(request.form)
    if user_login == None:
        flash("This email does not belong to an existing user. Please try again.", "error_login_user")
        return redirect("/")
    if not bcrypt.check_password_hash(user_login.password, request.form['password']):
        flash("This password does not belong to an existing user. Please try again.", "error_login_user")
        return redirect("/")
    else:
        # user_login is one instance of a user that has an email matching what they typed in, as seen with the User.get_one_user_email() function.
        session['first_name'] = user_login.first_name
        session['last_name'] = user_login.last_name
        session['email'] = user_login.email
        # Needed to add the session id part here so that def get_user_by_id can get the user id
        session['id'] = user_login.id
        return redirect("/success")


@app.route("/success")
def display_dashboard():
    if User.validate_user_session() == False:
        return redirect ("/")
    else:
        return render_template("success.html")
    

@app.route("/logout", methods = ['POST'])
def logout():
    session.clear()
    return redirect ("/")