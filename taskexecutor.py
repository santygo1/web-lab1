import sqlite3 as database
import pandas as pd

# pandas settings
pd.set_option('display.width', 1000)

def execute(query):
    con = database.connect('./library.sqlite')
    result = pd.read_sql(query, con)
    print(result)
