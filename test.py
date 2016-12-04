# John Moon
# yjmoon

from bs4 import BeautifulSoup

def main():
    

    
    max_url = int(sys.argv[2])
    root = ''
    with open(sys.argv[1], 'r') as INPUTFILE:
        root = INPUTFILE.readlines()[0]

    url_dictionary = set()
    url_dictionary.add(root)
    count = 0
    while count < max_url and queue:
        url = queue.popleft()
        base = url
        r = requests.get(url)
        soup = BeautifulSoup(r.text, "html.parser")
        for url in soup.find_all('a'):
            if count == 2000:
                break
            url = url.get("href")
            if url:
                url = normalize(url, root) 
                if url != False:
                    if "eecs.umich.edu" in url and url not in url_dictionary:
                        queue.append(url)
                        url_dictionary.add(url)
                        count += 1
                        print base.encode("utf-8"), url.encode("utf-8")
                        # print url.encode("utf-8")
    return

def normalize(url, base):
    if url == '':
        return False
    if url == '/':
        return False
    if ".php" in url or ".cgi" in url or ".pdf" in url or ".jpg" in url or ".eps" in url or ".bib" in url or ".tgz" in url or ".zip" in url:
        return False
    if ".jpeg" in url or ".png" in url or ".txt" in url or ".gz" in url or "javascript:" in url or ".ppt" in url or ".doc" in url:
        return False
    if "mailto:" in url:
        return False
    if "http://www.google.com/calendar" in url:
        return False
    if "index.html" in url:
        url = url.replace("index.html", "")
    if url:
        if url[-1] == '/':
            url = url[:-1]
    if "https" in url:
        url = "http" + url[5:]
    if '#' in url:
        url = url[:url.find('#')]
    if url[:4] != "http":
        if url:
            if url[0] != '/' and base[-1] != '/':
                url = base + '/' + url
            elif url[:2] == "..":
                k = url.rfind("/")
                url = base[:k] + url

            else:
                url = base + url
    return url


if __name__ == '__main__':
    main()