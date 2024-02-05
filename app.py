# Import the required libraries
from flask import Flask, render_template, request
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
import numpy as np

# Create a Flask app
app = Flask(__name__)

model = AutoModelForCausalLM.from_pretrained("bigscience/bloom-560m")
tokenizer = AutoTokenizer.from_pretrained("bigscience/bloom-560m")

# Define a route for the home page
@app.route("/")
def home():
    return render_template("home.html")

# Define a route for the generate page
@app.route("/generate", methods=["POST"])
def generate():
    # Get the user input from the form
    user_input = request.form["user_input"]
    prompt = model.generate(tokenizer.encode(user_input, return_tensors="pt"), max_length=50, top_k=50)[0]
    prompt = tokenizer.decode(prompt, skip_special_tokens=True)

    # Render the generate page with the user input and the prompt
    return render_template("generate.html", user_input=user_input, prompt=prompt)

# Run the app
if __name__ == "__main__":
    app.run(debug=True)
