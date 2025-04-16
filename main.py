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

    if "leaderboard" not in session:
        session["leaderboard"] = []

      

    message = ""
    guesses = session.get("guesses", [])
    score = session.get("score", 20)
    play_sound = False

    
    # Step 1: Ask for name if not provided
    if request.method == "POST" and "name" in request.form:
        session["name"] = request.form["name"]
        return redirect(url_for("play_game"))

    if "name" not in session:
        # Render template asking for name only
        return render_template("index.html", name_required=True)



    # Step 2: Game Logic
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
                message = f"Congratulations 🎉 {session['name']}, you guessed it! The number was {session['secret_number']} in {len(guesses)} guesses. 🔥"
                session["play_sound"] = True
                
                # High Score
                if "high_score" not in session or final_score > session["high_score"]:
                    session["high_score"] = final_score

                 # Leaderboard
                leaderboard = session.get("leaderboard", [])
                leaderboard.append({"name": session["name"], "score": final_score})
                leaderboard = sorted(leaderboard, key=lambda x: x["score"], reverse=True)[:5]
                session["leaderboard"] = leaderboard
                
                # Reset for new game
                session["secret_number"] = random.randint(1, 20)
                session["guesses"] = []
                session["score"] = 20
                session["last_score"] = final_score 


        except ValueError:
            message = "Invalid input. Please enter a number."

        play_sound = session.pop("play_sound", False)
        score_to_display = session.get("last_score", session["score"])

    else:
        play_sound = False
        score_to_display = score


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
        high_score=session.get("high_score", 0),
        leaderboard=session.get("leaderboard", []),
        name=session.get("name")
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=81)
