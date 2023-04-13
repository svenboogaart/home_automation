from sqlalchemy import create_engine, text, MetaData, Column, Integer, Table, String, ForeignKey
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass

class DataLayer:

    def __init__(self):
        self.engine = create_engine("sqlite+pysqlite:///:memory:", echo=True)
        self.metadata_obj = MetaData()
        self.lights = Table(
            "lights",
            self.metadata_obj,
            Column("id", Integer, primary_key=True),
            Column("hue_id", Integer, nullable=False),
            Column("name", String(30), nullable=False)
        )
        self.sensors = Table(
            "lights",
            self.metadata_obj,
            Column("id", Integer, primary_key=True),
            Column("hue_id", Integer, nullable=False),
            Column("name", String(30), nullable=False)
        )
        self.light_state_table = Table(
            "light_states",
            self.metadata_obj,
            Column("id", Integer, primary_key=True),
            Column("light_id", ForeignKey("lights.id"), nullable=False),
            Column("date", String, nullable=False),
            Column("state", String, nullable=False)
        )
        self.metadata_obj.create_all()


    def get_activitiies(self):
        with self.engine.connect() as conn:
            result = conn.execute(text("SELECT x, y FROM some_table"))
            for row in result:
                print(f"x: {row.x}  y: {row.y}")
            result = conn.execute(text("select x, y from some_table"))
            print()
            for x, y in result:
                print(f"x {x} y {y}")


    def create_tables(self):
        with self.engine.connect() as conn:
            conn.execute(text("CREATE TABLE some_table (x int, y int)"))
            conn.execute(
                text("INSERT INTO some_table (x, y) VALUES (:x, :y)"),
                [{"x": 1, "y": 1}, {"x": 2, "y": 4}],
            )
            conn.commit()


    def using_meta_object(self):
        print(self.light_state_table.c.keys())
        print(self.light_state_table.primary_key)

data_layer = DataLayer()
data_layer.create_tables()
data_layer.get_activitiies()
data_layer.using_meta_object()
