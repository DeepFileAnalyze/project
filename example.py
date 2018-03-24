import google.cloud.language

    # Create a Language client.
language_client = google.cloud.language.LanguageServiceClient()

    # TODO (Developer): Replace this with the text you want to analyze.
text = 'Google, headquartered in Mountain View, unveiled the new Android phone at the Consumer Electronic Show.  Sundar Pichai said in his keynote that users love their new Android phones.'
document = google.cloud.language.types.Document(content=text,type=google.cloud.language.enums.Document.Type.PLAIN_TEXT)

    # Use Language to detect the sentiment of the text.
response = language_client.analyze_sentiment(document=document)
sentiment = response.document_sentiment

print('Text: {}'.format(text))
print('Sentiment: Score: {}, Magnitude: {}'.format(sentiment.score, sentiment.magnitude))

