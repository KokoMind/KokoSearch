import urllib.request
from bs4 import BeautifulSoup
import re
import requests
from url_normalize import url_normalize
import urllib.parse
from os.path import splitext
import socket


class Fetcher:
    """Class that will fetch the page, validate that it is of type HTML, extract its contents and hyperlinks"""

    @staticmethod
    def fetch(url):
        code, page = Fetcher._download_page(url)
        if code == -1:
            return code, None, None

        soup = BeautifulSoup(page, 'lxml')
        content = Fetcher._extract_content(soup, page)
        links = Fetcher._extract_links(soup, page)
        return code, links, content

    @staticmethod
    def _download_page(url):
        """returns data,code. For code, 0 means success and -1 means failure."""
        if Fetcher._check_url(url):
            try:
                with urllib.request.urlopen(url) as response:
                    data = response.read().decode('utf-8', 'ignore')
                    return 0, data
            except:
                return -1, None
        else:
            return -1, None

    @staticmethod
    def _extract_content(soup, page):
        """Extract page contents (text for indexing)"""
        # kill all script and style elements
        for script in soup(["script", "style"]):
            script.decompose()  # rip it out

        # get text
        text = soup.get_text(' ')
        # break into lines and remove leading and trailing space on each
        lines = (line.strip() for line in text.splitlines())
        # break multi-headlines into a line each
        chunks = (phrase.strip() for line in lines for phrase in line.split(" "))
        # drop blank lines
        text = ' '.join(chunk for chunk in chunks if chunk)
        return text

    @staticmethod
    def _check_url(url):
        """Checks that URL is alive and of has a response of type html."""
        while True:
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
                if Fetcher._internet_on():
                    return False
                print("\rConnection lost. Retry!!", end="")

    @staticmethod
    def _extract_links(soup, page):
        """Extract links from a webpage and normalize those links. Returns a list of (link,dns) tuple."""
        extracted_links = re.findall('"((http)s?://.*?)"', page)
        extracted_links = [url for url, _ in extracted_links]

        links = []
        for i in range(len(extracted_links)):
            # Normalize the url link by converting it to canonical form.
            # For more info, refer to https://pypi.python.org/pypi/urlnorm
            extracted_links[i] = url_normalize(extracted_links[i])
            extracted_links[i] = extracted_links[i].replace("%3A", ":")  # Restore the ":" character back.
            if Fetcher._check_ext_html(extracted_links[i]):
                links.append((extracted_links[i], Fetcher.extract_dns(extracted_links[i])))
        return links

    @staticmethod
    def _internet_on():
        for timeout in [1, 5]:
            try:
                response = urllib.request.urlopen('http://www.google.com', timeout=timeout)
                return True
            except urllib.request.URLError as err:
                pass
        return False

    @staticmethod
    def _check_ext_html(url):
        """check the filename extension either HTML or ''."""
        parsed = urllib.parse.urlparse(url)
        root, ext = splitext(parsed.path)
        target = {'.htm', '.html', '.php', '.aspx', ''}
        if ext in target:
            return True
        return False

    @staticmethod
    def extract_dns(url):
        try:
            parsed = urllib.parse.urlparse(url)
            return socket.gethostbyname(parsed.hostname)
        except:
            return None

            # Test Driver code :D

# For testing
# code,links,content = Fetcher.fetch('https://wikimediafoundation.org/')
# print(code, content)
