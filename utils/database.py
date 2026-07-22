import sqlite3
import pandas as pd
import os

# =====================================================
# Database Configuration
# =====================================================

DATABASE_FOLDER = "database"
DATABASE_NAME = "business.db"
DATABASE_PATH = os.path.join(DATABASE_FOLDER, DATABASE_NAME)


# =====================================================
# Create Database Folder
# =====================================================

if not os.path.exists(DATABASE_FOLDER):
    os.makedirs(DATABASE_FOLDER)


# =====================================================
# Get Connection
# =====================================================

def get_connection():

    return sqlite3.connect(DATABASE_PATH)


# =====================================================
# Save Dataset
# =====================================================

def save_to_database(df: pd.DataFrame, table_name="sales"):

    conn = get_connection()

    try:

        df.to_sql(

            table_name,

            conn,

            if_exists="replace",

            index=False

        )

        conn.commit()

    finally:

        conn.close()


# =====================================================
# Execute SQL Query
# =====================================================

def execute_sql(sql_query):

    conn = get_connection()

    try:

        result = pd.read_sql_query(

            sql_query,

            conn

        )

        return result

    except Exception as e:

        raise Exception(f"SQL Error:\n\n{e}")

    finally:

        conn.close()


# =====================================================
# Get Column Names
# =====================================================

def get_columns(table_name="sales"):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(

        f"PRAGMA table_info({table_name})"

    )

    columns = [

        row[1]

        for row in cursor.fetchall()

    ]

    conn.close()

    return columns


# =====================================================
# Check Database Exists
# =====================================================

def database_exists():

    return os.path.exists(DATABASE_PATH)


# =====================================================
# Delete Database
# =====================================================

def clear_database():

    if os.path.exists(DATABASE_PATH):

        os.remove(DATABASE_PATH)