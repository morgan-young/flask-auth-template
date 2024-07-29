import json
import logging
import os
import uuid
from datetime import datetime, timedelta

from flask import Flask, jsonify, redirect, render_template, request, url_for
from flask_cors import CORS
from flask_login import (
    LoginManager,
    UserMixin,
    current_user,
    login_required,
    login_user,
    logout_user,
)
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash

# Initialize the Flask app
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# Set the environment based on FLASK_ENV
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")
app.config["SESSION_TYPE"] = "filesystem"

# Initialise the database connection
# Set the DATABASE_URI to reference the SQLite database
DATABASE_URI = os.environ.get("DATABASE_URI", "sqlite:///database.db")
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

# Set up logging
logging.basicConfig(level=logging.INFO)

# Initialize the LoginManager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


class User(UserMixin, db.Model):
    __tablename__ = "users"
    userId = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))
    email = db.Column(db.String, unique=True, nullable=False)
    passwordHash = db.Column(db.String, nullable=False)

    def check_password(self, password):
        return check_password_hash(self.passwordHash, password)

    def get_id(self):
        return self.userId


@login_manager.user_loader
def load_user(user_id):
    try:
        user = User.query.filter_by(userId=user_id).first()
        if user:
            return user
    except Exception as e:
        logging.error(f"Error loading user: {e}")
    return None


@app.route("/")
@login_required
def index():
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if request.is_json:
            data = request.get_json()
            email = data.get("email")
            password = data.get("password")
        else:
            email = request.form["email"]
            password = request.form["password"]

        try:
            user = User.query.filter_by(email=email).first()
            if user and user.check_password(password):
                login_user(user)
                next_page = request.args.get("next")
                return jsonify(
                    {"success": True, "redirectUrl": next_page or url_for("index")}
                )
            return jsonify({"error": "Invalid email or password"}), 401
        except Exception as e:
            logging.error(f"Error logging in user: {e}")
            return jsonify({"error": "Error logging in user"}), 500

    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        try:
            if request.is_json:
                data = request.get_json()
                email = data.get("email")
                password = data.get("password")
            else:
                email = request.form["email"]
                password = request.form["password"]

            password_hash = generate_password_hash(password)
            user_id = str(uuid.uuid4())

            # Check for an existing user by email
            existing_user = User.query.filter_by(email=email).first()

            if existing_user:
                logging.error(f"Account already exists for this email: {email}")
                return jsonify({"error": "Account already exists for this email"}), 409

            # Create a new user
            new_user = User(userId=user_id, email=email, passwordHash=password_hash)
            db.session.add(new_user)
            db.session.commit()

            return jsonify({"success": True, "redirectUrl": url_for("login")})
        except Exception as e:
            logging.error(f"Error registering user: {e}")
            return jsonify({"error": "Error registering user"}), 500

    return render_template("register.html")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))


# Server for WSGI
def handler(event, context):
    return app(event, context)


if __name__ == "__main__":
    app.run()
