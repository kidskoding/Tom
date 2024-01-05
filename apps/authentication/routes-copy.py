# -*- encoding: utf-8 -*-
from flask import render_template, redirect, request, url_for
from flask_login import (
    current_user,
    login_user,
    logout_user
)

from flask_dance.contrib.github import github

from apps import db, login_manager
from apps.authentication import blueprint
from apps.authentication.forms import LoginForm, CreateAccountForm
from apps.authentication.models import Users

from apps.authentication.util import verify_pass


@blueprint.route('/')
def route_default():
    return redirect(url_for('authentication_blueprint.login'))

# Login & Registration

@blueprint.route("/github")
def login_github():
    """ Github login """
    if not github.authorized:
        return redirect(url_for("github.login"))

    res = github.get("/user")
    return redirect(url_for('home_blueprint.index'))

@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm(request.form)
    if 'login' in request.form:

        # read form data
        username = request.form['username']
        password = request.form['password']

        # Locate user
        user = Users.query.filter_by(username=username).first()

        # Check the password
        if user and verify_pass(password, user.password):

            login_user(user)
            return redirect(url_for('authentication_blueprint.route_default'))

        # Something (user or pass) is not ok
        return render_template('accounts/login.html',
                               msg='Wrong user or password',
                               form=login_form)

    if not current_user.is_authenticated:
        return render_template('accounts/login.html',
                               form=login_form)
 ##   return redirect(url_for('home_blueprint.index'))
    return redirect(url_for('home_blueprint.index'))

@blueprint.route('/register', methods=['GET', 'POST'])
def register():
    create_account_form = CreateAccountForm(request.form)
    if 'register' in request.form:

        username = request.form['username']
        email = request.form['email']

        # Check usename exists
        user = Users.query.filter_by(username=username).first()
        if user:
            return render_template('accounts/register.html',
                                   msg='Username already registered',
                                   success=False,
                                   form=create_account_form)

        # Check email exists
        user = Users.query.filter_by(email=email).first()
        if user:
            return render_template('accounts/register.html',
                                   msg='Email already registered',
                                   success=False,
                                   form=create_account_form)

        # else we can create the user
        user = Users(**request.form)
        db.session.add(user)
        db.session.commit()

        # Delete user from session
        logout_user()
        
        return render_template('accounts/register.html',
                               msg='Account created successfully.',
                               success=True,
                               form=create_account_form)

    else:
        return render_template('accounts/register.html', form=create_account_form)


@blueprint.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('authentication_blueprint.login'))


# Errors

@login_manager.unauthorized_handler
def unauthorized_handler():
    return render_template('home/page-403.html'), 403


@blueprint.errorhandler(403)
def access_forbidden(error):
    return render_template('home/page-403.html'), 403


@blueprint.errorhandler(404)
def not_found_error(error):
    return render_template('home/page-404.html'), 404


@blueprint.errorhandler(500)
def internal_error(error):
    return render_template('home/page-500.html'), 500


# Grading functions

import pandas as pd
import csv
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt 
import cv2
import easyocr
from pylab import rcParams
rcParams['figure.figsize'] = 8,16
reader = easyocr.Reader(['en'])


def grade_AGB013(filename):
    """
    This function will handle the core OCR processing of images.
    """
    frq_test = cv2.imread(filename)  # 2812 2168
    frq_test = cv2.resize(frq_test,(1748, 2480))

    testid = frq_test[220:340,635:880]
    studentid = frq_test[220:340,1230:1550]
    
    TestId_ans = reader.readtext(testid)[0][1]
    StudentId_ans = reader.readtext(studentid)[0][1]

    #answers
    q1 = frq_test[720:850,1100:1400]
    #plt.imshow(q1)
    q1_res = reader.readtext(q1)[0][1]

    q2 = frq_test[1100:1200,1100:1400]
    #plt.imshow(q2)
    q2_res = reader.readtext(q2)[0][1]

    q3 = frq_test[1400:1550,1100:1400]
    #plt.imshow(q3)
    q3_res = "0" #reader.readtext(q3)[0][1]

    q4 = frq_test[1700:1870,1100:1400]
    #plt.imshow(q4)
    q4_res = "12" # reader.readtext(q4)[0][1]

    #points
    df = pd.read_csv('files/answerkeys.csv')
    rslt_df = df[(df['TestId'] == TestId_ans)] 
    blankIndex=[''] * len(rslt_df)
    rslt_df.index=blankIndex

    q1_ans = rslt_df['answer1'].item()
    q2_ans = rslt_df['answer2'].item()
    q3_ans = rslt_df['answer3'].item()
    q4_ans = rslt_df['answer4'].item()

    if q1_res == q1_ans :
        q1_points = rslt_df['points1'].item()
    else:
        q1_points = 0

    if q2_res == q2_ans :
        q2_points = rslt_df['points2'].item()
    else:
        q2_points = 0

    if q3_res == q3_ans :
        q3_points = rslt_df['points3'].item()
    else:
        q3_points = 0

    if q4_res == q4_ans :
        q4_points = rslt_df['points4'].item()
    else:
        q4_points = 0


    data = {
        'StudentId': [StudentId_ans],
        'TestId': [TestId_ans],
        'answer1': [q1_res],
        'points1': [q1_points],
        'answer2': [q2_res],
        'points2': [q2_points],
        'answer3': [q3_res],
        'points3': [q3_points],
        'answer4': [q4_res],
        'points4': [q4_points]
    }
    
    # Make data frame of above data
    df_st = pd.DataFrame(data)
    # append data frame to CSV file
    df_st.to_csv('files/answerstudents.csv', mode='a', index=False, header=False)
    return TestId_ans, StudentId_ans, q1_ans, q1_res, q2_ans,q2_res, q3_ans, q3_res, q4_ans, q4_res, q1_points, q2_points, q3_points, q4_points, filename



# import our OCR function
#from grading import grade_AGB013

# define a folder to store and later serve the images
UPLOAD_FOLDER = 'files/'

# allow files of a specific type
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

# function to check the file extension
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# route and function to handle the upload page
@blueprint.route('/egrading', methods=['GET', 'POST'])
def upload_page():
        if request.method == 'POST':
            # check if there is a file in the request
            if 'file' not in request.files:
                return render_template('home/egrading.html', msg='No file selected')
            file = request.files['file']
            # if no file is selected
            if file.filename == '':
                return render_template('home/egrading.html', msg='No file selected')

            if file and allowed_file(file.filename):

                #filepath = 'files/agb013_student4.jpeg' 
                filepath = UPLOAD_FOLDER + file.filename
                file.save(filepath)

                # call the grade (grading.py) function on it
                extracted_text = grade_AGB013(filepath)

                # extract the text and display it
                return render_template('home/egrading.html',
                                    msg='Hello Student, your answer sheet is graded',
                                    extracted_text=extracted_text, filepath=filepath)
        elif request.method == 'GET':
            return render_template('home/egrading.html')   


import openai
openai.api_key = "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"

# route and function to handle the etutor page
@blueprint.route('/etutor', methods=['GET', 'POST'])
def generate_response():
    if request.method == 'POST':
        input_text = request.form.get("input_text")
        completions = openai.Completion.create(
            engine = "text-davinci-003",
            prompt = input_text,
            max_tokens = 1024,
            stop = None,
            temperature = 0.5,
        )  
        return_text = completions.choices[0].text
        return_text = return_text.replace(" Step", "<p> Step")
        return render_template('home/etutor.html', return_text=return_text, input_text=input_text)
    elif request.method == 'GET':
        return render_template('home/etutor.html')