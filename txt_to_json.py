# Description: This script converts a text file to a json file.
# Developed by: angor.root
import re
import json
import string

archivo = "hymnBook_example" # Cambia por el nombre del archivo que deseas normalizar
text_ar = archivo + ".txt"
json_ar = archivo + ".json"

list_indexs = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X"]
with open(text_ar, 'r', encoding='utf-8') as file:
    list_all = file.readlines()

list_all = [i.strip() for i in list_all]

himnario = []
 
t = 0
coro = False
estrofa = False
n_estrofa = 0
for linea in list_all:
    if re.search(r'\d |#', linea):
        titulo = linea
        # print(titulo)
        numero = int(re.search(r'\d+', linea).group())
        nuevo_himno = None
        nuevo_himno = {
            "title": titulo,
            "number": numero,
            "verses": [""],
            "chorus": ""
        }
        n_estrofa = 0
        if nuevo_himno:
            nuevo_himno["title"] = re.sub(r'\d+|#', '', nuevo_himno["title"]).strip()
            # nuevo_himno["verses"] = [re.sub(r"^\s+|\s+$", "", verse) for verse in nuevo_himno["verses"]]      
            # nuevo_himno["verses"] = [verse for verse in nuevo_himno["verses"] if verse.strip()=='']
            himnario.append(nuevo_himno)
        continue
    al = linea.strip()
    al = al.lower()
    # Remove punctuation from each line
    al = al.translate(str.maketrans("", "", string.punctuation))
    if linea.strip() in list_indexs:
        estrofa = True
        coro = False
    elif al == "coro":
        coro = True
        estrofa = False

    if al == "coro" or coro:
        coro = True
        estrofa = False
        if al == "coro":
            nuevo_himno["chorus"] = ""
        else:
            nuevo_himno["chorus"] += " " + linea
    elif linea in list_indexs or estrofa:
        # n_estrofa = 0
        coro = False
        estrofa = True
        if linea in list_indexs:
            n_estrofa = list_indexs.index(linea)
            nuevo_himno["verses"].append("")
        else: 
            nuevo_himno["verses"][n_estrofa] += " " + linea


with open(json_ar, 'w', encoding='utf-8') as file:
    json.dump(himnario, file, ensure_ascii=False, indent=4)