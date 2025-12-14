import logging

from test_admission import test_first_layer_crawl
from playwright.sync_api import sync_playwright

from test_example import test_has_title

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)


def main():
    with sync_playwright() as p:
        # browser = p.chromium.launch(headless=True)
        browser = p.chromium.launch_persistent_context(
            user_data_dir="playwright_profile",
            headless=False
        )
        page = browser.new_page()
        test_first_layer_crawl(page)
        browser.close()

    # test_has_title()


# yield browser, page
# return


# conda activate mitadmission
# D:\PythonProject\mitadmission_crawl_demo
# python main.py

# Kill all the Chrome PID when you run this command!
if __name__ == "__main__":
    main()
