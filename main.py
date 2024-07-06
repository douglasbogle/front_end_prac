from flask import Flask, render_template, url_for, redirect, request
from forms import RegistrationForm
from flask_behind_proxy import FlaskBehindProxy
from flask_sqlalchemy import SQLAlchemy

# TEST REMOTELY LIKE GOOGLE EXAMPLE, use pythonanywhere address

app = Flask(__name__)
proxied = FlaskBehindProxy(app)
app.config['SECRET_KEY'] = '2c048f793a7ecdf8178dcd926640eb1a'                # this gets the name of the file so Flask knows it's name

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

class User(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(20), unique=True, nullable=False)
  email = db.Column(db.String(120), unique=True, nullable=False)
  password = db.Column(db.String(60), nullable=False)

  def __repr__(self):
    return f"User('{self.username}', '{self.email}')"

with app.app_context():
  db.create_all()


@app.route("/")      
@app.route("/home")                       # this tells you the URL the method below is related to
def home():
    home_message = "I wanted to explore API's, ORM's, Machine Learning, and more so I decided to make a tool to help \
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
    if form.validate_on_submit():  # works when i do it in incognito!
        user = User(username=form.username.data, email=form.email.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()

        return redirect(url_for('home'))
    # print("Form validation errors:", form.errors) form works
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


if __name__ == '__main__':         \
    app.run(debug=True, host="0.0.0.0")