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
        session["score"] = 20
      

    message = ""
    guesses = session.get("guesses", [])
    score = session.get("score", 20)


    if request.method == "POST":
        if request.form.get("action") == "reset":
            session["secret_number"] = random.randint(1, 20)
            session["guesses"] = []
            session["score"] = 20
            return redirect(url_for("play_game"))

        try:
            guess = int(request.form["guess"])
            guesses.append(guess)
            session["guesses"] = guesses

            if guess < session["secret_number"]:
                message = "Too low! 🔽 Try a bit higher."
                session["score"] -= 1
            elif guess > session["secret_number"]:
                message = "Too high! 🔼 Maybe go lower."
                session["score"] -= 1
            else:
                final_score = session["score"]
                message = f"Congratulations🎉 You guessed it! The number was {session['secret_number']} in {len(guesses)} guesses. 🔥"
                session["play_sound"] = True

                if "high_score" not in session or final_score > session["high_score"]:
                    session["high_score"] = final_score

                session["secret_number"] = random.randint(1, 20)
                session["guesses"] = []
                session["score"] = 20
                session["last_score"] = final_score 


        except ValueError:
            message = "Invalid input. Please enter a number."

        play_sound = session.pop("play_sound", False)

    
        score_to_display = session.get("last_score", session["score"])

        # Emoji logic
        emoji = ""
        if score_to_display >= 18:
            emoji = "🔥"
        elif score_to_display >= 14:
            emoji = "👍"
        elif score_to_display >= 8:
            emoji = "🙂"
        else:
            emoji = "😅"

        return render_template("index.html",
            message=message,
            guesses=guesses,
            play_sound=play_sound,
            score=score_to_display,
            emoji=emoji,
            high_score=session.get("high_score", 0)
        )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=81)