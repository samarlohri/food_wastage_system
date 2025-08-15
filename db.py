# import mysql.connector
# import pandas as pd

# # Function to connect to MySQL database
# def get_connection():
#     return mysql.connector.connect(
#         host="localhost",       # Change if not local
#         user="root",            # Your MySQL username
#         password="@21lohri", # Your MySQL password
#         database="food_wastage" # Your database name
#     )

# # SELECT queries → return DataFrame
# def fetch_query(query, params=None):
#     conn = get_connection()
#     df = pd.read_sql(query, conn, params=params if params else None)
#     conn.close()
#     return df

# # INSERT / UPDATE / DELETE queries
# def execute_query(query, params=None):
#     conn = get_connection()
#     cursor = conn.cursor()
#     cursor.execute(query, params)
#     conn.commit()
#     cursor.close()
#     conn.close()
import mysql.connector
import streamlit as st

def get_connection():
    # Fetch database credentials from Streamlit secrets
    try:
        conn = mysql.connector.connect(
            host=st.secrets["mysql"]["host"],
            user=st.secrets["mysql"]["user"],
            password=st.secrets["mysql"]["password"],
            database=st.secrets["mysql"]["database"]
        )
        return conn
    except Exception as e:
        st.error(f"Database connection failed: {e}")
        return None

def fetch_query(query, params=None):
    conn = get_connection()
    if conn is None:
        return None
    cursor = conn.cursor(dictionary=True)
    cursor.execute(query, params or ())
    rows = cursor.fetchall()
    conn.close()
    return rows

def execute_query(query, params=None):
    conn = get_connection()
    if conn is None:
        return
    cursor = conn.cursor()
    cursor.execute(query, params or ())
    conn.commit()
    conn.close()

