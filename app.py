from flask import Flask, render_template, request
from textblob import TextBlob
import praw

app = Flask(__name__)

def authenticate_reddit():
    reddit = praw.Reddit(
        client_id='uEpj3XpBBXxwn_Evc_nDHA',
        client_secret='tfaBTItElM2lJwFF1ETDBVEzjUjB3w',
        user_agent='Sentiment Analysis by /u/matinbean'
    )
    return reddit

@app.route('/')
def index():
    return render_template('index.html')

def get_reddit_posts(subreddit, keyword):
    reddit = authenticate_reddit()
    posts = reddit.subreddit(subreddit).search(keyword)
    return posts

def analyze_sentiment(posts):
    sentiment_scores = []
    for post in posts:
        title_blob = TextBlob(post.title)
        title_sentiment = title_blob.sentiment.polarity

        body_blob = TextBlob(post.selftext)
        body_sentiment = body_blob.sentiment.polarity

        average_sentiment = (title_sentiment + body_sentiment) / 2
        sentiment_scores.append(average_sentiment)

    if sentiment_scores:
        average_sentiment = sum(sentiment_scores) / len(sentiment_scores)
    else:
        average_sentiment = 0
    
    return average_sentiment


@app.route('/analyze', methods=['POST'])
def analyze():
    subreddit = request.form['subreddit']
    keyword = request.form['keyword']
    posts = get_reddit_posts(subreddit, keyword)
    average_sentiment = analyze_sentiment(posts)
    
    if average_sentiment > 0:
        sentiment_label = 'Positive'
        color = 'green'
    elif average_sentiment < 0:
        sentiment_label = 'Negative'
        color = 'red'
    else:
        sentiment_label = 'Neutral'
    
    return render_template('result.html', subreddit=subreddit, keyword=keyword, sentiment_label=sentiment_label, average_sentiment=average_sentiment, color=color)

if __name__ == '__main__':
    app.run(debug=True)
