import requests
from bs4 import BeautifulSoup as soup
import time
import json

def get_page(url):
    cache_path = 'cache_drivers.json'
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



def get_data(doc):
    site_wrapper = doc.find(class_="site-wrapper")
    main = site_wrapper.find(class_="template template-resultsarchive")
    inner_class = main.find(class_="inner-wrap ResultArchiveWrapper")
    result_archive = inner_class.find(class_="ResultArchiveContainer")
    results_archive_wrapper = result_archive.find(
        class_="resultsarchive-wrapper")
    content = results_archive_wrapper.table
    tbody = content.tbody
    return tbody


def get_driver_name(tbody):
    drivers_this_season = []
    tds_for_names = tbody.find_all("a", class_="dark bold ArchiveLink")
    for td_for_names in tds_for_names:
        names = td_for_names.find_all(
            True, {"class": ["hide-for-tablet", "hide-for-mobile"]})
        name = names[0].text + " " + names[1].text
        drivers_this_season.append(name)
        #print("Name:", name)
    return drivers_this_season


def get_driver_point(tbody):
    points_this_season = []
    tds_for_points = tbody.find_all("td", class_="dark bold")
    for td_for_points in tds_for_points:
        point = td_for_points.string
        points_this_season.append(point)
        #print("PTS:", point)
    return points_this_season


def get_team_name(tbody):
    teams_this_season = []
    tds_for_teams = tbody.find_all(
        "a", class_="grey semi-bold uppercase ArchiveLink")
    for td_for_teams in tds_for_teams:
        team = td_for_teams.string
        teams_this_season.append(team)
        #print("Team:", team)
    return teams_this_season


def save(path, year, names, points, teams):
    lines = []
    for i in range(len(names)):
        appendLine = (str(i+1) + "-" + names[i] + " "*(25-len(names[i])) +
                      points[i] + " "*(10-len(points[i])) + teams[i])
        lines.append(appendLine)
    with open(path, "a", encoding="utf-8") as f:
        txt = "-"*20 + str(year) + " Driver Standings" + "-"*60 + "\n"
        f.write(txt)
        for line in lines:
            f.write(line)
            f.write("\n")
    f.close()


def save_for_sql(path, year, names, points, teams):
    lines = []
    lines.append(str(year))
    for i in range(len(names)):
        appendLine = names[i] + "," + points[i] + "," + teams[i]
        lines.append(appendLine)
    with open(path, "a", encoding="utf-8") as f:
        for line in lines:
            f.write(line)
            f.write("\n")
    f.close()


def get_input():
    year = []
    ipt = input("What year do you want?\nIf multiple, seperate with comma.\n")
    ipt = ipt.split(",")
    if len(ipt) > 1:
        while int(ipt[0]) < 1950 or int(ipt[1]) > 2023:
            ipt = input(
                "No such year. Dates should be given between 1950 and 2023.\n")
            ipt = ipt.split(",")
        for y in range(int(ipt[0]), int(ipt[1])+1):
            year.append(y)
    else:
        while int(ipt[0]) < 1950 or int(ipt[0]) > 2023:
            ipt = input(
                "No such year. Dates should be given between 1950 and 2023.\n")
            ipt = ipt.split(",")
        year.append(int(ipt[0]))
    return year


dict_person = {}
dict_team = {}


def update_dict(name, team, point, flag):
    global dict_team, dict_name
    if flag == 0:
        for i in range(len(name)):
            key = name[i]
            if key in dict_person:
                dict_person[key] += float(point[i])
            else:
                dict_person[key] = float(point[i])
    else:
        for i in range(len(team)):
            key = team[i]
            if key in dict_team:
                dict_team[key] += float(point[i])
            else:
                dict_team[key] = float(point[i])


def save_dict(path, dict, flag):
    if flag == 1:
        sorted_dict = sorted(dict.items(), key=lambda x: x[0], reverse=False)
    else:
        sorted_dict = sorted(dict.items(), key=lambda x: x[1], reverse=True)
    
    key_width = max(len(str(key)) for key in dict.keys()) + 2
    value_width = max(len(str(value)) for value in dict.values()) + 2

    with open(path, "a", encoding="utf-8") as output:
        header = f"{'-'*24} Total points collected by drivers/teams during this period {'-'*30}\n"
        output.write(header)
        for key, value in sorted_dict:
            line = f"{key:<{key_width}} {value:>{value_width}}\n"
            output.write(line)



def main():
    global dict_team, dict_person
    open("year_data.txt", "w").close()
    #open("sqlData.txt", "w").close()
    year = get_input()
    len_year = len(year)
    for y in year:
        print("Scraping year", y)
        url = "https://www.formula1.com/en/results.html/" + str(y)+"/drivers.html"
        doc = get_page(url)
        tbody = get_data(doc)
        name = get_driver_name(tbody)
        point = get_driver_point(tbody)
        team = get_team_name(tbody)
        save("year_data.txt", y, name, point, team)
        update_dict(None, team, point, 1)
        save_for_sql("sqlData.txt", y, name, point, team)
        if len_year > 1:
            update_dict(name, None, point, 0)
        time.sleep(1)
    if len_year > 1:
        save_dict("year_data.txt", dict_person, 0)
    save_dict("year_data.txt", dict_team, 1)
    print("Process Finished Successfully")
    print("Please check the results in the file 'year_data.txt'.")

main()
