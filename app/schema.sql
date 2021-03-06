DROP TABLE IF EXISTS sensor_data;
DROP TABLE IF EXISTS laite;
DROP TABLE IF EXISTS laitteen_tila;

CREATE TABLE laite(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sijainti TEXT UNIQUE NOT NULL
);

CREATE TABLE sensor_data(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    laite_id INTEGER NOT NULL,
    sisaan BOOLEAN NOT NULL CHECK (sisaan IN (0,1)),
    aika TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (laite_id) REFERENCES laite(id)
);

CREATE TABLE laitteen_tila(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    laite_id INTEGER NOT NULL,
    etaisyys1 INTEGER NOT NULL,
    etaisyys2 INTEGER NOT NULL,
    aika TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (laite_id) REFERENCES laite(id)
);