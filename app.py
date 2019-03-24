
import thread
import time
import psutil
import sqlite3
import json
from flask import Flask
from flask import render_template

server = Flask(__name__)


initial_sql = """CREATE TABLE IF NOT EXISTS log(
                    TimeStamp INTEGER,
                    cpu_percent FLOAT
               )"""

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    try:
        conn = sqlite3.connect(db_file,timeout=1)
        return conn
    except Exception as e:
        print(e)
 
    return None

def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        conn.execute(create_table_sql)
        conn.commit()
    except Exception as e:
        print(e)

def create_item(conn, item):
    """
    Create a new task
    :param conn:
    :param task:
    :return:
    """
    conn.execute("INSERT INTO log(TimeStamp,cpu_percent) VALUES(%d,%s)" % ( int(time.time()),item))
    conn.commit()
    
def processthread( foo, foo2 ):
        try:
                conn = create_connection("log.db")
                if conn is not None:
                        # create projects table
                        print("create table")
                        create_table(conn, initial_sql)
                        while True:
                                time.sleep(5)
                                cursor = conn.cursor()
                                percent = psutil.cpu_percent()
                                sql = "INSERT INTO log(TimeStamp,cpu_percent) VALUES(%d,%s)" % (int(time.time()),percent)
                                cursor.execute(sql)
                                conn.commit() 
                                print(sql)
        except (KeyboardInterrupt, SystemExit):
                conn.close()



@server.route('/getjson')
def getjson():
    conn = create_connection("log.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM  log ORDER BY TimeStamp DESC LIMIT 1;")
    rows = cur.fetchall()
    print(rows)
    return json.dumps(rows)
    return render_template('index.html', rows=rows)
    

@server.route('/')
def hello():
    conn = create_connection("log.db")
    cur = conn.cursor()
    cur.execute("SELECT TimeStamp,cpu_percent FROM log")
    rows = cur.fetchall()
    return render_template('index.html', rows=rows)
    #return "Hello World!"

       
if __name__ == '__main__':
    thread.start_new_thread(processthread,(None,None))
    server.run(debug=True)