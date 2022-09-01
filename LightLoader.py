from rich.console import Console
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup

import random
import string
import os
import threading
import requests
import time


# - Output folder name.
DIRNAME = "Output"
DLCOUNT = 0
ERCOUNT = 0
LENGTH = 6

console = Console()


class LightLoader(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        with console.status("[bold green]Scraping data...") as status:
            while True:
                fileName = self.generateId(LENGTH)
                url = self.generateLink(fileName)
                self.generateImgur(url, fileName)
                fmt_filename = ''.join((fileName, '.png'))
                console.log(f"[green]Finish scraping data[/green] {fmt_filename}")

    # - Generates lightshot link using generateId() function
    def generateLink(self, fileName):
        return "https://prnt.sc/" + fileName


    # - Generates random string
    def generateId(self, size):
        return ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(size))


    # - Downloads HTML File from link previously generated
    def generateHtml(self, fileName):
        url = self.generateLink(fileName)
        request = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        page = urlopen(request).read()
  
        return page


    # - Looks for raw image link in HTML File
    def generateImgur(self, url, fileName):
        soup = BeautifulSoup(self.generateHtml(fileName), 'html.parser')
        imgUrl = soup.find('img', id='screenshot-image')['src']
        
        # - Prevents "Error Image" From being downloaded
        if imgUrl != '//st.prntscr.com/2018/06/19/0614/img/0_173a7b_211be8ff.png':
            imgUrl = imgUrl.replace('//st.', 'http://st.') if imgUrl.startswith('//st.') else imgUrl
            
            resp = requests.get(imgUrl, headers={'User-Agent': 'Mozilla/5.0'}).content
            try:
                soup1 = BeautifulSoup(resp, 'html.parser').find('title').text
            except Exception as e:
                global DLCOUNT
                DLCOUNT += 1
                
                archive_path = DIRNAME + "/" + fileName + ".png"
                log_path = DIRNAME + "/" + fileName + ".txt"

                with open(archive_path, 'wb') as f:
                    f.write(resp)
    
                console.log(f"[blue]Total Downloads:[/blue] {DLCOUNT}")

        else:
            global ERCOUNT
            ERCOUNT += 1


def main():
    # - Creates "Output" folder if not present
    if not os.path.exists(DIRNAME):
        os.makedirs(DIRNAME)
        
    # threads_count = int(input("Input number of threads to be used: "))
    threads_count = 5
    for t in range(threads_count):
        thread = LightLoader()
        thread.start()
        thread.join()
        time.sleep(0.25)
    


if __name__ == '__main__':
    main()
    console.log(f'[bold][red]Done!')
    input()
    quit()
