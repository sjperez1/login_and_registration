from flask import Flask
app = Flask(__name__)

app.secret_key = "shhh"

# The following allows easy changing of database name throughout our files
DATABASE = 'login_and_registration_schema'