
def check_url(link):
    import re
    if re.match(r'^https?:/{2}',link):
        pass
    else:
        link = ''
    return link
