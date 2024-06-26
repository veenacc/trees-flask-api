import sqlite3


def connect_to_db():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn


def initial_setup():
    conn = connect_to_db()
    conn.execute(
        """
        DROP TABLE IF EXISTS photos;
        """
    )
    conn.execute(
        """
        CREATE TABLE photos (
          id INTEGER PRIMARY KEY NOT NULL,
          name TEXT,
          width INTEGER,
          height INTEGER
        );
        """
    )
    conn.commit()
    print("Table created successfully")

    photos_seed_data = [
        ("1st photo", 800, 400),
        ("2nd photo", 1024, 768),
        ("3rd photo", 200, 150),
    ]
    conn.executemany(
        """
        INSERT INTO photos (name, width, height)
        VALUES (?,?,?)
        """,
        photos_seed_data,
    )
    conn.commit()
    print("Seed data created successfully")

    conn.close()


if __name__ == "__main__":
    initial_setup()


# code to pull data for Index/GET action
def photos_all():
    conn = connect_to_db()
    rows = conn.execute(
        """
        SELECT * FROM photos
        """
    ).fetchall()
    return [dict(row) for row in rows]

# code to insert data into db during the create/POST action
def photos_create(name, width, height):
    conn = connect_to_db()
    row = conn.execute(
        """
        INSERT INTO photos (name, width, height)
        VALUES (?, ?, ?)
        RETURNING *
        """,
        (name, width, height),
    ).fetchone()
    conn.commit()
    return dict(row)

# code to show data for a show/get/:id action
def photos_find_by_id(id):
    conn = connect_to_db()
    row = conn.execute(
        """
        SELECT * FROM photos
        WHERE id = ?
        """,
        (id,),
    ).fetchone()
    return dict(row)

# code to update data for a update/patch/:id action
def photos_update_by_id(id, name, width, height):
    conn = connect_to_db()
    row = conn.execute(
        """
        UPDATE photos SET name = ?, width = ?, height = ?
        WHERE id = ?
        RETURNING *
        """,
        (name, width, height, id),
    ).fetchone()
    conn.commit()
    return dict(row)


# code to destroy data for a delete/:id action
def photos_destroy_by_id(id):
    conn = connect_to_db()
    row = conn.execute(
        """
        DELETE from photos
        WHERE id = ?
        """,
        (id,),
    )
    conn.commit()
    return {"message": "Photo destroyed successfully"}