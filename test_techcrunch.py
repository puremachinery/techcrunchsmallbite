from techcrunch import Article
import techcrunch as tc


def test_get_company_name_when_present():
    raw_html = '<a class="cb-card-title-link" href="#dice">\n\t\tDICE\t\t\t</a>'
    html = tc.parse_html(raw_html)
    company_name = tc.get_company_name_from_techcrunch_article(html)
    assert company_name == 'DICE'


def test_get_company_name_when_missing():
    raw_html = '<a class="cb-card" href="#dice">\n\t\tDICE\t\t\t</a>'
    html = tc.parse_html(raw_html)
    company_name = tc.get_company_name_from_techcrunch_article(html)
    assert company_name == tc.default_value


def test_get_company_link_when_present():
    raw_html = """<li class="full"><strong class="key">Founders</strong>
    <span class="value">
    <a href="https://crunchbase.com/person/person/rick-pat" target="_blank">
    Rick Patterson</a></span></li>
    <li class="full"><strong class="key">Website</strong>
    <span class="value"><a href="http://www.dice.com/" target="_blank">
    http://www.dice.com/</a></span></li>"""
    html = tc.parse_html(raw_html)
    company_website = tc.get_company_website_from_techcrunch_article(html)
    assert company_website == 'http://www.dice.com/'


def test_get_company_link_when_missing():
    raw_html = """<li class="full"><strong class="key">Website</strong></li>"""
    html = tc.parse_html(raw_html)
    company_website = tc.get_company_website_from_techcrunch_article(html)
    assert company_website == tc.default_value


def test_get_techcrunch_articles():
    articles = tc.get_techcrunch_articles()
    assert articles


def test_add_company_information():
    articles = [Article('title1', 'url1')]
    articles_with_company_info = tc.add_company_information(articles)
    assert articles_with_company_info[0] == [tc.default_value,  # company name
                                             tc.default_value,  # company url
                                             'title1',  # article title
                                             'url1']  # article url

