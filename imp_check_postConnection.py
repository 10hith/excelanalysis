import psycopg2
con = psycopg2.connect(database="mydb", user="basal", password="#7804c11bN", host="127.0.0.1", port="5432")
cur = con.cursor()
cur.execute("select version();")
print(cur.fetchone())