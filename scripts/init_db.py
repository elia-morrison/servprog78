import sqlite3
import os

def apply_sql_scripts(db_path, sql_directory):
    """
    Apply all .sql scripts in the given directory to the SQLite database specified by db_path.

    Args:
    db_path (str): Path to the SQLite database file.
    sql_directory (str): Directory containing .sql files.
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        for filename in os.listdir(sql_directory):
            if filename.endswith(".sql"):
                filepath = os.path.join(sql_directory, filename)
                print(f"Applying script: {filename}")
                
                with open(filepath, 'r', encoding='utf-8') as file:
                    sql_script = file.read()

                cursor.executescript(sql_script)
                conn.commit()
                print(f"Applied {filename} successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        cursor.close()
        conn.close()


if __name__ == "__main__":
    db_path = '../database/db.db'
    sql_directory = './sql/'
    apply_sql_scripts(db_path, sql_directory)