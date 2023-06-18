from flask import Flask, request, render_template, redirect, url_for
import json

app = Flask(__name__)


last_id = 0


def fetch_blog_posts():
    """Fetch the blog posts from json file"""
    with open('posts.json', 'r') as file:
        blog_posts = json.load(file)
        return blog_posts


@app.route('/')
def index():
    """Fetch blog posts and render them into the html template"""
    blog_posts = fetch_blog_posts()
    return render_template('index.html', posts=blog_posts)


def generate_id():
    """Generate an ID for each blog post"""
    global last_id
    last_id += 1
    return last_id


def save_new_post(post):
    """Read the existing blog posts from the JSON file,
    append new posts to the file"""
    with open('posts.json', 'r') as file:
        blog_posts = json.load(file)

    post['id'] = generate_id()

    blog_posts.append(post)

    with open('posts.json', 'w') as file:
        json.dump(blog_posts, file, indent=4)

    return post['id']


def save_post(post):
    """Read the existing blog posts from the JSON file, find the location
    update and save the post"""
    with open('posts.json', 'r') as file:
        blog_posts = json.load(file)

    location = None
    for i, p in enumerate(blog_posts):
        if p['id'] == post['id']:
            location = i
            break

    if location is not None:
        blog_posts[location] = post

        with open('posts.json', 'w') as file:
            json.dump(blog_posts, file, indent=4)

        return True

    return False


@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        """Handle the form submission and add a new blog post"""
        new_post = {
            'id': generate_id(),
            'author': request.form.get('author'),
            'title': request.form.get('title'),
            'content': request.form.get('content')
        }
        save_new_post(new_post)
        return redirect(url_for('index'))

    return render_template('add.html')


@app.route('/delete/<int:post_id>')
def delete(post_id):
    """Read json file, find the blog post based on id, write
    update data back to file"""
    with open('posts.json', 'r') as file:
        blog_posts = json.load(file)

    for post in blog_posts:
        if post['id'] == post_id:
            blog_posts.remove(post)
            break

    with open('posts.json', 'w') as file:
        json.dump(blog_posts, file, indent=4)

    return redirect(url_for('index'))


def fetch_post_by_id(post_id):
    """Read json file, find the blog post with a given ID"""
    with open('posts.json', 'r') as file:
        blog_posts = json.load(file)

    for post in blog_posts:
        if post['id'] == post_id:
            return post

    return None


@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id):
    """Fetch the blog post from the JSON file or database"""
    post = fetch_post_by_id(post_id)
    if post is None:
        return "Post not found", 404

    if request.method == 'POST':
        # Update the post details based on the form data
        post['author'] = request.form['author']
        post['title'] = request.form['title']
        post['content'] = request.form['content']

        # Save the updated post back to the JSON file or database
        save_post(post)

        return redirect(url_for('index'))

    # If it's a GET request, display the update form
    return render_template('update.html', post=post)


if __name__ == '__main__':
    app.run()
