# Kids Stories

A production-ready Flask-based static web application for sharing stories organized by categories.

## Features
- Stories in Markdown, organized by category
- Modern, mobile-friendly UI
- SEO optimized (URLs, meta, sitemap, robots.txt, Open Graph)
- Search by title, content, or category
- Pagination for story lists
- Ad and analytics placeholders
- Easy content editing
- Modular Flask blueprint structure

## Project Structure
```
kids-stories/
├── app.py
├── requirements.txt
├── README.md
├── content/
│   ├── fairy-tales/
│   │   ├── cinderella.md
│   │   └── hansel-and-gretel.md
│   └── animal-stories/
│       └── the-lion-and-the-mouse.md
├── static/
│   ├── css/
│   │   └── style.css
│   ├── js/
│   │   └── main.js
│   └── images/
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── category.html
│   ├── story.html
│   ├── search.html
│   └── 404.html
├── admin/
│   └── add_story.py
├── sitemap.xml
└── robots.txt
```

## Setup Instructions
1. Clone the repo and install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the app:
   ```bash
   python app.py
   ```
3. Visit [https://fairy-tales.rathnaschools.com](https://fairy-tales.rathnaschools.com)

## Adding/Editing Stories
- Stories are Markdown (.md) files under `content/<category>/` folders.
- Each file starts with `# Title` on the first line.
- To add a new story or category, use the `admin/add_story.py` script or manually add files.

## Example Markdown Format
```
# The Lion and the Mouse

Once upon a time, a lion was asleep when a little mouse began running up and down upon him...

## Moral
Kindness is never wasted.
```

## SEO & Ads
- SEO meta tags and Open Graph tags are included in templates.
- AdSense/Analytics placeholders are in `base.html`.

## License
MIT
