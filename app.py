from flask import Flask, render_template, request
from textblob import TextBlob

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    text = request.form['text']
    blob = TextBlob(text)
    sentiment = blob.sentiment

    polarity = sentiment.polarity
    subjectivity = sentiment.subjectivity

    if polarity > 0:
        sentiment_label = 'Positive'
        color = 'green'
    elif polarity < 0:
        sentiment_label = 'Negative'
        color = 'red'
    else:
        sentiment_label = 'Neutral'
        color = 'black'

    return render_template('result.html', text=text, polarity=polarity, subjectivity=subjectivity, sentiment_label=sentiment_label, color=color)

if __name__ == '__main__':
    app.run(debug=True)
