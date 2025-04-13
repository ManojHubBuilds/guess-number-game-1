from flask import Flask, request, render_template, session, redirect, url_for
import random

app = Flask(__name__)
app.secret_key = "guessgame_secret" 


# Initialize secret number
@app.route("/", methods=["GET", "POST"])
def play_game():
    if "secret_number" not in session:
        session["secret_number"] = random.randint(1, 20)
        session["guesses"] = []
      
      

    message = ""
    guesses = session.get("guesses", [])

    if request.method == "POST":
        if request.form.get("action") == "reset":
            session["secret_number"] = random.randint(1, 20)
            session["guesses"] = []
            return redirect(url_for("play_game"))

        try:
            guess = int(request.form["guess"])
            guesses.append(guess)
            session["guesses"] = guesses

            if guess < session["secret_number"]:
                message = "Too low! 🔽 Try a bit higher."
            elif guess > session["secret_number"]:
                message = "Too high! 🔼 Maybe go lower."
            else:
                message = f"Congratulations🎉 You guessed it! The number was {session['secret_number']} in {len(guesses)} guesses. 🔥"
                session["play_sound"] = True
                session["secret_number"] = random.randint(1, 20)
                session["guesses"] = []

        except ValueError:
            message = "Invalid input. Please enter a number."

    play_sound = session.pop("play_sound", False)
    return render_template("index.html",, message=message, guesses=guesses, play_sound=play_sound)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=81)