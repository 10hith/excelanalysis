import psycopg2
con = psycopg2.connect(database="postgres", user="postgres", password="example123", host="127.0.0.1", port="5432")
cur = con.cursor()
cur.execute("select current_date;")
print(cur.fetchone())