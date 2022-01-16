from pathlib import Path

ROOT_PATH=Path("/mnt/c/Users/micro/Nextcloud/Spiele/stats-racing/")
PATH_SQL_INSERT=Path("sql/inserts/")

def read_sql_insert_template(sql_file):
    file_path = PATH_SQL_INSERT / sql_file
    return file_path.read_text().replace('\n', ' ')