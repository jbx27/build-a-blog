from flask import Flask, request, redirect, render_template, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:buildablog@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = "forflashmessages"


class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(1000))

    def __init__(self, title, body):
        self.title = title
        self.body = body

@app.route('/', methods=['POST', 'GET'])
def index():
    return redirect('/blog')

@app.route('/blog', methods=['GET', 'POST'])
def blog():
    post_id = request.args.get('id')
    if (post_id):
        post = Blog.query.get(post_id)
        return render_template('post_page.html', post = post)
    else:
        posts = Blog.query.all()
        return render_template("/blog.html", posts = posts)
    
   
@app.route('/newpost', methods=['GET', 'POST'])
def newpost():
    if request.method == 'POST':
        post_title = request.form['title']
        post_body = request.form['body']

#flash message for blank post title or body
        if len(post_title) == 0:
            flash("Title cannot be blank.")
        elif len(post_body) == 0:
            flash("Blog post cannot be blank.")
        else:
            new_post = Blog(post_title, post_body)
            db.session.add(new_post)
            db.session.commit()
            return redirect('/blog?id={}'.format(new_post.id))

    return render_template('new_post.html')


if __name__ == '__main__':
    app.run()