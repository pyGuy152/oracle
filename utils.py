from psycopg2 import Error
from psycopg2.extras import RealDictCursor
import time, psycopg2, requests, time, os
from dotenv import load_dotenv

load_dotenv()
db_user = os.getenv("DB_User")
db_pass = os.getenv("DB_User_PASS")

# AI
def askAI(prompt):
    headers = {"Content-Type":"application/json"}
    data = {'messages':[{"role": "user", "content": prompt}]}
    response = requests.post("https://ai.hackclub.com/chat/completions",headers=headers,json=data)
    response.raise_for_status()
    output = response.json()
    return output['choices'][0]['message']['content']

# methord for sql queries 
def sqlQuery(sql: str, params: tuple, fetchALL: bool = False, fetchNone: bool = False):
    while True:
        try:
            conn = psycopg2.connect(database='oracle',user=db_user,password=db_pass,host='localhost',port='5432',cursor_factory=RealDictCursor)
            cur = conn.cursor()
            break
        except Error as e:
            if conn:
                conn.close()
            print(f"Error connecting to DB: {e}")
            time.sleep(5)
    cur.execute(sql,params)
    try:
        if fetchALL:
            out = cur.fetchall()
        elif fetchNone:
            out = None
        else:
            out = cur.fetchone()
    except Exception as e:
        print(e)
        raise 'ERROR: SQL query problem'
    conn.commit()
    conn.close()
    return out