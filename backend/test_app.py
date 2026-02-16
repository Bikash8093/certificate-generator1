from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "Flask is running!"

if __name__ == "__main__":
    print(">>> Starting Flask test app...")
    app.run(host="127.0.0.1", port=5000, debug=True)