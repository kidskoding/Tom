import openai
import os
from flask import Flask, redirect, render_template, request, url_for

openai.api_key = "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"

app = Flask(__name__)

# route and function to handle the etutor page
@app.route('/etutor', methods=['GET', 'POST'])

def submit_chat1():
    #if request.method == "POST":
        input_text = "who is elon musk"
        response = openai.Completion.create(
            model="text-davinci-002",
            prompt=input_text, #generate_prompt(input_text),
            temperature=0.6,
        )
        print(response)
        result = response.choices[0].text
        print(result)
        result = request.args.get("result")
        print(result)
        #return render_template('home/etutor.html',
        #                            msg='Hello Student, your answer sheet is graded',
         #                           return_text=result)
    #elif request.method == 'GET':
    #    return render_template('home/etutor.html') 

submit_chat1()        

def generate_prompt(input_text):
    return """Suggest three names for an animal that is a superhero.
Animal: Cat
Names: Captain Sharpclaw, Agent Fluffball, The Incredible Feline
Animal: Dog
Names: Ruff the Protector, Wonder Canine, Sir Barks-a-Lot
Animal: {}
Names:""".format(
        input_text.capitalize()
    )