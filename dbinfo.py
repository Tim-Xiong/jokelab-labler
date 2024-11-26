import sqlite3
import pandas as pd

def get_db_info(db_path):
    """
    Retrieve information about the database at the specified path.
    Args:
        db_path (str): The file path to the SQLite database.
    Returns:
        dict: A dictionary containing information about each table in the database.
              The keys are table names, and the values are dictionaries with the following keys:
              - 'column_headers' (list): A list of column names in the table.
              - 'num_rows' (int): The number of rows in the table.
              - 'sample_rows' (DataFrame): A pandas DataFrame containing up to 5 sample rows from the table.
    """
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
    """
    Prints detailed information about database tables.
    Args:
        db_info (dict): A dictionary where keys are table names and values are dictionaries
                        containing the following keys:
                        - 'column_headers' (list): List of column headers for the table.
                        - 'num_rows' (int): Number of rows in the table.
                        - 'sample_rows' (list): List of sample rows from the table.
    Example:
        db_info = {
            'users': {
                'column_headers': ['id', 'name', 'email'],
                'num_rows': 100,
                'sample_rows': [
                    [1, 'Alice', 'alice@example.com'],
                    [2, 'Bob', 'bob@example.com']
                ]
            }
        }
        print_db_info(db_info)
    """
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