import bs4 as bs
import urllib.request
import re
import nltk
import heapq
#from textblob import TextBlob

from pprint import pprint
nltk.download('vader_lexicon')
from nltk.sentiment import SentimentIntensityAnalyzer
sia = SentimentIntensityAnalyzer()



scraped_data = urllib.request.urlopen('https://en.wikipedia.org/wiki/Artificial_intelligence')
article = scraped_data.read()

parsed_article = bs.BeautifulSoup(article,'lxml')

paragraphs = parsed_article.find_all('p')


#text_file = open("amazon_reviews.txt", "r",encoding='utf-8')
 
#read whole file to a string
#data = text_file.read()
article_text = "" #data

#print(article_text)


for p in paragraphs:
    article_text += p.text

# Removing Square Brackets and Extra Spaces
article_text = re.sub(r'\[[0-9]*\]', ' ', article_text)
article_text = re.sub(r'\s+', ' ', article_text)
# Removing special characters and digits
formatted_article_text = re.sub('[^a-zA-Z]', ' ', article_text )
formatted_article_text = re.sub(r'\s+', ' ', formatted_article_text)


sentence_list = nltk.sent_tokenize(article_text)
"""
pos_sentences = []
for sentence in sentence_list:
    
    #if sia.polarity_scores(sentence)['neg']>0:
    pos_sentences.append(sentence)
    print(sentence)
    print('compound=' + str(sia.polarity_scores(sentence)['compound']))
    print('neg=' + str(sia.polarity_scores(sentence)['neg']))
    print('pos=' + str(sia.polarity_scores(sentence)['pos']))
    print('neu=' + str(sia.polarity_scores(sentence)['neu']))
    print('subjectivity=' + str(TextBlob(sentence).sentiment.subjectivity))
    print('polarity=' + str(TextBlob(sentence).sentiment.polarity))

exit()
"""
stopwords = nltk.corpus.stopwords.words('english')

word_frequencies = {}
for word in nltk.word_tokenize(formatted_article_text):
    if word not in stopwords:
        if word not in word_frequencies.keys():
            word_frequencies[word] = 1
        else:
            word_frequencies[word] += 1

maximum_frequncy = max(word_frequencies.values())

for word in word_frequencies.keys():
    word_frequencies[word] = (word_frequencies[word]/maximum_frequncy)

def getSummary(sentence_list):
    sentence_scores = {}
    for sent in sentence_list:
        for word in nltk.word_tokenize(sent.lower()):
            if word in word_frequencies.keys():
                if len(sent.split(' ')) < 30:
                    if sent not in sentence_scores.keys():
                        sentence_scores[sent] = word_frequencies[word]
                    else:
                        sentence_scores[sent] += word_frequencies[word]

    percentage = 0.1
    num_sentences = int(len(sentence_scores) * percentage)
    
    
    summary_sentences = heapq.nlargest(5, sentence_scores, key=sentence_scores.get)

    summary = ' '.join(summary_sentences)
    return summary

def word_count(string):
    # split the string into individual words
    words = string.split()
    # count the number of words
    count = len(words)
    # return the word count
    return int(count*.7)

#print(getSummary(pos_sentences))
x = getSummary(sentence_list)
print(x)
print(word_count(x))

