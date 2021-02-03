import scrapy
import re
from ..items import CatalogcrawlerItem, deptItem

names_global = []


class deptSpider(scrapy.Spider):
    name = "DepartmentNames"
    start_urls = [
        "http://catalog.aucegypt.edu/content.php?catoid=36&navoid=1738"
        #"http://catalog.aucegypt.edu/content.php?filter%5B27%5D=-1&filter%5B29%5D=&filter%5Bcourse_type%5D=-1&filter%5Bkeyword%5D=&filter%5B32%5D=1&filter%5Bcpage%5D=1&cur_cat_oid=36&expand=1&navoid=1738&print=1#acalog_template_course_filter"
    ]

    def parse(self, response, **kwargs):
        items = deptItem()
        apprs = response.css("br+ p strong::text").extract()
        is_code = True
        names = []
        listX = ["Prerequisites", "Description", "Cross-listed", "Hours", "When Offered", "Notes", "Repeatable"]
        for appr in apprs:
            #items = re.findall(r"\w.*\w", appr)
            if appr not in listX:
                if (appr not in names_global) and ('-' not in appr):
                    print(appr)
                    print(names)
                    names.append(appr)
                    names_global.append(appr)
        for name in names:
            yield {
                "name": name
            }

        next_page = response.css("td > span+a::attr(href)").get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)