import os
import glob
import markdown
from flask import Flask, render_template, abort, Blueprint, send_from_directory, request, url_for
from markupsafe import Markup
from werkzeug.utils import secure_filename
from datetime import datetime
from urllib.parse import quote, unquote

app = Flask(__name__)

# Configurations
CONTENT_DIR = os.path.join(app.root_path, 'content')
CATEGORIES = [d for d in os.listdir(CONTENT_DIR) if os.path.isdir(os.path.join(CONTENT_DIR, d))]

# Helper functions
def get_categories():
    return [d for d in os.listdir(CONTENT_DIR) if os.path.isdir(os.path.join(CONTENT_DIR, d))]

@app.context_processor
def inject_globals():
    return dict(categories=get_categories(), now=datetime.now())

def get_stories(category):
    cat_path = os.path.join(CONTENT_DIR, category)
    if not os.path.exists(cat_path):
        return []
    files = glob.glob(os.path.join(cat_path, '*.md'))
    stories = []
    for f in files:
        with open(f, encoding='utf-8') as file:
            lines = file.readlines()
            title = lines[0].replace('#', '').strip() if lines and lines[0].startswith('#') else os.path.splitext(os.path.basename(f))[0]
            excerpt = ''.join(lines[1:4]).strip() if len(lines) > 3 else ''
            stories.append({'title': title, 'filename': os.path.splitext(os.path.basename(f))[0], 'excerpt': excerpt, 'category': category})
    return stories

def get_story(category, story_name):
    file_path = os.path.join(CONTENT_DIR, category, story_name + '.md')
    if not os.path.exists(file_path):
        return None
    with open(file_path, encoding='utf-8') as f:
        md_content = f.read()
        html = markdown.markdown(md_content, extensions=['fenced_code', 'codehilite', 'meta', 'toc'])
    return html, md_content

# Blueprints
main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    categories = get_categories()
    stories_by_cat = {cat: get_stories(cat)[:5] for cat in categories}
    return render_template('index.html', categories=categories, stories_by_cat=stories_by_cat)

@main_bp.route('/category/<category>/')
def category_view(category):
    if category not in get_categories():
        abort(404)
    stories = get_stories(category)
    page = int(request.args.get('page', 1))
    per_page = 10
    total = len(stories)
    paged = stories[(page-1)*per_page:page*per_page]
    next_url = url_for('main.category_view', category=category, page=page+1) if page*per_page < total else None
    prev_url = url_for('main.category_view', category=category, page=page-1) if page > 1 else None
    return render_template('category.html', category=category, stories=paged, next_url=next_url, prev_url=prev_url)

@main_bp.route('/category/<category>/<story_name>/')
def story_view(category, story_name):
    if category not in get_categories():
        abort(404)
    story = get_story(category, story_name)
    if not story:
        abort(404)
    html, md_content = story
    return render_template('story.html', category=category, story_name=story_name, html=Markup(html), md_content=md_content)

@main_bp.route('/search')
def search():
    query = request.args.get('q', '').lower()
    results = []
    if query:
        for cat in get_categories():
            for story in get_stories(cat):
                if query in story['title'].lower() or query in story['excerpt'].lower() or query in cat.lower():
                    results.append(story)
    return render_template('search.html', query=query, results=results)

@main_bp.route('/sitemap.xml')
def sitemap():
    pages = []
    ten_days_ago = (datetime.now()).date().isoformat()
    for cat in get_categories():
        pages.append(f"{request.url_root}category/{quote(cat)}/")
        for story in get_stories(cat):
            pages.append(f"{request.url_root}category/{quote(cat)}/{quote(story['filename'])}/")
    sitemap_xml = render_template('sitemap.xml', pages=pages, lastmod=ten_days_ago)
    return sitemap_xml, {'Content-Type': 'application/xml'}

@main_bp.route('/robots.txt')
def robots():
    return send_from_directory(app.static_folder, 'robots.txt')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

app.register_blueprint(main_bp)

if __name__ == '__main__':
    app.run(debug=True)
