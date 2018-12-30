# -*- coding: utf-8 -*-
import csv
import re
from time import sleep

import requests
from bs4 import BeautifulSoup

page = 256
peom_id = 0
peot_id = 0

if __name__ == "__main__":
    # __init__
    with open('d://link.csv', 'a', newline='') as csv_file:
        csv.writer(csv_file).writerow(["peom_id", "peot_id"])
    with open('d://peoms.csv', 'a', newline='') as csv_file:
        csv.writer(csv_file).writerow(["peom_id", "peom"])
    with open('d://peots.csv', 'a', newline='') as csv_file:
        csv.writer(csv_file).writerow(["peot_id", "peot"])
    for tt in range(page):
        tt += 1
        rep = requests.get("https://so.gushiwen.org/authors/default.aspx?p="+str(page)+"&c=%E5%94%90%E4%BB%A3")
        soup = BeautifulSoup(rep.text, "lxml")
        for item in soup.find_all(class_="cont"):
            if item.find(style=" margin:0px;") is not None:
                # 诗人页
                peot_id += 1
                peom = item.find(style="font-size:18px; line-height:22px; height:22px;").find("b").string
                with open('d://peots.csv', 'a', newline='') as csv_file:
                    csv.writer(csv_file).writerow([peot_id, peom])
                peot_url = "https://so.gushiwen.org" + item.find(style=" margin:0px;").find("a").attrs["href"]
                peot_re = requests.get(peot_url)
                peot_soup = BeautifulSoup(peot_re.text, "lxml")
                # 诗人有多少页诗
                try:
                    peot_pages_num = re.search(r'\d+', peot_soup.find(
                        style=" background-color:#E1E0C7; border:0px; margin-top:22px; width:auto;").string).group()
                except:
                    pass
                peoms_url_raw = re.sub(r"A1.aspx$", "", peot_url)
                for peot_page in range(int(peot_pages_num)):
                    # 诗人所属诗的一页
                    peot_page += 1
                    sleep(2)
                    final_rep = requests.get(peoms_url_raw + "A" + str(peot_page) + ".aspx")
                    final_soup = BeautifulSoup(final_rep.text, "lxml")
                    for final_item in final_soup.find_all(class_="cont"):
                        if final_item.find("b") is not None:
                            peot = final_item.find("b").string
                            if (peot != peom):
                                peom_id += 1
                                with open('d://peoms.csv', 'a', newline='') as csv_file:
                                    csv.writer(csv_file).writerow([peom_id, peot])
                                with open('d://link.csv', 'a', newline='') as csv_file:
                                    csv.writer(csv_file).writerow([peot_id, peom_id])




