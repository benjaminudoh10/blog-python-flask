import os
import json

from flask import (
    request,
    jsonify,
    redirect,
    url_for,
    request,
    render_template,
)
from flask_login import (
    login_required,
    login_user,
    logout_user,
    current_user,
)
from werkzeug.utils import secure_filename
from oauthlib.oauth2 import WebApplicationClient
import requests

from . import app, Article, User, Topic, TopicGroup
from .utils import allowed_file, get_google_provider_cfg

client = WebApplicationClient(app.config['GOOGLE_CLIENT_ID'])

@app.route('/')
def home():
    topics = Topic.get_topics()

    page = request.args.get('page', 1, type=int)
    posts = Article.get_articles(False, page)
    my_posts = current_user.is_authenticated and \
        Article.get_user_posts(current_user.id) or []

    context = {
        'topics': topics,
        'my_posts': my_posts,
        'posts': posts,
    }
    return render_template('home.html', **context)

@app.route('/login')
def login():
    google_provider_cfg = get_google_provider_cfg()
    authorization_endpoint = google_provider_cfg['authorization_endpoint']
    request_uri = client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=f'{request.base_url}/callback',
        scope=['openid', 'email', 'profile'],
    )

    return redirect(request_uri)

@app.route('/login/callback')
def login_callback():
    # Get authorization code Google sent back to you
    code = request.args.get('code')

    # Find out what URL to hit to get tokens that allow you to ask for
    # things on behalf of a user
    google_provider_cfg = get_google_provider_cfg()
    token_endpoint = google_provider_cfg['token_endpoint']

    # Prepare and send a request to get tokens! Yay tokens!
    token_url, headers, body = client.prepare_token_request(
        token_endpoint,
        authorization_response=request.url,
        redirect_url=request.base_url,
        code=code
    )
    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(app.config['GOOGLE_CLIENT_ID'], app.config['GOOGLE_CLIENT_SECRET']),
    )

    # Parse the tokens!
    client.parse_request_body_response(json.dumps(token_response.json()))

    # Now that you have tokens (yay) let's find and hit the URL
    # from Google that gives you the user's profile information,
    # including their Google profile image and email
    userinfo_endpoint = google_provider_cfg['userinfo_endpoint']
    uri, headers, body = client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body)
    userinfo_response_json = userinfo_response.json()

    # You want to make sure their email is verified.
    # The user authenticated with Google, authorized your
    # app, and now you've verified their email through Google!
    if not userinfo_response_json.get('email_verified'):
        return redirect(url_for('home'))

    sub = userinfo_response_json['sub']
    email = userinfo_response_json['email']
    profile_pic = userinfo_response_json['picture']
    name = userinfo_response_json['given_name']

    user_json = {
        'sub': sub,
        'email': email,
        'name': name,
        'profile_pic': profile_pic,
    }
    user = User.get_or_create(user_json)

    login_user(user)

    return redirect(url_for('home'))

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/topics')
def topics():
    topic_groups = TopicGroup.get()

    context = {
        'groups': topic_groups
    }
    return render_template('topics.html', **context)

@app.route('/posts')
def posts():
    posts = [
        {
            'author_img': 'https://miro.medium.com/fit/c/40/40/1*iQYB9PakI5YQsF0GV_KKqQ.jpeg',
            'author_name': '@benjaminudoh10',
            'title': 'Hi',
            'url': 'https://chrissyteigen.medium.com/hi-2e45e6faf764?source=extreme_main_feed---------0-73--------------------7c7fd3e3_8525_441a_b493_c9673528dd4b-------',
            'short_description': 'This was not one of my conventionl writeups. I had to be very intentional about this.',
            'date': 'Jan 27, 1983',
            'post_image': 'https://miro.medium.com/fit/c/400/266/0*wirKJ0HSw389Tqq3',
            'time': 8
        },
        {
            'author_img': 'https://miro.medium.com/fit/c/40/40/1*8OIW1rabg1zNia0RjTm0KQ.png',
            'author_name': 'Amardeep Parmar in The Ascent',
            'title': '20 Realistic Micro-Habits To Live Better Every Day',
            'url': 'https://medium.com/the-ascent/20-realistic-micro-habits-to-live-better-every-day-df1731a2cd41?source=extreme_main_feed---------2-73--------------------7c7fd3e3_8525_441a_b493_c9673528dd4b-------',
            'short_description': 'Aimed at humans, not gods.',
            'date': 'Dec 5, 2020',
            'post_image': 'https://miro.medium.com/fit/c/400/266/1*amkHKqOb8lCXYk2Jum-Spw.jpeg',
            'time': 8
        },
    ]
    return jsonify(posts)

@app.route('/new-story', methods=['GET', 'POST'])
@login_required
def new_story():
    if request.method == 'POST':
        data = request.get_json()
        article = {
            'content': json.dumps(data['content']),
            'title': data['title'],
            'first_paragraph': data['first_paragraph'],
            'draft': data['draft'],
            'user_id': current_user.id,
        }
        Article.insert(article)
        return {
            'status': 200,
            'message': 'Article successfully created',
        }

    return render_template('write.html', article={'content': {}})

@app.route('/stories')
@login_required
def stories():
    draft = request.args.get('draft', False)
    articles = current_user.is_authenticated and \
        Article.get_user_posts(current_user.id, draft) or []
    return render_template('articles.html', articles=articles)

@app.route('/story/<int:story_id>', methods=['GET', 'PUT', 'DELETE'])
@login_required
def story(story_id):
    if request.method == 'PUT':
        data = request.get_json()
        Article.update(story_id, data)
        return {
            'status': 200,
            'message': 'Article updated successfully'
        }
    
    if request.method =='DELETE':
        Article.delete(story_id)
        return {
            'status': 200,
            'message': 'Article deleted successfully'
        }

    article = Article.get(story_id)
    return render_template('article.html', article=article)

@app.route('/story/<int:story_id>/edit')
@login_required
def edit_story(story_id):
    article = Article.get(story_id, False)
    return render_template('write.html', article=article)

@app.route('/story/fetch_url', methods=['POST'])
@login_required
def upload_by_url():
    return {
        'success' : 1,
        'file': {
            'url': request.get_json()['url'],
        }
    }

@app.route('/story/upload_file', methods=['POST'])
@login_required
def upload_file():
    failed_response = {
        'success': 0
    }

    if request.method == 'POST':
        if 'image' not in request.files:
            return failed_response

        file = request.files['image']
        if file.filename == '':
            return failed_response
        if file and allowed_file(file.filename, app.config['ALLOWED_EXTENSIONS']):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return {
                'success' : 1,
                'file': {
                    'url': url_for('static', filename=f'images/blog-images/{filename}'),
                }
            }

    return failed_response
