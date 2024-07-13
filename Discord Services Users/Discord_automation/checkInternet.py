import requests
def check_internet_connection():
    try:
        response = requests.get("https://www.google.com")
        if 200<=response.status_code<=299:
            return True
        else:
            False
    except:
        return False