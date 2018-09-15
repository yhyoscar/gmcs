import requests

def check_url(url):
    try:
        rtest = requests.head(url)
    except requests.exceptions.HTTPError as errh:
        print ("Http Error:", url); return False
    except requests.exceptions.ConnectionError as errc:
        print ("Connecting Error:", url); return False
    except requests.exceptions.Timeout as errt:
        print ("Timeout Error:", url); return False
    except requests.exceptions.RequestException as err:
        print ("Other Errors:", url); return False

    if requests.head(url).status_code == 200:
        return True
    else:
        return False

