import link
import vizualise
import json

f = open("g.json")
raum = json.loads(f.read())
link.koord_def(raum)
vizualise.vizualise()