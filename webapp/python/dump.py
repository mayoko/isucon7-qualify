import os
import MySQLdb.cursors
from PIL import Image
import io
import pathlib

config = {
    'db_host': os.environ.get('ISUBATA_DB_HOST', 'localhost'),
    'db_port': int(os.environ.get('ISUBATA_DB_PORT', '3306')),
    'db_user': os.environ.get('ISUBATA_DB_USER', 'root'),
    'db_password': os.environ.get('ISUBATA_DB_PASSWORD', ''),
}

def dbh():
    conn = MySQLdb.connect(
        host   = config['db_host'],
        port   = config['db_port'],
        user   = config['db_user'],
        passwd = config['db_password'],
        db     = 'isubata',
        charset= 'utf8mb4',
        cursorclass= MySQLdb.cursors.DictCursor,
        autocommit = True,
    )
    cur = conn.cursor()
    cur.execute("SET SESSION sql_mode='TRADITIONAL,NO_AUTO_VALUE_ON_ZERO,ONLY_FULL_GROUP_BY'")
    return conn

def main():
    # save all images to icons directory
    cur = dbh().cursor()
    cur.execute("SELECT * FROM image")
    rows = cur.fetchall()
    icons_folder = pathlib.Path('../public/icons')
    for row in rows:
        avatar_name = row['name']
        avatar_data = row['data']
        print(avatar_name)
        with open(icons_folder / avatar_name, 'wb') as f:
            f.write(avatar_data)
        # img = Image.open(io.BytesIO(avatar_data))
        # img.save(icons_folder / avatar_name)

if __name__ == '__main__':
    main()