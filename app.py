from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/events')
def events():
    return render_template("events.html")

@app.route('/techHer')
def techher():
    return render_template("techHer.html")

@app.route('/resources')
def resources():
    return render_template("resources.html")

@app.route('/newsletter')
def newsletter():
    return render_template("newsletter.html")

if __name__ == '__main__':
    app.run(debug=True)