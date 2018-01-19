import sqlite3
DB_PATH = "db.sqlite3"
conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

def get_posts():
    with conn:
    	#cur.execute("INSERT INTO generator_ontologie VALUES ('28','creier','cutia craniana','face parte din')")
    	cur.execute("SELECT * FROM generator_ontologie")
    	colnames = cur.description
    	for row in colnames:
        	print (row[0])
    	print(cur.fetchall())

get_posts()