# Import the required libraries
from flask import Flask, render_template, request
from transformers import pipeline

# Create a Flask app
app = Flask(__name__)

# Create a GPT-4 pipeline
gpt4 = pipeline("text-generation", model="Bert")

# Define a route for the home page
@app.route("/")
def home():
    return render_template("home.html")

# Define a route for the generate page
@app.route("/generate", methods=["POST"])
def generate():
    # Get the user input from the form
    user_input = request.form["user_input"]

    # Generate a prompt using GPT-4
    prompt = gpt4(user_input, max_length=50)[0]["generated_text"]

    # Render the generate page with the user input and the prompt
    return render_template("generate.html", user_input=user_input, prompt=prompt)

# Run the app
if __name__ == "__main__":
    app.run(debug=True)
