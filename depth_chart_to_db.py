from depth_chart_scraper import scrape_depth
import psycopg2
from psycopg2 import sql

depth_chart_list = scrape_depth()

DB_HOST = 'ec2-3-227-154-49.compute-1.amazonaws.com'
DB_NAME = 'd60fncflpfafu6'
DB_USER = 'vakfpuyytwxuay'
DB_PASS = '0b7dd7386296b1523f605deac8be346208c987b0d3229db9bccd25f3af07185e'

conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)

cur = conn.cursor()

#cur.execute('CREATE TABLE depth_chart (id VARCHAR PRIMARY KEY, first_name VARCHAR, last_name VARCHAR, position VARCHAR, date DATE, injury_status VARCHAR);')

args = [cur.mogrify('(%s, %s, %s, %s, %s, %s, %s, %s, %s)', i).decode('utf-8')
        for i in depth_chart_list]
args_str = ', '.join(args)
cur.execute('''INSERT INTO depth_chart(id, date, position, first_name, last_name, injury_status, team, increase_rank, position_final) VALUES'''
            + args_str + '''ON CONFLICT(id) DO UPDATE SET
            (date, position, first_name, last_name, injury_status, team, increase_rank, position_final) = (EXCLUDED.date, EXCLUDED.position, EXCLUDED.first_name, EXCLUDED.last_name, EXCLUDED.injury_status, EXCLUDED.team, EXCLUDED.increase_rank, EXCLUDED.position_final)''')

conn.commit()

cur.close()
conn.close()