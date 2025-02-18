-- write a SQL query to list the titles of the five highest rated movies (in order)
-- that Chadwick Boseman starred in, starting with the highest rated

SELECT title
-- FROM people JOIN stars ON stars.person_id = people.id JOIN movies ON movies.id = stars.movie_id JOIN ratings ON ratings.movie_id = movies.id
FROM movies JOIN ratings ON ratings.movie_id = movies.id JOIN stars ON stars.movie_id = ratings.movie_id JOIN people ON people.id = stars.person_id
WHERE name = "Chadwick Boseman"
ORDER BY rating DESC
LIMIT 5;
