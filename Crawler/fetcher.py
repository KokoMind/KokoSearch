import urllib.request
from bs4 import BeautifulSoup
import re
import requests


class Fetcher:
    """Class that will fetch the page, validate that it is of type HTML, extract its contents and hyperlinks"""

    @staticmethod
    def fetch(url):
        code, page = Fetcher._download_page(url)
        if code == -1:
            return code, None, None
        soup = BeautifulSoup(page, 'html.parser')
        content = Fetcher._extract_content(soup, page)
        links = Fetcher._extract_links(soup, page)
        return code, links, content

    @staticmethod
    def _download_page(url):
        """returns data,code. For code, 0 means success and -1 means failure."""
        if Fetcher._check_url(url):
            with urllib.request.urlopen(url) as response:
                data = response.read().decode('utf-8', 'ignore')
                return 0, data
        else:
            return -1, None

    @staticmethod
    def _extract_content(soup, page):
        """Extract page contents (text for indexing)"""
        # kill all script and style elements
        for script in soup(["script", "style"]):
            script.decompose()  # rip it out

        # get text
        text = soup.get_text()
        # break into lines and remove leading and trailing space on each
        lines = (line.strip() for line in text.splitlines())
        # break multi-headlines into a line each
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        # drop blank lines
        text = '\n'.join(chunk for chunk in chunks if chunk)
        return text

    @staticmethod
    def _check_url(url):
        """Checks that URL is alive and of type html."""
        connection_lost = True
        while connection_lost:
            try:
                response = requests.get(url)
                if response.status_code == 200:  # OK
                    content_type = response.headers['content-type']
                    if content_type.find('html') != -1:
                        return True
                    return False
                else:
                    return False
            except:
                print("\rConnection lost. Retry!", end="")

    @staticmethod
    def _extract_links(soup, page):
        links = re.findall('"((http)s?://.*?)"', page)
        links = [url for url, _ in links]
        #To be done  ----> url_normalizer.
        return links

# Test Driver code :D
# code,links,content = Fetcher.fetch("http://www.adobe.com/")
# print(code, links)
