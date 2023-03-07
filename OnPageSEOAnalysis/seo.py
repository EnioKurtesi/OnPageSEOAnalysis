from types import NoneType
import requests
from bs4 import BeautifulSoup
import nltk
from nltk.tokenize import word_tokenize
from nltk.util import ngrams
nltk.download('stopwords')
nltk.download('punkt')
import streamlit as sl


sl.title('ON PAGE SEO ANALYZER')

url = sl.text_input('Enter URL')
number = sl.number_input(label="Enter the number of keywords,bigrams and trigrams",step=1)
number = int(number)
if len(url) == 0:
    url = "https://yoast.com/copywriting-tips-from-experts-to-experts/"

if number == 0:
    number = 10
def seo_analysis(url):
# Save the good and the warnings in lists
    good = []
    bad = []
# Send a GET request to the website
    response = requests.get(url)
# Check the response status code
    if response.status_code != 200:
        sl.error("Error: Unable to access the website.")
        return

# Parse the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')

# Extract the title and description
    try:
        title = soup.find('title').get_text()
    except TypeError as te:
        bad.append('No title found!')    
    try:
        description = soup.find('meta', attrs={'name': 'description'})['content']
    except TypeError as te:
        bad.append('No meta description is found!')    

# Check if the title and description exist
    if title:
        good.append("Title Exists! Great!")
        good.append(title)
        good.append(f"Length of title is {len(title)}")
        if(len(title) > 60):
            good.append('Title is long. Google recommends 55-60 characters')
        elif(len(title) >= 55 and len(title) <= 60 ):
            good.append('Length of title is optimal! Congrats!')
        elif(len(title) < 55):
            good.append('Title tag is short. There is room for improvement! Google recommends 55-60 characters!')    
    else:
        bad.append("Title does not exist! Add a Title")

    try:
        if description:
            good.append("Description Exists! Great!")
            good.append(description)
            good.append(f"Length of meta-description is {len(description)}")
            if(len(description) > 160):
                good.append('Meta description is long. Please, optimize!')
            elif(len(description)>=150 and len(description) <=160):
                good.append('Meta description length is optimal! Congrats!')
            elif(len(description) < 150):
                good.append('Meta description is short. There is room for improvement! Google recommends 150-160 characters')        
        else:
            bad.append("Description does not exist! Add a Meta Description")
    except UnboundLocalError as ule:
        print(ule)    

# Grab the Headings
    hs = ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']
    h_tags = []
    for h in soup.find_all(hs):
        good.append(f"{h.name}-->{h.text.strip()}")
        h_tags.append(h.name)

    if 'h1' not in h_tags:
        bad.append("No H1 found!")

# Extract the images without Alt
    for i in soup.find_all('img', alt=''):
        bad.append(f"No Alt: {i}") 

# Extract keywords
# Grab the text from the body of html
    bod = soup.find('body').text

# Extract all the words in the body and lowercase them in a list
    words = [i.lower() for i in word_tokenize(bod)]

    bigrams = ngrams(words,2)
    freq_bigrams = nltk.FreqDist(bigrams)
    most_common_bigrams= freq_bigrams.most_common(number)
    trigrams = ngrams(words,3)
    freq_trigrams = nltk.FreqDist(trigrams)
    most_common_trigrams= freq_trigrams.most_common(number)


# Grab a list of English stopwords
    sw = nltk.corpus.stopwords.words('english')
    new_words = []

# Put the tokens which are not stopwords and are actual words (no punctuation) in a new list
    for i in words:
      if i not in sw and i.isalpha():
        new_words.append(i)

# Extract the fequency of the words and get the 10 most common ones
    freq = nltk.FreqDist(new_words)
    keywords= freq.most_common(number)

# Print the results

    tab1,tab2,tab3,tab4,tab5 = sl.tabs(['Keywords', 'Bigrams', 'Trigrams','Good', 'Bad'])

    with tab1:
        for i in keywords:
            sl.text(i)
    with tab2:
        for i in most_common_bigrams:
            sl.text(i)
    with tab3:
        for i in most_common_trigrams:
            sl.text(i)
    with tab4:
        for i in good:
            sl.text(i)
    with tab5:
        for i in bad:
            sl.text(i)                
    print("Keywords: ", keywords)
    print("The Good: ", good)
    print("The Bad: ", bad)
    
# Call the function to see the results
seo_analysis(url)