from flask import Flask, render_template, url_for, flash, redirect, request
from forms import RegistrationForm
from flask_behind_proxy import FlaskBehindProxy
import git

app = Flask(__name__)
proxied = FlaskBehindProxy(app)
app.config['SECRET_KEY'] = '1df9ffd8437d42b30dbf2042fa913737'                # this gets the name of the file so Flask knows it's name

@app.route("/")      
@app.route("/home")                       # this tells you the URL the method below is related to
def home():
    home_message = "Hi, I wanted to explore API's, ORM's, Machine Learning, and more so I decided to make a tool to help \
    Youtube Developers! Given several youtube channels/searches, I help you generate a youtube title! Additionally, I \
    Provide you with tags for your video, auto comment-liking, and an auto response feature."
    return render_template('home.html', subtitle='Home Page', text=home_message)       # this prints HTML to the webpage

@app.route("/titles")
def titles():
  return render_template('titles.html', subtitle='Title page', text='This is the title tool')

@app.route("/comments")
def comments():
  return render_template('comments.html', subtitle='Comment tool', text='This is the comment tool')

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit(): # checks if entries are valid
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home')) # if so - send to home page
    return render_template('register.html', title='Register', form=form)

@app.route("/update_server", methods=['POST'])
def webhook():
    if request.method == 'POST':
        repo = git.Repo('/home/youtubedataproj/front_end_prac')
        origin = repo.remotes.origin
        origin.pull()
        return 'Updated PythonAnywhere successfully', 200
    else:
        return 'Wrong event type', 400


if __name__ == '__main__':               # this should always be at the end
    app.run(debug=True, host="0.0.0.0")