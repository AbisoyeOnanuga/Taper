# Import the required libraries
from flask import Flask, render_template, request
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
import numpy as np
import random

# Create a Flask app
app = Flask(__name__)

model = AutoModelForCausalLM.from_pretrained("bigscience/bloom-560m")
tokenizer = AutoTokenizer.from_pretrained("bigscience/bloom-560m")

# Define a route for the home page
@app.route("/")
def home():
    return render_template("home.html")

# Define the list of possible prompt types
prompt_types = [
    "Write a story about {seed}.",
    "How would you describe {seed} in three words?",
    "What if {seed} was real?",
    "Use {seed} as the first line of a poem.",
    "Create a dialogue between two characters who disagree about {seed}.",
]

# Define the list of possible sampling methods
sampling_methods = [
    {"top_k": 50},
    {"top_p": 0.9},
    {"num_beams": 5},
    {"temperature": 0.7},
    {"do_sample": True},
]

# Define the common parameters for generating prompts
max_length = 50
repetition_penalty = 1.2
length_penalty = 0.8
no_repeat_ngram_size = 3

# Define a function to generate a prompt given a seed and a sampling method
def generate_prompt(seed, sampling_method):
    # Choose a random prompt type
    prompt_type = random.choice(prompt_types)
    user_input = request.form["user_input"]
    prefix = "Seed: {seed}. Creative writing prompt: {prompt}\n"
    # Use the user input as the seed for the first prompt
    if seed == user_input:
        prefix += "Seed: a haunted house. Creative writing prompt: Write a story about a haunted house.\n"

    # Encode the prefix and the seed as input ids
    input_ids = tokenizer.encode(
        prefix.format(seed=seed, prompt=""), return_tensors="pt"
    )
    # Generate a prompt with the sampling method
    prompt = model.generate(
        input_ids,
        max_length=max_length,
        repetition_penalty=repetition_penalty,
        length_penalty=length_penalty,
        no_repeat_ngram_size=no_repeat_ngram_size,
        **sampling_method,
    )[0]
    # Decode the prompt and remove the prefix and the seed
    prompt = tokenizer.decode(prompt, skip_special_tokens=True).replace(
        prefix.format(seed=seed, prompt=""), ""
    )
    # Return the prompt
    return prompt

# Define a function to render the generate page given a list of prompts
def render_generate_page(prompts):
    # Render the generate page with the prompts
    return render_template("generate.html", prompts=prompts)

# Define a list of possible seeds
seeds = [
    "a haunted house",
    "love",
    "what if",
    "a rainy day",
    "chocolate and cheese",
]

# Define a route for the generate page
@app.route("/generate", methods=["POST"])
def generate():
    # Get the user input from the form
    user_input = request.form["user_input"]
    # Generate 5 prompts with different sampling methods
    prompts = []
    for i in range(5):
        # Use a different seed for each prompt
        if i == 0:
            # Use the user input as the seed for the first prompt
            seed = user_input
        else:
            # Use a random seed for the other prompts
            seed = random.choice(seeds)
        # Use a different sampling method for each prompt
        sampling_method = sampling_methods[i]
        # Generate a prompt with the user input and the sampling method
        prompt = generate_prompt(user_input, sampling_method)
        # Append the prompt to the list of prompts
        prompts.append(prompt)
    # Render the generate page with the prompts
    return render_generate_page(prompts)

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
