from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
sentiment = SentimentIntensityAnalyzer()

def sentiment_analysis(text: str):
    sent = sentiment.polarity_scores(text)
    return {
        "compound": sent['compound'],
        "polarity": {
            "neutral": sent['neu'],
            "positive": sent['pos'],
            "negative": sent['neg']
        }
    }