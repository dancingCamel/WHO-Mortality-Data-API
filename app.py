from flask import Flask


app = Flask(__name__)

app.secret_key = "1aV1B&r6^wdC"

if __name__ == '__main__':
    app.run(port=500, debug=True)
