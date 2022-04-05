from flask import Flask
from depth_chart_scraper import scrape_depth

app = Flask(__name__)

@app.route('/')

def depth_chart_scraper():
    scrape_depth()

