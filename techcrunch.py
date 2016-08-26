from bs4 import BeautifulSoup
import collections
import csv
import feedparser
import requests


default_value = 'n/a'
Article = collections.namedtuple('Article', ['title', 'url'])


def get_link_from_feedburner_entry(entry):
    if 'feedburner_origlink' in entry.keys():
        return entry.feedburner_origlink
    elif 'link' in entry.keys():
        return entry.link
    else:
        return default_value


def get_techcrunch_articles():
    base_url = 'http://feeds.feedburner.com/'
    feed_paths = ['TechCrunch/', 'TechCrunch/startups',
                  'TechCrunch/fundings-exits', 'TechCrunch/social',
                  'Mobilecrunch', 'crunchgear', 'TechCrunch/europe',
                  'TechCrunchIT', 'greentech']
    feeds = [base_url + path for path in feed_paths]
    parsed_feeds = [feedparser.parse(feed) for feed in feeds]
    articles = set()
    for parsed_feed in parsed_feeds:
        for entry in parsed_feed.entries:
            title = entry.title if 'title' in entry.keys() else default_value
            link = get_link_from_feedburner_entry(entry)
            articles.add(Article(title, link))
    return articles


def get_company_name_from_techcrunch_article(html):
    """There can be more than one company specified in the CrunchBase tile,
    but determining which is the primary subject of the article, if any,
    is beyond the scope of this project, so we'll just take the first one.
    """
    link_tags = html.find_all('a', {'class': 'cb-card-title-link'})
    return link_tags[0].contents[0].strip() if link_tags else default_value


def get_company_website_from_techcrunch_article(html):
    """There can be more than one company specified in the CrunchBase tile,
    but determining which is the primary subject of the article, if any,
    is beyond the scope of this project, so we'll just take the first one.
    """
    company_website = default_value
    lis = html.find_all('li', {'class': 'full'})
    for li in lis:
        if li.span is not None and li.span.a is not None:
            if li.span.a['href'] == li.span.a.contents[0].strip():
                company_website = li.span.a.contents[0].strip()
                break
    return company_website


def parse_html(raw_html):
    return BeautifulSoup(raw_html, 'html.parser')


def get_html(url):
    try:
        return parse_html(requests.get(url).text)
    except requests.exceptions.RequestException as e:
        print e
        return parse_html('')


def save_article_information(article_info, filename='tc.csv'):
    with open(filename, 'wb') as csvfile:
        writer = csv.writer(csvfile)
        for row in article_info:
            row = [s.encode('utf-8') for s in row]
            writer.writerow(row)


def add_company_information(articles):
    article_info = []
    for article in articles:
        if article.url == default_value:
            company_name, company_website = default_value
        else:
            html = get_html(article.url)
            company_name = get_company_name_from_techcrunch_article(html)
            company_website = get_company_website_from_techcrunch_article(html)
        article_info.append(
            [article.title, article.url, company_name, company_website])
    return article_info


if __name__ == '__main__':
    tc_articles = get_techcrunch_articles()
    articles_with_company_info = add_company_information(tc_articles)
    save_article_information(articles_with_company_info)
