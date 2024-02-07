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

    # Add a prefix to the user input to specify the task and domain
    prefix = "Word: {word}. Creative writing prompt: {prompt}\n"
    prefix += "Word: dog. Creative writing prompt: Write a story from the point of view of a dog.\n"
    prefix += "Word: love. Creative writing prompt: Write a poem that rhymes with the word love.\n"
    prefix += "Word: mystery. Creative writing prompt: Write a dialogue between a detective and a suspect.\n"

    # Encode the prefix and the user input as input ids
    input_ids = tokenizer.encode(
        prefix.format(word=user_input, prompt=""), return_tensors="pt"
    )

    # Generate 5 prompts with different sampling methods
    prompts = []
    for i in range(5):
        # Use a different seed for each prompt
        np.random.seed(i)
        # Use a different sampling method for each prompt
        if i == 0:
            # Use top-k sampling with k=50
            prompt = model.generate(input_ids, max_length=50, top_k=50)[0]
        elif i == 1:
            # Use top-p sampling with p=0.9
            prompt = model.generate(input_ids, max_length=50, top_p=0.9)[0]
        elif i == 2:
            # Use beam search with beam size=5
            prompt = model.generate(input_ids, max_length=50, num_beams=5)[0]
        elif i == 3:
            # Use temperature sampling with temperature=0.7
            prompt = model.generate(input_ids, max_length=50, temperature=0.7)[0]
        else:
            # Use random sampling
            prompt = model.generate(input_ids, max_length=50, do_sample=True)[0]
        # Decode the prompt and remove the prefix and the user input
        prompt = tokenizer.decode(prompt, skip_special_tokens=True).replace(
            prefix.format(word=user_input, prompt=""), ""
        )
        # Append the prompt to the list of prompts
        prompts.append(prompt)

    # Render the generate page with the prompts
    return render_template("generate.html", prompts=prompts)

# Define a route for the rate page
@app.route("/rate", methods=["POST"])
def rate():
    # Get the user input, the prompts, and the rating from the form
    user_input = request.form["user_input"]
    prompts = request.form["prompts"]
    rating = request.form["rating"]
    # Save the user input, the prompts, and the rating to a file or a database
    with open("feedback.txt", "a") as f:
        f.write(user_input + "\n")
        f.write(prompts + "\n")
        f.write(rating + "\n")
    # Use the rating to update or improve the model or the app
    # Render the rate page with a thank you message
    return render_template("rate.html")

# Run the app
if __name__ == "__main__":
    app.run(debug=True)
