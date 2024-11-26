import sqlite3
import pandas as pd

def get_db_info(db_path):
    # Connect to the database
    conn = sqlite3.connect(db_path)
    
    # Get the list of tables
    tables = pd.read_sql_query("SELECT name FROM sqlite_master WHERE type='table';", conn)
    
    db_info = {}
    
    for table_name in tables['name']:
        # Get column headers
        columns = pd.read_sql_query(f"PRAGMA table_info({table_name});", conn)
        column_headers = columns['name'].tolist()
        
        # Get number of rows
        num_rows = pd.read_sql_query(f"SELECT COUNT(*) FROM {table_name};", conn).iloc[0, 0]
        
        # Get sample rows
        sample_rows = pd.read_sql_query(f"SELECT * FROM {table_name} LIMIT 5;", conn)
        
        db_info[table_name] = {
            'column_headers': column_headers,
            'num_rows': num_rows,
            'sample_rows': sample_rows
        }
    
    conn.close()
    
    return db_info

def print_db_info(db_info):
    for table_name, info in db_info.items():
        print(f"Table: {table_name}")
        print(f"Column Headers: {info['column_headers']}")
        print(f"Number of Rows: {info['num_rows']}")
        print("Sample Rows:")
        print(info['sample_rows'])
        print("\n" + "-"*50 + "\n")

if __name__ == "__main__":
    db_path = 'instance/jokes.db'
    db_info = get_db_info(db_path)
    print_db_info(db_info)