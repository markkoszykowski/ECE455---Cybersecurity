import random

from .checks import check_existence, check_bounds, get_radial_distance, get_midpoint
from .models import users_database, User, Passwords, Attempts
from flask_login import login_user, logout_user, current_user
from flask import Blueprint, jsonify, send_file, request
from werkzeug.utils import secure_filename
from random import sample
import itertools
import uuid
import os

IMAGES_DIR = "images"
PROJECT_DIR = os.path.dirname(os.path.realpath(__file__))

main = Blueprint("main", __name__)

MINIMUM_POINTS = 6
RADIAL_DISTANCES = [3, 5, 10, 15, 20]


@main.route("/ping", methods=["GET"])
def ping():
    return jsonify("OK"), 200


@main.route("/", methods=["GET"])
def index():
    if current_user.is_authenticated:
        return jsonify(F"Hello {current_user.username}, Thanks for helping our study!"), 200
    else:
        return jsonify("Please try our ECE455 - Cybersecurity Final Project!"), 200


@main.route("/get_image/<image>", methods=["GET"])
def get_image(image):
    file_path = None
    try:
        file_path = check_existence(secure_filename(image))
    except OSError:
        pass
    return (send_file(file_path), 200) if file_path else (jsonify("Requested image does not exist"), 404)


@main.route("/get_password_images", methods=["GET"])
def get_password_images():
    images = os.listdir(os.path.join(PROJECT_DIR, IMAGES_DIR))
    random.shuffle(images)
    return jsonify(images), 200


@main.route("/getR", methods=["GET"])
def get_radial_distances():
    return jsonify({"R": sorted(sample(RADIAL_DISTANCES, 2), reverse=True)}), 200


"""

    Expected signup password format: 
        "<image_name> <tuple_of_coordinates>, <image_name> <tuple_of_coordinates>, ...;
        <image_name> <tuple_of_coordinates>, <image_name> <tuple_of_coordinates>, ..." 

    Signup password should be one continuous string. Each attempt (should be 2) should be semi-colon delimited. Within
    each attempt, each sequence of password 'points' should be the name of the image file, followed by a tuple of x, y
    coordinates delimited with a comma. There should be N signup strings, one for each of the R being tested.

    Total signup post request:

    {
        "username": <username>,
        "radial_distance": <radial_distance_user_wants_to_use>,
        "password": <expected_signup_password_string>
    }


"""
@main.route("/signup", methods=["POST"])
def signup():
    body = request.json
    if body is None:
        return jsonify("No request data"), 400
    username = body.get("username", None)
    radial_distance = body.get("radial_distance", None)
    password = body.get("password", None)

    if username is None or radial_distance is None or password is None:
        return jsonify("Request is missing parameters"), 400

    # Make sure R is an integer and one that the backend deems valid
    try:
        radial_distance = int(radial_distance)
    except ValueError:
        return jsonify("Provided radial distance not valid"), 400

    if radial_distance not in RADIAL_DISTANCES:
        return jsonify("Invalid radial distance requested"), 400

    # Check if user has a password
    user = User.query.filter_by(username=username).first()
    if user:
        radial_distance_password = Passwords.query.filter_by(id=user.id, r=radial_distance).first()
        if radial_distance_password:
            return jsonify("User already has a password for this radial distance, pick a new username"), 403

    if password == "":
        return jsonify(F"Please enter a password at least {MINIMUM_POINTS} points long"), 400

    # Password formatting
    password = password.split(";")
    if any(subpassword == "" for subpassword in password):
        return jsonify(F"Please enter a password at least {MINIMUM_POINTS} points long"), 400

    if len(password) == 1:
        return jsonify(F"Please enter a password at least {MINIMUM_POINTS} points long"), 400
    elif len(password) != 2:
        return jsonify("Incorrect format"), 400

    for entry, string in enumerate(password):
        points = string.split(",")
        if len(points) < MINIMUM_POINTS:
            return jsonify(F"Not enough points used, need {MINIMUM_POINTS} points"), 400

        password[entry] = [tuple(point.split()) for point in points]
        if not all(len(point) == 3 for point in password[entry]):
            return jsonify("Incorrect format"), 400

        try:
            password[entry] = [(check_existence(secure_filename(point[0])), int(point[1]), int(point[2])) for point in
                               password[entry]]
            [check_bounds(*point) for point in password[entry]]
        except ValueError:
            return jsonify("Incorrect format"), 400
        except OSError:
            return jsonify("Image does not exist"), 400
        except IndexError:
            return jsonify("Image coordinates out of bounds"), 400

    if not user:
        current_ids = users_database.session.query(User.id).all()
        new_id = uuid.uuid4().hex
        while new_id in current_ids:
            new_id = uuid.uuid4().hex

        user = User(id=new_id, username=username)
        users_database.session.add(user)

    radial_distance_attempts = Attempts.query.filter_by(id=user.id, r=radial_distance).first()
    if radial_distance_attempts:
        radial_distance_attempts.attempts += 1
    else:
        radial_distance_attempts = Attempts(id=user.id, r=radial_distance, attempts=1, successes=0)
        users_database.session.add(radial_distance_attempts)

    midpoint_password = ""
    first = True

    # Compare 2 attempts
    for entry1, entry2 in itertools.zip_longest(*password, fillvalue=("", -1, -1)):
        if not first:
            midpoint_password += ", "
        first = False

        if entry1[0] != entry2[0]:
            users_database.session.commit()
            return jsonify("Password attempts are not the same"), 406

        if get_radial_distance((entry1[1], entry1[2]), (entry2[1], entry2[2])) > radial_distance:
            users_database.session.commit()
            return jsonify("Password attempts are not the same"), 406

        mid_x, mid_y = get_midpoint((entry1[1], entry1[2]), (entry2[1], entry2[2]))
        midpoint_password += F"{os.path.basename(entry1[0])} {mid_x} {mid_y}"

    radial_distance_attempts.successes += 1
    radial_distance_password = Passwords(id=user.id, r=radial_distance, password=midpoint_password)
    users_database.session.add(radial_distance_password)
    users_database.session.commit()

    login_user(user, remember=True)

    return jsonify("Success!"), 201


