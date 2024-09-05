from flask import Flask, render_template, request
import speech_recognition as sr
import pyttsx3
from textblob import TextBlob

app = Flask(__name__)

def speak(text):
    print(text)
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def analyze_sentiment(text):
    blob = TextBlob(text)
    sentiment = blob.sentiment.polarity
    if sentiment > 0:
        return "Positive"
    elif sentiment == 0:
        return "Neutral"
    else:
        return "Negative"

@app.route("/", methods=["GET", "POST"])
def index():
    sentiment = None
    if request.method == "POST":
        sentence = request.form["sentence"]
        recognizer = sr.Recognizer()
        try:
            speak("You said: " + sentence)
            sentiment = analyze_sentiment(sentence)
            speak("The sentiment of the sentence is: " + sentiment)
        except sr.UnknownValueError:
            speak("Sorry, could not understand audio.")
        except sr.RequestError as e:
            speak(f"Could not request results; {e}")

    return render_template("index.html", sentiment=sentiment)

if __name__ == "__main__":
    app.run(debug=True)
