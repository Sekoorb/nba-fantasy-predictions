from depth_chart_scraper import scrape_depth
import psycopg2
from psycopg2 import sql

depth_chart_list = scrape_depth()

DB_HOST = 'ec2-35-170-146-54.compute-1.amazonaws.com'
DB_NAME = 'd7ef58eh3ocdtm'
DB_USER = 'iqsbkgeldxxkid'
DB_PASS = '021b264660631a9b7a4ce60b6a9ae431a7fd67f459d106ac81c6211b8a6d77ce'

conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)

cur = conn.cursor()

args = [cur.mogrify('(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', i).decode('utf-8') for i in depth_chart_list]
args_str = ', '.join(args)

cur.execute('''INSERT INTO depth_chart(id, date, position, first_name, last_name, injury, team, position_rank, position_type, position_rank_increase, position_rank_final, position_final) VALUES'''
            + args_str + '''ON CONFLICT(id) DO UPDATE SET
            (date, position, first_name, last_name, injury, team, position_rank, position_type, position_rank_increase, position_rank_final, position_final) = 
            (EXCLUDED.date, EXCLUDED.position, EXCLUDED.first_name, EXCLUDED.last_name, EXCLUDED.injury, 
            EXCLUDED.team, EXCLUDED.position_rank, EXCLUDED.position_type, EXCLUDED.position_rank_increase, EXCLUDED.position_rank_final, EXCLUDED.position_final)''')

conn.commit()

cur.close()
conn.close()