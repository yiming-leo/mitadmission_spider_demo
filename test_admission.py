import csv
import logging
import time
import block_detector
import proxy_set

from DrissionPage import ChromiumOptions
from DrissionPage import Chromium
from DrissionPage import SessionPage
from lxml.etree import ParserError
from playwright.sync_api import Page, expect

# ref: https://playwright.dev/python/docs/writing-tests
# ref: https://www.drissionpage.cn/get_start/import

# Title | Author | Comment Count | Time | Article Content | Images In Article|

"""
Mission is below:

https://mitadmissions.org/blogs/page/*/
(1<*<479)

Title: .post-tease__title
Author: .post-tease__meta-item--author a
Time: tease__meta-item--date

https://mitadmissions.org/blogs/entry/*/

Article Content: article__body js-hang-punc
Images In Article: img (extracting src's URL)

https://mitadmissions.org/blogs/page/*/
Comment Count: .tease__comment-text a (playwright)
"""


def test_first_layer_crawl(page: Page):
    # how many page in MIT Admissions (+1 for range)
    page_number = 480
    # file name what wanna write in
    file_name = "mitadmission.csv"

    # records is for storage all detailed links, authors,...  by order
    # dict could handle col-inserting
    records = {
        "links": [],
        "titles": [],
        "authors": [],
        "times": [],
        "img_urls": [],
        "comment_counts": [],
        "article_contents": []
    }

    # --------------------- drissionpage browser control ---------------------
    agent = Chromium().latest_tab

    # --------------------- proxy control ---------------------
    proxy_set.init_node_pool()

    # no browser popup
    # sp = SessionPage()

    # =========================== author, time, title, link ===========================
    # use DrissionPage's SessionPage (cannot perform JS)
    # first info layer access & extract (author, time, title, link)
    for i in range(1, page_number):
        # >------if blocked
        proxy_set.auto_handle_proxy(agent)
        # <------if blocked
        agent.get(f"https://mitadmissions.org/blogs/page/{i}/")
        # titles: a [] for article's title
        article_titles = agent.eles('.post-tease__title')

        # hgroups: a [] for article's author, time, and url link
        hgroups = agent.eles('.post-tease__hgroup')
        # extract details from hgroups
        for hgroup in hgroups:
            link = (hgroup
                    .ele('.post-tease__h')
                    .ele('.post-tease__h__link')
                    .attr('href'))
            author = (hgroup
                      .ele('.post-tease__meta-list')
                      .ele('.post-tease__meta-item post-tease__meta-item--author')
                      .ele('tag:a')
                      .text)
            a_time = (hgroup
                      .ele('.post-tease__meta-list')
                      .ele('.post-tease__meta-item tease__meta-item--date')
                      .text)

            # print(f"{author} -- {a_time} -- {link}")

            records["links"].append(link)
            records["authors"].append(author)
            records["times"].append(a_time)

        for article_title in article_titles:
            # print(f"{article_title.text}\n")

            records["titles"].append(article_title.text)

        logging.info(f"-------- author, a_time, title, link page: {i} --------")
        time.sleep(2)

    # =========================== article__contents, image_urls by links ===========================
    # details access & extract article__contents, image_urls
    for i in range(0, len(records["links"])):
        # each detailed link will be accessed at this stage
        # ---------------------------- article__contents by links----------------------------
        agent.get(records["links"][i])
        # >------if blocked
        proxy_set.auto_handle_proxy(agent)
        # <------if blocked
        article_content = agent.ele(".article__body js-hang-punc").text
        records["article_contents"].append(article_content)

        # ---------------------------- image_urls by links----------------------------
        # img_url is for storage each SINGLE article's img_url temporary
        img_url = []
        imgs = agent.ele(".article__body js-hang-punc").eles("tag:img")

        # !!!cuz Lazyload, [None, None, None] will happen due to the lazyload!!!
        # need to use attr "data-flickity-lazyload-src" to grab
        # Chrome DevTools -> Network -> 3G, Disable cache -> Ctrl+R -> Watch specific lazyload image what will happen
        for img in imgs:
            img_url.append(img.attr("src") or img.attr("data-flickity-lazyload-src"))
        records["img_urls"].append(img_url)
        # print(records["img_urls"])
        logging.info(f"-------- article__contents, image_urls page: {int(i / 16) + 1} --------")
        time.sleep(2)

    # print(f"{records}\n")
    logging.info("========= DATA EXCEPT comment_count HAS BEEN READ =========")

    # =========================== An independent Loop comment_count ===========================
    # here comment_count cannot be crawled cuz the JS Dynamic Insertion
    # need to use Playwright to catch

    for i in range(1, page_number):
        # >------if blocked
        proxy_set.auto_handle_proxy(page)
        # <------if blocked
        page.goto(f"https://mitadmissions.org/blogs/page/{i}/")
        # ref: https://playwright.dev/python/docs/api/class-elementhandle#element-handle-query-selector-all
        comment_rows = page.query_selector_all(".tease__comment-text a")
        # reading pseudo-elements
        for comment_row in comment_rows:
            text_raw = comment_row.inner_text().strip('"')
            # "column/columns" clean, if no comment / null, return 0
            comment_count = text_raw.strip('comments') or text_raw.strip('comment') or 0 if text_raw.find(
                'comment') else 0
            records["comment_counts"].append(comment_count)
        time.sleep(2)
        logging.info(f"\n-------- take a 5s break, comment_count page: {i} --------")

    # ---------------------------- write into csv by column----------------------------
    # get total length
    total = len(records["links"])
    with open(file_name, "w", newline="", encoding="UTF-8") as f:
        writer = csv.writer(f)
        # write title
        writer.writerow([
            "Title",
            "Author",
            "Comment Count",
            "Time",
            "Article Content",
            "Images In Article"
        ])

        for i in range(total):
            writer.writerow([
                records["titles"][i],
                records["authors"][i],
                records["comment_counts"][i],
                records["times"][i],
                records["article_contents"][i],
                records["img_urls"][i],
            ])

        logging.info("========= DATA HAS BEEN WRITTEN =========")
