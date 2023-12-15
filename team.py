
import requests
from bs4 import BeautifulSoup as soup
import time
import json

def get_page(url):
    cache_path = 'cache_teams.json'
    try:
        with open(cache_path, 'r', encoding='utf-8') as file:
            cache = json.load(file)
    except FileNotFoundError:
        cache = {}

    if url in cache:
        print("Loading from cache")
        page_content = cache[url]
    else:
        print("Fetching from web")
        response = requests.get(url, headers={
            "User-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.6099.71 Safari/537.36"})
        page_content = response.text

        cache[url] = page_content
        with open(cache_path, 'w', encoding='utf-8') as file:
            json.dump(cache, file)

    doc = soup(page_content, "html.parser")
    return doc


def get_tbody(y):
    url = "https://www.formula1.com/en/results.html/"+str(y)+"/team.html"
    doc = get_page(url)
    site_wrapper = doc.find(class_="site-wrapper")
    main = site_wrapper.find(class_="template template-resultsarchive")
    inner_class = main.find(class_="inner-wrap ResultArchiveWrapper")
    result_archive = inner_class.find(class_="ResultArchiveContainer")
    results_archive_wrapper = result_archive.find(
        class_="resultsarchive-wrapper")
    content = results_archive_wrapper.table
    tbody = content.tbody
    return tbody


def get_input():
    year = []
    ipt = input("What year do you want?\nIf multiple, seperate with comma.\n")
    ipt = ipt.split(",")
    if len(ipt) > 1:
        while int(ipt[0]) < 1958 or int(ipt[1]) > 2023:
            ipt = input(
                "No such year. Dates should be given between 1958 and 2023.\n")
            ipt = ipt.split(",")
        for y in range(int(ipt[0]), int(ipt[1])+1):
            year.append(y)
    else:
        while int(ipt[0]) < 1958 or int(ipt[0]) > 2023:
            ipt = input(
                "No such year. Dates should be given between 1958 and 2023.\n")
            ipt = ipt.split(",")
        year.append(int(ipt[0]))
    return year


def get_team_name(tbody):
    list_of_teams = []
    tds = tbody.find_all("a", class_="dark bold uppercase ArchiveLink")
    for td in tds:
        list_of_teams.append(td.text)
    return list_of_teams


def get_points(tbody):
    list_of_points = []
    tds = tbody.find_all("td", class_="dark bold")
    for td in tds:
        list_of_points.append(td.text)
    return list_of_points


def save(path, year, teams, points):
    lines = []
    pos_width = 4
    team_width = max(len(team) for team in teams) + 2
    points_width = 10

    header = f"{'Pos':<{pos_width}} {'Team':<{team_width}} {'Points':>{points_width}}"
    lines.append(header)

    for i, (team, point) in enumerate(zip(teams, points)):
        line = f"{i+1:<{pos_width}} {team:<{team_width}} {point:>{points_width}}"
        lines.append(line)

    with open(path, "a", encoding="utf-8") as f:
        txt = f"{'-'*20} {year} Team Info {'-'*60}\n"
        f.write(txt)

        for line in lines:
            f.write(line + "\n")

    f.close()    


def main():
    year = get_input()
    open("team_info.txt", "w").close()
    for y in year:
        print("Scraping year", y)
        tbody = get_tbody(y)
        team = get_team_name(tbody)
        points = get_points(tbody)
        save("team_info.txt", y,team, points)
        time.sleep(1)
        print("Done")
    print("Please check the results in the file 'team_info.txt'.")

