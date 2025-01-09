-- SELECT license_plate
-- FROM bakery_security_logs
-- WHERE year = 2021 AND month = 7 AND day = 28 AND hour = 10 AND 15 <= minute <= 25 AND activity = "exit";



SELECT name
FROM people
WHERE license_plate IN
(SELECT license_plate
FROM bakery_security_logs
WHERE year = 2021 AND month = 7 AND day = 28 AND hour = 10 AND 15 <= minute <= 25 AND activity = "exit");

SELECT account_number
FROM people
JOIN bakery_security_logs ON bakery_security_logs.license_plate = people.license_plate
JOIN bank_accounts ON bank_accounts.person_id = people.id
WHERE year = 2021 AND month = 7 AND day = 28 AND hour = 10 AND 15 <= minute <= 25 AND activity = "exit";


-- transaction에서 이 특정시간에 뽑은 account_number인 사람 모음
SELECT name
FROM people JOIN bank_accounts ON bank_accounts.person_id = people.id
WHERE account_number IN (
    SELECT DISTINCT account_number
    FROM atm_transactions
    WHERE account_number IN
    (SELECT account_number
    FROM people
    JOIN bakery_security_logs ON bakery_security_logs.license_plate = people.license_plate
    JOIN bank_accounts ON bank_accounts.person_id = people.id
    WHERE year = 2021 AND month = 7 AND day = 28 AND hour = 10 AND 15 <= minute AND minute <= 25 AND activity = "exit")
    AND transaction_type = "withdraw" AND atm_location = "Leggett Street")

INTERSECT

-- -- Passport정보
SELECT name
FROM people
JOIN passengers ON passengers.passport_number = people.passport_number
WHERE passengers.flight_id = (
    -- This will give only one 'id' of flights that is the earliest flight on this particular time.
    SELECT DISTINCT id
    FROM flights
    WHERE year = 2021 AND month = 7 AND day = 29 AND origin_airport_id = (
        SELECT id
        FROM airports
        WHERE city = "Fiftyville"
    )
    ORDER BY hour, minute
    LIMIT 1
)

INTERSECT

-- -- Call 정보
SELECT name
FROM people JOIN phone_calls ON phone_calls.caller = people.phone_number
WHERE year= 2021 AND month = 7 AND day = 28 AND duration < 60;

-- --최종적으로 이 3가지 리스트의 사람들을 전부 intersect(교집합)을 사용하면 한명의 공통된 인물 Bruce가 범인인것을 알수있음

-- 2. 어디로 도망간건지 아는법
SELECT city
FROM airports
WHERE id = (
    SELECT destination_airport_id
    FROM flights
    JOIN passengers ON passengers.flight_id = flights.id
    JOIN people ON people.passport_number = passengers.passport_number
    WHERE origin_airport_id = (
        SELECT id
        FROM airports
        WHERE city = "Fiftyville"
    )
    AND name = "Bruce"
);





