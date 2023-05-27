from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension

from surveys import *

app = Flask(__name__)

app.config['SECRET_KEY'] = "!1IcedCoffee"
debug = DebugToolbarExtension(app) 

button_content = 'start'

@app.route('/')
def home():
    session['responses'] = []
    surv_title = satisfaction_survey.title
    surv_instructions = satisfaction_survey.instructions
    return render_template('base.html', title = surv_title, instructions = surv_instructions, current = 0, button = button_content, method = "get")

@app.route('/<int:current>', methods=["GET", "POST"])
def question(current):
    if len(request.form) == 0 and current > 0:
        flash('must submit questions in order!')
        return redirect('/')
    if len(request.form) > 0:
        answers = session['responses']
        answers.append(request.form["answer"])
        session['responses'] = answers
    if current <= 3:
        frm_method = "post"
        next = current + 1
        button_content = 'next'
        return render_template('question.html', question = satisfaction_survey.questions[current].question, choices = satisfaction_survey.questions[current].choices, button = button_content, current = next, method = frm_method, number = next)
    return render_template('thanks.html', button = "return to start", current = '/', answers = session['responses'])