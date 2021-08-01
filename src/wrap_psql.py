"""Individual wrapper functions for postgresql."""

# %% [Markdown] ======================================================================
# Section 0: imports and credentials
#   (1) package import
#   (2) register data types psycopg2
#   (3) get credentials
# 
# ====================================================================================

# %% (1) package import
import os
from dotenv import load_dotenv
import numpy as np
import pandas as pd
import psycopg2
import psycopg2.extras as extras
from psycopg2.extensions import register_adapter, AsIs
import json

# %% (2) register data types psycopg2
register_adapter(np.float64, lambda a: AsIs(a))
register_adapter(np.int64, lambda a: AsIs(a))
register_adapter(np.bool_, lambda a: AsIs(a))
register_adapter(dict, extras.Json)

# %% (3) get credentials
load_dotenv()
auth = json.loads(os.getenv("database"))

# %% [Markdown] ======================================================================
# section 1: post functions
#   (1) generic writing statement without return
#   (2) upsert writing into table without statement
#
# ====================================================================================

#%% (1) generic statement without return
def post_generic_postgreSQL(statement, auth=auth):
    """Execute a generic sql command.

    Use for create table, create views!

    params
        auch: database connection credentials 
        statement: an sql statet statement
    
    return
        None
    """
    conn = None
    c = None
    try:
        conn = psycopg2.connect(
            database=auth["database"],
            user=auth["user"],
            password=auth["key"],            
            host=auth["host"],
            port=auth["port"]
        )
        c = conn.cursor()
        c.execute(statement)
        conn.commit()
    except psycopg2.Error as e:
        print(e)
    finally:
        if conn:
            conn.close()
        if c:
            c.close()

# %% (2) upsert writing into table without statement
def post_upsert_postgreSQL(table, df, auth=auth, bulk_size = 1000):
    """Insert into a table or update rows (upsert) into table populated by df.
    
    params
        auth: Connection credentials
        table: the table to insert values into
        df: a dataframe to populate the table
        bulk_size: how many commits at a time
    
    return
        None
    """
    # create empty variables for better control
    conn = None
    c = None
    
    # corrective actions for writing
    df = df.replace({np.nan: None})

    # create query
    # ...as opposed to sqlite, one placeholder is enough, no need for exact number
    # ... such as: vals = ", ".join(len(df.columns) * ["%s"])
    cols = ", ".join(list(df.columns))

    # if this is not an f string, double %% required
    insert_sql  = f"""INSERT INTO {table}
        ({cols}) VALUES %s
        ON CONFLICT on constraint {table}_pkey
        DO UPDATE SET ({cols}) = ({', '.join(["EXCLUDED." + x for x in list(df.columns)])})"""

    # write data
    print(f"executing: \n{insert_sql}")
    try:
        conn = psycopg2.connect(
            database=auth["database"],
            user=auth["user"],
            password=auth["key"],            
            host=auth["host"],
            port=auth["port"]
        )
        c = conn.cursor()
        for idx, group in df.groupby(np.arange(len(df))//bulk_size):
            # status
            print(f"executing upsert to {table} num {idx + 1}/{(len(df)//bulk_size) + 1}")        
            # send data and commit
            extras.execute_values(
                c,
                insert_sql, 
                group.to_records(index=False))
            conn.commit()
    except (psycopg2.Error, psycopg2.DatabaseError, ValueError) as e:
        print(e)
        conn.rollback()
    finally:
        if conn:
            conn.close()
        if c:
            c.close()

# %% [Markdown] ======================================================================
# section 2: get / query functions
#   (1) generic statement  with return (GET)
#
# ====================================================================================

# %% (1) generic query statement with return
def get_generic_postgreSQL(statement, auth=auth):
    """Query based on provided statement.
    
    params
        auth: Connection credentials
        statement: query to select data
    
    return
        df : fetched data
    """
    conn = None
    df = None
    try:
        conn = psycopg2.connect(
            database=auth["database"],
            user=auth["user"],
            password=auth["key"],            
            host=auth["host"],
            port=auth["port"]
        )
        df = pd.read_sql_query(statement, conn)
    except psycopg2.Error as e:
        print(e)
    finally:
        if conn:
            conn.close()
    return df