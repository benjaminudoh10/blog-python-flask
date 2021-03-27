import os
import json
from datetime import datetime

from flask import (
    request,
    jsonify,
    redirect,
    url_for,
    request,
    render_template,
)
from werkzeug.utils import secure_filename

from . import app, models, db
from .utils import allowed_file

@app.route('/')
def home():
    topics = models.Topic.get_topics()

    trends = [
        {
            'title': 'Cardano (ADA) is now available on Coinbase',
            'date': 'Mar 19',
            'time': 5,
            'name': 'Coinbase in The Coinbase Blog',
            'url': 'https://blog.coinbase.com/cardano-ada-is-now-available-on-coinbase-dd30c1e0d93a?source=home---------0---------------------268a3e05_41d3_49ec_837e_c08db2a55aa5-------7',
            'image_url': 'https://miro.medium.com/fit/c/40/40/1*gBXfxLQiRiP5NycsMHPzKA.png'
        },
        {
            'title': 'The Challenge All Stars Full Cast Preseason Power Ranking',
            'date': 'Mar 21',
            'time': 14,
            'name': 'Alan Aguirre',
            'url': 'https://theallanaguirre.medium.com/the-challenge-all-stars-full-cast-preseason-power-ranking-2e54c0243017?source=home---------1---------------------268a3e05_41d3_49ec_837e_c08db2a55aa5-------7',
            'image_url': 'https://miro.medium.com/fit/c/40/40/1*J4NkADsXvoqeaTZlGiIZNw.jpeg'
        },
        {
            'title': 'Yes, here’s the best CSS framework in 2021',
            'date': 'Mar 20',
            'time': 4,
            'name': '@maisonfutari in ITNEXT',
            'url': 'https://itnext.io/yes-heres-the-best-css-framework-in-2021-2c9eb2ced678?source=home---------2---------------------268a3e05_41d3_49ec_837e_c08db2a55aa5-------7',
            'image_url': 'https://miro.medium.com/fit/c/40/40/1*yAqDFIFA5F_NXalOJKz4TA.png'
        },
        {
            'title': 'What Does Today’s News About HOGE Mean?',
            'date': 'Mar 21',
            'time': 6,
            'name': 'Jesse J Rogers in Compounding Interest Podcast',
            'url': 'https://medium.com/compounding-interest-podcast/what-does-todays-news-about-hoge-mean-9bb59dfc983e?source=home---------3---------------------268a3e05_41d3_49ec_837e_c08db2a55aa5-------7',
            'image_url': 'https://miro.medium.com/fit/c/40/40/1*KwGtQ8YjoQpelFRWAoJddw.png'
        },
        {
            'title': '6 Resources To Help You Ace Your Data Science Interview',
            'date': 'Mar 20',
            'time': 6,
            'name': 'Safra D. WaliMew',
            'url': 'https://towardsdatascience.com/6-resources-to-help-you-ace-your-data-science-interview-6a4ef973e90b?source=home---------4---------------------268a3e05_41d3_49ec_837e_c08db2a55aa5-------7',
            'image_url': 'https://miro.medium.com/fit/c/40/40/1*eLxNtw6hQ4-3HrHda5BCCw.png'
        },
        {
            'title': 'The Dark Side of Logic: The near crash of SmartLynx Estonia flight 9001',
            'date': 'Mar 20',
            'time': 21,
            'name': 'Colonel_Goldberg',
            'url': 'https://admiralcloudberg.medium.com/the-dark-side-of-logic-the-near-crash-of-smartlynx-estonia-flight-9001-68b9f42b1fb2?source=home---------5---------------------268a3e05_41d3_49ec_837e_c08db2a55aa5-------7',
            'image_url': 'https://miro.medium.com/fit/c/40/40/2*pZPMtIONqtJYi2xHYD_Ivg.jpeg'
        }
    ]

    posts = [
        {
            'author_img': 'https://miro.medium.com/fit/c/40/40/1*iQYB9PakI5YQsF0GV_KKqQ.jpeg',
            'author_name': 'chrissy teigen',
            'title': 'Hi',
            'url': 'https://chrissyteigen.medium.com/hi-2e45e6faf764?source=extreme_main_feed---------0-73--------------------7c7fd3e3_8525_441a_b493_c9673528dd4b-------',
            'short_description': 'I had no idea when I would be ready to write this. Part of me thought it would be early on, when I was still really feeling the pain of...',
            'date': 'Oct 27, 2020',
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
        {
            'author_img': 'https://miro.medium.com/fit/c/40/40/1*5xv8leEElYbEGzsTRU0Jnw.jpeg',
            'author_name': 'inc. magazine in Inc Magazine',
            'title': 'Bill Gates: 4 Choices in Life Separate the Doers From the Dreamers',
            'url': 'https://aninjusticemag.com/we-cant-afford-to-live-anymore-and-the-rich-are-gaslighting-us-ac8e5bc9b455?source=extreme_main_feed---------35-73--------------------7c7fd3e3_8525_441a_b493_c9673528dd4b-------',
            'short_description': 'Practice the simple habits that have helped Gates become the world’s fourth-richest person',
            'date': 'Feb 19',
            'post_image': 'https://miro.medium.com/fit/c/400/266/1*Ja9gm1DpMCrmXKE2y5mk5w.jpeg',
            'time': 4
        },
        {
            'author_img': 'https://miro.medium.com/fit/c/40/40/1*TyRLQdZO7NdPATwSeut8gg.png',
            'author_name': 'Lew C in Better Programming',
            'title': 'Flutter Is About To Win Over the Web',
            'url': 'https://betterprogramming.pub/flutter-is-about-to-win-over-the-web-be0a205af03d?source=extreme_main_feed---------8-73--------------------7c7fd3e3_8525_441a_b493_c9673528dd4b-------',
            'short_description': 'The cross-platform framework offers the most compelling web development experience',
            'date': 'Feb 12',
            'post_image': 'https://miro.medium.com/fit/c/400/266/1*jgFIhR2M19NPVsSVXOGe-w.png',
            'time': 12
        },
    ]

    context = {
        'topics': topics,
        'trends': trends,
        'posts': posts
    }
    return render_template('home.html', **context)

@app.route('/topics')
def topics():
    topic_groups = models.TopicGroup.get()

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
def new_story():
    if request.method == 'POST':
        data = request.get_json()
        article = {
            'content': json.dumps(data),
            'title': data['blocks'][0]['data']['text']
        }
        models.Article.insert(article)
        return {
            'status': 200,
            'message': 'Article successfully created',
        }

    return render_template('write.html', article={'content': {}})

@app.route('/stories')
def stories():
    articles = models.Article.get_all_articles()
    return render_template('articles.html', articles=articles)

@app.route('/story/<int:story_id>', methods=['GET', 'PUT'])
def story(story_id):
    if request.method == 'PUT':
        data = request.get_json()
        models.Article.update(story_id, json.dumps(data))
        return {
            'status': 200,
            'message': 'Article updated successfully'
        }

    article = models.Article.get(story_id)
    return render_template('article.html', article=article)

@app.route('/story/<int:story_id>/edit')
def edit_story(story_id):
    article = models.Article.get(story_id, False)
    return render_template('write.html', article=article)

@app.route('/story/fetch_url', methods=['POST'])
def upload_by_url():
    return {
        'success' : 1,
        'file': {
            'url': request.get_json()['url'],
        }
    }

@app.route('/story/upload_file', methods=['POST'])
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
