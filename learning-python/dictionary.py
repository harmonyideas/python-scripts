import json
import os
from flask import Flask, jsonify, request, render_template


class MyDictionary():
    def __init__(self):
        self.english_words = []
        # Load the word list
        self.english_words = self.load_words()
        self.add_routes()

    def load_words(self):
        try:
          filepath = os.path.abspath(__file__)
          with open(os.path.join(os.path.dirname(filepath), 'dictionary.json', encoding='utf-8')) as f:
            return json.load(f)
        except: OSError as e:
          print("Could not open/read file:", fname)
            return str(e)

    def add_routes(self):
        @app.route('/home', methods=['GET'])
        def home_route():
            return render_template('index.html')

        @app.route('/search', methods=['GET', 'POST'])
        def search():
            if request.method == "POST":
                search_word = request.form.get('search_word', '').lower()
                if not search_word:
                    return 'Missing values in POST data', 400
                response = self.english_words.get(search_word, f'Word "{search_word}" not found')
                return jsonify(response), 200
            return 'Invalid request method', 405


# Instantiate our Node
app = Flask(__name__)

dictionary = MyDictionary()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
