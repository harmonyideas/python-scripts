import json
import os, sys
from flask import Flask, jsonify, request, render_template


class MyDictionary(object):
    def __init__(self):
        self.english_words = []
        # Load the word list
        self.english_words = self.load_words()
        self.add_routes()

    def load_words(self):
        try:
            dir = os.path.dirname(__file__)
            filename = os.path.join(dir, 'dictionary.json')
            with open(filename, "r") as english_dictionary:
                valid_words = json.load(english_dictionary)
                return valid_words
        except Exception as e:
            return str(e)

    def add_routes(self):
        @app.route('/home', methods=['GET'])
        def home_route():
            return render_template('index.html')

        @app.route('/search', methods=['GET', 'POST'])
        def search():
            response = ""
            required = ['search_word']

            if not all(k in request.form for k in required):
                return 'Missing values in POST data', 400

            if request.method == "POST":
                try:
                    search_word = request.form['search_word'].lower()
                    response = self.english_words[search_word]
                except Exception as e:
                    response = e.message
            return jsonify(response), 200

# Instantiate our Node
app = Flask(__name__)

# Generate a unique address for this node

dictionary = MyDictionary()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
