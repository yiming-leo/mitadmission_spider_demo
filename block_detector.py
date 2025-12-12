def is_blocked(page):
    # detect <pre>Request has been blocked.</pre>
    try:
        html = page.html
    except:
        return False

    if not html:
        return False

    return "Request has been blocked" in html
