import requests
import re
import titlecase
import datetime
import random
from bs4 import BeautifulSoup

from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import Paragraph, Frame
from reportlab.lib.utils import ImageReader

from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
import reportlab.rl_config
reportlab.rl_config.warnOnMissingFontGlyphs = 0

pdfmetrics.registerFont(TTFont('Vera', 'Vera.ttf'))
pdfmetrics.registerFont(TTFont('VeraBd', 'VeraBd.ttf'))


def main():
    prompt_list = [
        "Welcome to the ABS CBN News PDF Generator. \n",
        "Please select from the following:",
        "1 - Headline News",
        "2 - Business",
        "3 - Entertainment",
        "4 - Overseas",
        "5 - Spotlight",
        "6 - Sports",
        "Not a valid value. Please try again."]
    welcome_prompt = " \n".join(prompt_list[:len(prompt_list)-1]) + " \n"
    error_msg = len(prompt_list)-1
    print(welcome_prompt)

    while True:
        try:
            inquire_input = int(input("Select: "))
            if inquire_input == 1:
                url = ("https://news.abs-cbn.com/news")
                soup_list = soup_getter(url, "news")
            if inquire_input == 2:
                url = "https://news.abs-cbn.com/business"
                soup_list = soup_getter(url, "business")
            if inquire_input == 3:
                url = "https://news.abs-cbn.com/entertainment"
                soup_list = soup_getter(url, "entertainment")
            if inquire_input == 4:
                url = "https://news.abs-cbn.com/overseas"
                soup_list = soup_getter(url, "overseas")
            if inquire_input == 5:
                url = "https://news.abs-cbn.com/spotlight"
                soup_list = soup_getter(url, "spotlight")
            if inquire_input == 6:
                url = "https://news.abs-cbn.com/sports"
                soup_list = soup_getter(url, "sports")

            pick = random.choice(soup_list)

            if inquire_input < 6 | inquire_input <= 0:
                raise ValueError(f"{prompt_list[error_msg]}")
        except (ValueError, UnboundLocalError):
            print(f"{prompt_list[error_msg]}")
            continue
        else:
            break

    final_url = "https://news.abs-cbn.com"+pick

    title, date = title_builder(str(pick))
    content = content_getter(final_url)
    news_pdf = generate_news_pdf(title, date, content)

    print(f"{news_pdf}! Please note that this news is published by ABS-CBN Corporation, a media and entertainment organization in the Philippines. \nVisit {final_url} for the source details.\nAll rights and credits go directly to ABS CBN.\nNo copyright infringement intended.")


def soup_getter(url, type):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        html_content = response.text
    else:
        print("Try again later.")

    home_soup = BeautifulSoup(html_content, 'html.parser')
    results = home_soup.find_all('article')

    news_list = []

    for result in results:
        match = re.search(r'href="(/'+type+'/\d{2}/.+)">{1}', str(result))
        if match:
            if match.group(1) not in news_list:
                news_list.append(match.group(1))

    return news_list


def content_getter(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'
    }
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        html_content = response.text
    else:
        print("Try again later.")

    content_list = []

    content_soup = BeautifulSoup(html_content, 'html.parser')
    content_maker = content_soup.find_all("p")
    for line in content_maker:
        match = re.search(r"<p>(.+)</p>", str(line))
        if match:
            if match.group(1) != "Share":
                if "Related video" not in match.group(1):
                    if "RELATED VIDEO" not in match.group(1):
                        content_list.append(match.group(1))

    return content_list


def title_builder(title):
    match = re.search(r"/.+/(\d{2}/\d{2}/\d{2})/(.+)", title)
    if match:
        n_date = match.group(1)
        snippet = match.group(2)
    x = snippet.replace("-", " ")
    f_title = titlecase.titlecase(x)

    mm, dd, yy = n_date.split("/")
    x_date = datetime.datetime(int('20'+yy), int(mm), int(dd))
    x_date = x_date.strftime("%B %d, %Y, %A")

    return f_title, x_date


def generate_news_pdf(title, date, contents):

    fileName = "news.pdf"

    pdf = canvas.Canvas(fileName)
    pdf.setTitle(title)

    # Logo builder
    logo_src = "http://t3.gstatic.com/images?q=tbn:ANd9GcSBo1m8t1CzVvU6ZFDAb6g7cw80RoqVXct0NmRCHnJqSxZNQ4SV"

    logo = ImageReader(logo_src)

    logo_width = 1*inch
    logo_height = 1*inch
    logo_x = 0.775*inch
    logo_y = 760

    pdf.setFont('VeraBd', 10)
    pdf.drawString(0.9*inch+logo_x, 30+logo_y, title)
    pdf.setFont('Helvetica', 8.5)
    pdf.drawString(0.9*inch+logo_x, 15+logo_y, date)

    pdf.drawImage(logo, logo_x, logo_y, width=logo_width,
                  height=logo_height, mask=[255, 255, 255])

    styles = getSampleStyleSheet()
    styleN = styles['Normal']
    story = []
    story_p2 = []

    def footer_disclaimer():
        pdf.setFont('Vera', 6.5)
        pdf.drawString(logo_x+15, 0.65 * inch+16,
                       "Please note that this news is published by ABS-CBN Corporation, a media and entertainment organization in the Philippines.")
        pdf.drawString(logo_x+15, 0.65 * inch+8,
                       "Visit this link for the source details: ")
        pdf.drawString(logo_x+15, 0.65 * inch,
                       "All rights and credits go directly to ABS CBN.No copyright infringement intended.")

    if len(contents) > 12:

        content_part1 = contents[:12]
        content_part2 = contents[12:]
        create_content_p1 = " <br/><br />".join(content_part1)
        create_content_p2 = " <br/><br />".join(content_part2)
        story.append(Paragraph(create_content_p1, styleN))
        f1 = Frame(inch, inch, 6.5*inch, 9.5*inch, showBoundary=1)
        f1.addFromList(story, pdf)

        footer_disclaimer()

        pdf.showPage()

        f2 = Frame(inch, inch, 6.5*inch, 9.5*inch, showBoundary=1)
        story_p2.append(Paragraph(create_content_p2, styleN))
        f2.addFromList(story_p2, pdf)
        footer_disclaimer()

    else:
        create_content = " <br/><br />".join(contents)
        story.append(Paragraph(create_content, styleN))
        f = Frame(inch, inch, 6.5*inch, 9.5*inch, showBoundary=1)
        f.addFromList(story, pdf)

        footer_disclaimer()

    pdf.save()

    return "Success"


if __name__ == "__main__":
    main()
