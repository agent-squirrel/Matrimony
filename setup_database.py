#!/usr/bin/env python3
"""
Database setup script for the wedding website.

Usage:
  python setup_database.py               # full setup: create DB + user + tables
  python setup_database.py --tables-only # create tables only (used by Docker entrypoint)

Reads DB_TYPE (mariadb or postgres), DB_HOST, DB_PORT, DB_USER, DB_PASS, DB_NAME
from the environment or a .env file.
"""

import sys
import os
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from dotenv import load_dotenv
load_dotenv()


def _db_params():
    db_type = os.environ.get('DB_TYPE', 'mariadb').lower()
    is_pg = db_type in ('postgres', 'postgresql')
    return {
        'type': 'postgres' if is_pg else 'mariadb',
        'host': os.environ.get('DB_HOST', 'localhost'),
        'port': int(os.environ.get('DB_PORT', '5432' if is_pg else '3306')),
        'user': os.environ.get('DB_USER', 'wedding_user'),
        'password': os.environ.get('DB_PASS', 'wedding_password'),
        'name': os.environ.get('DB_NAME', 'wedding_db'),
    }


def create_tables(retries=10, delay=3):
    """Create all database tables using Flask-SQLAlchemy models, with retry for Docker startup."""
    from app import app, db

    for attempt in range(1, retries + 1):
        try:
            print(f"Creating database tables (attempt {attempt}/{retries})...")
            with app.app_context():
                db.create_all()
                tables = db.inspect(db.engine).get_table_names()
                print(f"Tables ready: {', '.join(tables)}")
            return True
        except Exception as e:
            if attempt < retries:
                print(f"Database not ready yet ({e}), retrying in {delay}s...")
                time.sleep(delay)
            else:
                print(f"Failed to create tables: {e}")
                import traceback
                traceback.print_exc()
                return False


def setup_mariadb(p):
    """Create MariaDB/MySQL database and user. Requires root access."""
    import pymysql

    root_password = input("Enter MySQL/MariaDB root password: ")
    try:
        conn = pymysql.connect(
            host=p['host'], port=p['port'], user='root', password=root_password,
        )
        cur = conn.cursor()
        cur.execute(
            f"CREATE DATABASE IF NOT EXISTS `{p['name']}` "
            f"CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"
        )
        cur.execute(
            f"CREATE USER IF NOT EXISTS '{p['user']}'@'%' IDENTIFIED BY '{p['password']}'"
        )
        cur.execute(f"GRANT ALL PRIVILEGES ON `{p['name']}`.* TO '{p['user']}'@'%'")
        cur.execute("FLUSH PRIVILEGES")
        cur.close()
        conn.close()
        print("Database and user created.")
    except pymysql.Error as e:
        print(f"MariaDB error: {e}")
        sys.exit(1)


def setup_postgres(p):
    """Create PostgreSQL database and user. Requires superuser (postgres) access."""
    import psycopg2
    from psycopg2 import sql

    superuser_pass = input("Enter PostgreSQL superuser (postgres) password: ")
    try:
        conn = psycopg2.connect(
            host=p['host'], port=p['port'],
            user='postgres', password=superuser_pass,
            dbname='postgres',
        )
        conn.autocommit = True
        cur = conn.cursor()

        cur.execute("SELECT 1 FROM pg_roles WHERE rolname = %s", (p['user'],))
        if cur.fetchone():
            print(f"User '{p['user']}' already exists.")
        else:
            cur.execute(
                sql.SQL("CREATE USER {} WITH PASSWORD %s").format(sql.Identifier(p['user'])),
                (p['password'],),
            )
            print(f"User '{p['user']}' created.")

        cur.execute("SELECT 1 FROM pg_database WHERE datname = %s", (p['name'],))
        if cur.fetchone():
            print(f"Database '{p['name']}' already exists.")
        else:
            cur.execute(
                sql.SQL("CREATE DATABASE {} OWNER {}").format(
                    sql.Identifier(p['name']), sql.Identifier(p['user'])
                )
            )
            print(f"Database '{p['name']}' created.")

        cur.execute(
            sql.SQL("GRANT ALL PRIVILEGES ON DATABASE {} TO {}").format(
                sql.Identifier(p['name']), sql.Identifier(p['user'])
            )
        )
        cur.close()
        conn.close()
        print("Database and user configured.")
    except psycopg2.Error as e:
        print(f"PostgreSQL error: {e}")
        sys.exit(1)


def setup_database():
    p = _db_params()
    print(f"Setting up {p['type']} database '{p['name']}' on {p['host']}:{p['port']}")

    if p['type'] == 'postgres':
        setup_postgres(p)
    else:
        setup_mariadb(p)

    if create_tables():
        print("\nSetup complete.")
        print("Next: run the app and visit /admin/setup to create your admin account.")
    else:
        print("\nDatabase created but table setup failed — check the errors above.")


if __name__ == '__main__':
    if '--tables-only' in sys.argv:
        success = create_tables()
        sys.exit(0 if success else 1)
    else:
        setup_database()
