SELECT id FROM artists WHERE name = "Drake";  /* drake's artist_id */
SELECT AVG(energy) FROM songs WHERE artist_id = (SELECT id FROM artists WHERE name = "Drake");