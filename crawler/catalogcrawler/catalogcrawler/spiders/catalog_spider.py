import scrapy
import re
from ..items import CatalogcrawlerItem

def append_num(L, num):
    for i in range(len(L)):
        print(type(L[i]))
        print(L)
        L[i] += '+' + str(num)
    return L

class CatalogSpider(scrapy.Spider):
    name = "AUC Catalog"
    start_urls = [
        "http://catalog.aucegypt.edu/content.php?filter%5B27%5D=-1&filter%5B29%5D=&filter%5Bcourse_type%5D=-1&filter%5Bkeyword%5D=&filter%5B32%5D=1&filter%5Bcpage%5D=1&cur_cat_oid=36&expand=1&navoid=1738&print=1#acalog_template_course_filter"
    ]

    def parse(self, response, **kwargs):
        items = CatalogcrawlerItem()
        all_courses = response.css("td.width li")
        for course in all_courses:
            course_title = course.css("li h3::text").extract()
            descrip = course.css("li::text, strong::text, a::text, li p::text, li span:nth-child(15)::text, "
                                 "li span:nth-child(14)::text, li span:nth-child(8)::text, li span::text").extract()

            if(course_title != [""] and course_title != []):
                cr_pattern = re.compile(r"(\d-?\d?)\s?(cr|credits)+")
                dept_pattern = re.compile(r"^[A-Z][A-Z]+")
                course_pattern = re.compile(r"\d{4}")
                coursename_pattern = re.compile(r"(?<=-\s).+(?=\d)")
                coursename_pattern_nocre = re.compile(r"(?<=-\s).+")
                coursename_pattern1 = re.compile(r"[A-Z].*\w")
                credits = cr_pattern.findall(course_title[0])
                creditsN = 0
                for credit in credits:
                    creditsN = creditsN + int(credit[0][0])
                dept_code = dept_pattern.findall(course_title[0])
                course_num = course_pattern.findall(course_title[0])
                if (credits == []):
                    course_name = coursename_pattern_nocre.findall(course_title[0])
                else:
                    course_name = coursename_pattern.findall(course_title[0])
                    if (len(credits[0][0]) > 1):
                        course_name = re.findall(r".+(?=\s\()", course_name[0])
                if (course_name != []):
                    course_name = coursename_pattern1.findall(course_name[0])

                prerq = ""
                desc = ""
                cross = ""
                wnofferd = ""
                notes = ""
                listX = ["Prerequisites", "Description", "Cross-listed", "Hours", "When Offered", "Notes", "Repeatable"]
                choose = ''
                for i in range(len(descrip)):
                    if descrip[i] in listX:
                        choose = descrip[i][0]
                    else:
                        if choose is 'P':
                            prerq += descrip[i]
                        elif choose is 'D':
                            desc += descrip[i]
                        elif choose is 'C':
                            cross += descrip[i]
                        elif choose is 'W':
                            wnofferd += descrip[i]
                        elif choose is 'N':
                            notes += descrip[i]

                prerq_pattern = re.compile(r"(([A-Z]{3}|[A-Z]{4})\s(\d{3}/\d{4}|\d{4})?)")

                # PROCESSING THE PREREQUISITES AND CONCURRENCY
                prerqs = [y[0] for y in prerq_pattern.findall(prerq)]
                for i, prerqs_item in enumerate(prerqs):
                    if '/' in prerqs_item:
                        str = prerqs_item.split('/')
                        dCode = re.findall(r"[A-Z]{3}[A-Z]?", str[0])
                        newlist = [dCode[0], str[1]]
                        prerqs[i] = " ".join(newlist)
                if (prerqs != []) and (("APLN 5021" in cross[0])): #this is an exception (some crosslisting refers to non-existing courses)
                    del prerqs[0]
                print(prerq)
                print(prerqs)
                if 'concurrent' in prerq:
                    prerqs[-1] += '+1'
                    prerqs[:-1] = append_num(prerqs[:-1], 0)
                else:
                    prerqs = append_num(prerqs, 0)
                prerq = prerqs

                #PROCESSING THE REST
                cross = re.findall(r"[A-Z][A-Z0-9/]+\s\d{4}", cross) # (11) was [A-Z][A-Z0-9/]+\s\d{4} before
                for i, cross_item in enumerate(cross):
                    if ('/' in cross_item):
                        str = cross_item.split('/')
                        dCode = re.findall(r"\d{3}\d?", str[1])
                        newlist = [str[0], dCode[0]]
                        cross[i] = " ".join(newlist)
                if (cross != []) and (("TAFL" in cross[0]) or ("LING 4211" in cross[0])): #this is an exception (some crosslisting refers to non-existing courses)
                    del cross[0]
                wnoff_pat = re.compile(r"(fall|winter|spring|summer|occasional)", re.IGNORECASE) #(11) edited
                wnofferd = wnoff_pat.findall(wnofferd)
                desc = re.findall(r"\w.+\.", desc) #(11)in trial, remove dot and add word if fails
                notes = re.findall(r"\w.+\.", notes)
                yield {
                    "dept_code": dept_code,
                    "course_num": course_num[0],
                    "course_name": course_name,
                    "credit": creditsN,
                    "descrip": desc,
                    "when_offered": wnofferd,
                    "Crosslisted": cross,
                    "Prerequisites": prerq,
                    "notes": notes
                }

        next_page = response.css("td > span+a::attr(href)").get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)