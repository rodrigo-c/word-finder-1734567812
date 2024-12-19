from flask import Flask, render_template, request
import urllib.request
import os

app = Flask(__name__)

# Download and cache the word list
WORD_LIST_URL = "https://raw.githubusercontent.com/dwyl/english-words/master/words_alpha.txt"
WORD_LIST_PATH = "words_alpha.txt"

def download_word_list():
    if not os.path.exists(WORD_LIST_PATH):
        urllib.request.urlretrieve(WORD_LIST_URL, WORD_LIST_PATH)

def load_words():
    with open(WORD_LIST_PATH, 'r') as file:
        return set(word.strip().lower() for word in file)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        strings = request.form.get('strings', '').lower().split()
        if not strings:
            return render_template('index.html', error="Please enter at least one string")
        
        words = load_words()
        matching_words = [word for word in words if all(s in word for s in strings)]
        matching_words.sort(key=len)
        
        return render_template('index.html', results=matching_words[:100], strings=strings)
    
    return render_template('index.html')

if __name__ == '__main__':
    download_word_list()
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
