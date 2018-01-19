from owlready2 import *
import sqlite3
import os 

dir_path = os.path.dirname(os.path.realpath(__file__))
DB_PATH = "chestionar\\db.sqlite3"

onto = onto_path.append(dir_path)
onto = get_ontology("http://www.students.info.uaic.ro/~ionut.trofin/iai2.owl").load()

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

def insert(termen,parinte,relatie):
    with conn:
        cur.execute("SELECT MAX(id) FROM generator_ontologie")
        id = cur.fetchall()[0][0]
        if id is None:
            id = 0
        cur.execute("INSERT INTO generator_ontologie VALUES ('"+str(id+1)+"','"+termen+"','"+parinte+"','"+relatie+"')")

def convert(fraza):
	fraza = str(fraza)[5:]
	if '_' not in fraza:	
		ok = 0
		for index,char in enumerate(fraza):
			if char.isupper() and index != 0:
				fraza = fraza[:index+ok]+' '+fraza[index+ok:]
				ok += 1
		return fraza.lower()
	else:
		return fraza.replace('_',' ').lower()

for item in list(onto.properties()):
	for i in range(0,len(item.domain)):
		termen,parinte,relatie = convert(item.domain[i]),convert(item.range[i]), convert(item)
		insert(termen,parinte,relatie)

		print (termen,relatie,parinte)
conn.commit()
conn.close()