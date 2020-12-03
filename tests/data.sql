INSERT INTO laite (id, sijainti)
VALUES
  (666, "puisto1"),
  (123, "kirjasto");

INSERT INTO sensor_data (laite_id, sisaan, aika)
VALUES
  (666, 0, '2020-11-29 09:44:30'),
  (666, 0, '2020-11-29 09:44:35'),
  (666, 1, '2020-11-29 09:45:00'),
  (666, 0, '2020-11-29 09:45:44');