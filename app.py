import narrator
from flask import Flask

app = Flask(__name__)

@app.route('/run')
def run_program():
    narrator.main()  # This calls the main function in narrator.py
    return 'Program executed!'

@app.route('/')
def home():
    return 'Hello, World!'

if __name__ == '__main__':
    app.run(debug=True)