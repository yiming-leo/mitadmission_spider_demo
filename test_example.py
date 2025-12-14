import re

from DrissionPage import ChromiumOptions
from DrissionPage import Chromium
from playwright.sync_api import Page, expect


def test_has_title():
    co = ChromiumOptions()
    browser = Chromium(co)
    agent_dp = browser.latest_tab
    agent_dp.get(f"https://mitadmissions.org/blogs/page/1/")
    browser.quit(force=True, del_data=True)


def test_get_started_link(page: Page):
    page.goto("https://playwright.dev/")

    # Click the get started link.
    page.get_by_role("link", name="Get started").click()

    # Expects page to have a heading with the name of Installation.
    expect(page.get_by_role("heading", name="Installation")).to_be_visible()
