from flask import g
from app.config.configGetter import get_csv_files
import sqlite3
import pandas as pd


def init_app(app):
    """
    initialize app
    :param app: app
    """
    app.teardown_appcontext(close_connection)


def get_db():
    """
    create database if none exists
    :return: database instance
    """
    db = getattr(g, '_database', None)

    if db is None:
        db = g._database = sqlite3.connect('database.db')
    return db


def init_db():
    """
    initialize database, clear existing data and create new tables
    """
    db = get_db()

    with open('schema.sql') as f:
        db.executescript(f.read())


def fill_db(conn):
    """
    fill database with data from csv files specified in configuration
    :param conn: database connection
    """
    csv_files = get_csv_files()

    for csv_file, table_name in csv_files.items():
        df = pd.read_csv(f'app/static/{csv_file}.csv')
        df.to_sql(table_name, conn, if_exists='append', index=False)


def close_connection(exception):
    """
    close database connection
    """
    db = getattr(g, '_database', None)

    if db is not None:
        db.close()
