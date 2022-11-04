from lxml.html import fromstring

import datetime
import requests
import json
import os


class NewsCrawler:
    def __init__(self, categories, _directory, _links_xpath, _title_xpath, _body_xpath, _time_xpath, _author_xpath, _number_of_page, _url):
        self.title_xpath = _title_xpath
        self.body_xpath = _body_xpath
        self.time_xpath = _time_xpath
        self.author_xpath = _author_xpath
        self.number_of_page = _number_of_page
        self.directory = _directory
        self.categories = categories
        self.links_xpath = _links_xpath
        self.url = _url

    def crawl_page(self, link, f):
        req = requests.get(link)
        tree = fromstring(req.text)
        title = "".join(tree.xpath(self.title_xpath))
        body = "".join(tree.xpath(self.body_xpath))
        author = "".join(tree.xpath(self.author_xpath))
        time = "".join(tree.xpath(self.time_xpath))
        time_fix = self.date_convert(time,'%d/%m/%Y %H:%M')
        title_save = "".join(filter(str.isalnum, title))

        os.makedirs(self.directory + f, mode=0o777, exist_ok=True)
        try:
            with open(self.directory + f + "/" + title_save + ".txt", "w", encoding="utf-8") as my_file:
                my_file.write("\t\t" + title + "\n\n")
                my_file.write("\t\t\t\t\t\t" + time_fix + "\n\n\n")
                my_file.write("\t" + body + "\n")
                my_file.write("\t\t\t\t\t\t" + author + "\n\n\n")
        except:
            pass
        
    def get_links(self, u, file):
        for x in range(1,(self.number_of_page + 1)): 
            links = u
            req = requests.get(links)
            tree = fromstring(req.text)
            xpath_links = tree.xpath(self.links_xpath)
            xpath_links = sorted(set(xpath_links), key=xpath_links.index)  
            for each_link in xpath_links:
                url_each_link = self.url + each_link
                self.crawl_page(url_each_link, file)
                
    def date_convert(self, date_str, date_form):
        if "(GMT+7)" in date_str:
            tt = list(date_str)
            t = tt[-24:-8]
            tn = "".join(t)
            try:
                dat = datetime.datetime.strptime(tn,'%d/%m/%Y %H:%M')
                date = datetime.datetime.strftime(dat, date_form)
                return date
            except ValueError:
                pass        
            
        if "-" in date_str:
            tt = list(date_str)
            t = tt[-18:]
            tn = "".join(t)
            try:
                dat = datetime.datetime.strptime(tn,'%d/%m/%Y - %H:%M')
                date = datetime.datetime.strftime(dat, date_form)
                return date
            except ValueError:
                pass
            
        if ("CH" in date_str) or ("SA" in date_str):
            tt = list(date_str)
            t = tt[-19:-3]
            tn = "".join(t)
            try:
                dat = datetime.datetime.strptime(tn,'%d/%m/%Y %H:%M')
                date = datetime.datetime.strftime(dat, date_form)  
                return date
            except ValueError:
                pass

    def _run_crawler(self):
        """Sau khi hoàn thiện xong hết tất cả các hàm
         rồi thì hãy gọi tất cả các hàm ở đây rồi chạy."""
        for cate in self.categories:
            
            if "baophuyen" in cate:
                ct = cate[20:-13].replace("/","_")
                self.get_links(cate, ct)

            elif "dantri" in cate:
                ct = cate[22:-13].replace("/","_")
                self.get_links(cate, ct)
            
            else:
                ct = cate[20:-5].replace("/","_")
                self.get_links(cate, ct)
        
if __name__ == '__main__':
    file = "E:/pthon/PycharmProjects/craw/class/"
    for each_file in os.listdir(file):
        if ".json" in each_file:
            with open(file + each_file, "r", encoding = "utf-8") as json_file:
                data = json.loads(json_file.read())
                my_crawler = NewsCrawler(categories=data.get("categories"),
                                        _directory=data.get("directory"),
                                        _links_xpath=data.get("xpath_links"),
                                        _url=data.get("url"),
                                        _title_xpath=data.get("xpath_title"),
                                        _body_xpath=data.get("xpath_body"),
                                        _time_xpath=data.get("xpath_time"),
                                        _author_xpath=data.get("xpath_author"),
                                        _number_of_page=data.get("number_of_page")
                                        )
                my_crawler._run_crawler()