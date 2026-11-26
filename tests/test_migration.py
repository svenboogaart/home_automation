import sqlite3
import unittest

from database.migration import Migration


class LightStatesMigrationTests(unittest.TestCase):
    def test_adds_ids_without_losing_existing_states(self):
        connection = sqlite3.connect(":memory:")
        cursor = connection.cursor()
        cursor.execute('''
            CREATE TABLE lights(
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                type TEXT NOT NULL
            )
        ''')
        cursor.execute('''
            CREATE TABLE light_states(
                light_id INTEGER,
                brightness INTEGER,
                hue INTEGER,
                saturation INTEGER,
                state TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(light_id) REFERENCES lights(id)
            )
        ''')
        cursor.execute(
            "INSERT INTO light_states (light_id, brightness, hue, saturation, state, timestamp) "
            "VALUES (?, ?, ?, ?, ?, ?)",
            ("light-1", 254, 41432, 75, "3", "2025-03-24 12:55:52"),
        )

        Migration.create_tables_if_not_exist(cursor)
        Migration.create_tables_if_not_exist(cursor)

        columns = cursor.execute("PRAGMA table_info(light_states)").fetchall()
        self.assertTrue(any(column[1] == "id" and column[5] == 1 for column in columns))
        existing = cursor.execute(
            "SELECT light_id, brightness, hue, saturation, state, timestamp "
            "FROM light_states"
        ).fetchone()
        self.assertEqual(
            existing,
            ("light-1", 254, 41432, 75, "3", "2025-03-24 12:55:52"),
        )

        cursor.execute(
            "INSERT INTO light_states (light_id, brightness, hue, saturation, state) "
            "VALUES (?, ?, ?, ?, ?)",
            ("light-1", 200, 30000, 50, "2"),
        )
        ids = cursor.execute("SELECT id FROM light_states ORDER BY id").fetchall()
        self.assertEqual(ids, [(1,), (2,)])
        connection.close()


if __name__ == "__main__":
    unittest.main()
