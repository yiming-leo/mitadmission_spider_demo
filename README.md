# MIT Admission Crawl Demo by Playwright & DrissionPage

# Requirements

## Page Number You Want Crawl

1. set up newest `page_number` in test_first_layer_crawl()

## Proxy Settings

1. set up your native proxy (Clash e.g.) and open the external control
2. set up the `BASE_URL`, `SECRET` `PROXY_NAME` in `proxy_set.py` by your own proxy
3. make sure your own proxy is open & connected (the script will auto select the newest available node in specific
   proxy's rule)

# Run
please do following cmd to run this demo:
### `pip install requirements.txt`
### `python main.py`