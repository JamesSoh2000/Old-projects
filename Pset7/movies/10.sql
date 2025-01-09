-- write a SQL query to list the names of all people who have directed a movie that received a rating of at least 9.0
-- 여기서 DISTINCT란 똑같은 것은 전부 하나로 만드는 removing duplicates 임

SELECT DISTINCT name
FROM people JOIN directors ON directors.person_id = people.id JOIN ratings ON ratings.movie_id = directors.movie_id
WHERE rating >= 9.0;