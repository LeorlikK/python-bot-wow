import time

url = "https://www.wowhead.com/object=375363/mawsworn-supply-chest"
res = requests.get(url=url).text
with open("pars.html", "w", encoding="utf-8") as file:
    file.write(res)


m = []
with open("pars.html", "r", encoding="utf-8") as file:
    for x in file:
        x.strip()
        x = x.replace(",", " ")
        x = x.replace("[", "")
        x = x.replace("]", "")
        m.append(x + "\n")
print(m)
with open("save_coordinates.txt", "w", encoding="utf-8") as file1:
    for x in m:
        file1.write(x)