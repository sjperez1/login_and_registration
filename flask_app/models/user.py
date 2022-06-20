from flask_app import DATABASE
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash, session
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def get_one_user_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL(DATABASE).query_db(query, data)

        if len(result) > 0:
            return cls(result[0])
        else:
            return None
    @classmethod
    def create_user(cls, data):
        query = "INSERT INTO users(first_name, last_name, email, password) VALUES(%(first_name)s, %(last_name)s, %(email)s, %(password)s);"
        return connectToMySQL(DATABASE).query_db(query, data)

    @staticmethod
    def validate_user_registration(data):
        isValid = True
        if data['first_name'] == "":
            flash("Your first name is required for registration.", "error_first_registration")
            isValid = False
        if len(data['first_name']) < 2:
            flash("Your first name must be at least 2 characters long for registration.", "error_first_registration")
            isValid = False
        if data['last_name'] == "":
            flash("Your last name is required for registration.", "error_last_registration")
            isValid = False
        if len(data['last_name']) < 2:
            flash("Your last name must be at least 2 characters long for registration.", "error_last_registration")
            isValid = False
        if data['email'] == "":
            flash("Your email is required for registration.", "error_email_registration")
            isValid = False
        if not EMAIL_REGEX.match(data['email']):
            flash("You must provide a valid email for registration.", "error_email_registration")
            isValid = False
        if data['password'] == "":
            flash("You must provide a password.", "error_password_registration")
            isValid = False
        if len(data['password']) < 8:
            flash("Your password must be at least 8 characters long.", "error_password_registration")
            isValid = False
        if data["confirm_password"] != data['password']:
            flash("Your password and password confirmation must match.", "error_confirm_password_registration")
            isValid = False
        return isValid

    @staticmethod
    def validate_user_session():
        if "id" not in session:
            flash("You must login to view this page.", "error_must_login")
            return False
        else:
            return True