import json
f = open("g.json")
raum = json.loads(f.read())

def koord_def(raum) :
    i = 0
    k = 0
    raum["links"] = []
    for word in raum["nodes"]:
        j = 0
        for word1 in raum["nodes"]:
            if i == j :
                continue
            if  not word.__contains__("desc"):
                print(word)
                word["desc"] = "Sample text"
            if  not word1.__contains__("desc"):
                word1["desc"] = "Sample text"
            if word1["name"] in word["desc"]:
                er = {}
                er["value"] = 1
                er["source"] = i
                er["target"] = j
                raum["links"].append(er)
                k += 1
            j += 1
        i += 1
    print(raum)
    with open('g.json', 'w') as outfile:
        json.dump(raum, outfile)
