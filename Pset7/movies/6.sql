

-- SELECT AVG(rating) FROM ratings WHERE movie_id IN (SELECT id FROM movies WHERE year = 2012);  -- Version 1  IN function은 multiple OR conditions이라고 생각하면됨.
SELECT AVG(rating) FROM ratings JOIN movies ON movies.id = ratings.movie_id WHERE year = 2012;  -- Version 2 with Join