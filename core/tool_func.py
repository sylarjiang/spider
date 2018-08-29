


def check_url(domain,link):
    import re
    if re.match(r'^https?:/{2}',link):
        pass
    else:
        if re.match(r'^/',link):
            link = domain+link
        else:
            link = domain + '/' + link
    return link