"""

    Expected login password format: 
        "<image_name> <tuple_of_coordinates>, <image_name> <tuple_of_coordinates>, ..." 

    Login password should be one continuous string. Each sequence of password 'points' should be the name of the image
    file, followed by a tuple of x, y coordinates delimited with a comma. Expecting one password string for a specified
    radial distance that the user would like to use/test for login.

    Total signup post request:

    {
        "username": <username>,
        "radial_distance": <radial_distance_user_wants_to_use>,
        "password": <expected_signup_password_string>,
    }


"""
@main.route("/login", methods=["POST"])
def login():
    body = request.json
    if body is None:
        return jsonify("No request data"), 400
    username = body.get("username", None)
    radial_distance = body.get("radial_distance", None)
    password = body.get("password", None)

    if username is None or radial_distance is None or password is None:
        return jsonify("Request is missing parameters"), 400

    # Make sure R is an integer and one that the backend deems valid
    try:
        radial_distance = int(radial_distance)
    except ValueError:
        return jsonify("Provided radial distance not valid"), 400

    if radial_distance not in RADIAL_DISTANCES:
        return jsonify("Invalid radial distance requested"), 400

    # Check if user has a password
    user = User.query.filter_by(username=username).first()
    radial_distance_password = None
    if user:
        radial_distance_password = Passwords.query.filter_by(id=user.id, r=radial_distance).first()
        if not radial_distance_password:
            return jsonify("User does not have password setup for provided radial distance"), 400
    else:
        return jsonify("User has not set up an account"), 400

    if password == "":
        return jsonify("Please enter a password at least 6 points long"), 400

    # Password formatting
    password = password.split(",")

    password = [tuple(point.split()) for point in password]
    if not all(len(point) == 3 for point in password):
        return jsonify("Incorrect format"), 400

    try:
        password = [(check_existence(secure_filename(point[0])), int(point[1]), int(point[2])) for point in password]
        [check_bounds(*point) for point in password]
    except ValueError:
        return jsonify("Incorrect format"), 400
    except OSError:
        return jsonify("Image does not exist"), 400
    except IndexError:
        return jsonify("Image coordinates out of bounds"), 400

    radial_distance_attempts = Attempts.query.filter_by(id=user.id, r=radial_distance).first()
    radial_distance_attempts.attempts += 1

    actual_password = radial_distance_password.password.split(",")
    actual_password = [tuple(point.split()) for point in actual_password]

    for provided_point, password_point in itertools.zip_longest(password, actual_password, fillvalue=("", -1, -1)):
        if os.path.basename(provided_point[0]) != password_point[0]:
            users_database.session.commit()
            return jsonify("Incorrect Password"), 401

        if get_radial_distance((provided_point[1], provided_point[2]),
                               (int(password_point[1]), int(password_point[2]))) > radial_distance:
            users_database.session.commit()
            return jsonify("Incorrect Password"), 401

    radial_distance_attempts.successes += 1
    users_database.session.commit()

    login_user(user, remember=True)

    return jsonify(), 200


@main.route("/logout", methods=["GET"])
def logout():
    if current_user.is_authenticated:
        logout_user()
        return jsonify("Successfully logged out"), 200
    else:
        return jsonify("User not logged in"), 401
