import sqlite3


def get_interval_publish_to_broker_from_sqlite(sqlite_path):
    with sqlite3.connect(sqlite_path) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT interval_publish_to_broker FROM core_middlewarefilter")
        rows = cursor.fetchall()
        return float(rows[0][0])


def get_interval_publish_to_blockchain_from_sqlite(sqlite_path):
    with sqlite3.connect(sqlite_path) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT interval_publish_to_blockchain FROM core_middlewarefilter")
        rows = cursor.fetchall()
        return float(rows[0][0])


def get_low_high_temp_range(sqlite_path):
    with sqlite3.connect(sqlite_path) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT low_temp_range, high_temp_range FROM core_middlewarefilter")
        rows = cursor.fetchall()
        return float(rows[0][0]), float(rows[0][1])
