-- Keep a log of any SQL queries you execute as you solve the mystery.

-- 1
-- SELECT description
-- FROM crime_scene_reports
-- WHERE month = 7 AND day = 28 AND year = 2021 AND street = "Humphrey Street";

-- | Theft of the CS50 duck took place at 10:15am at the Humphrey Street bakery.
-- Interviews were conducted today with three witnesses who were present at the time – each of their interview transcripts mentions the bakery.
-- | Littering took place at 16:36. No known witnesses.


--2
-- SELECT name, transcript
-- FROM interviews
-- WHERE year = 2021 AND month = 7 AND day = 28;
-- What we have from 2-section query

-- | Ruth    | Sometime within ten minutes of the theft, I saw the thief get into a car in the
-- bakery parking lot and drive away. If you have security footage from the bakery parking lot,
-- you might want to look for cars that left the parking lot in that time frame.
-- | Eugene  | I don't know the thief's name, but it was someone I recognized. Earlier this morning,
-- before I arrived at Emma's bakery, I was walking by the ATM on Leggett Street and saw the thief there withdrawing some money.                                                                                                 |
-- | Raymond | As the thief was leaving the bakery, they called someone who talked to them for less than a minute. In the call,
-- I heard the thief say that they were planning to take the earliest flight out of Fiftyville tomorrow.
-- The thief then asked the person on the other end of the phone to purchase the flight ticket


--3
-- SELECT activity, license_plate
-- FROM bakery_security_logs
-- WHERE year = 2021 AND month = 7 AND day = 28 AND hour = 10 AND 15 <= minute <= 25;
-- The theif drive away at somepoint from 10:15 am to 10:25. 여기 있는 자료가 15분에서 25분사이에 나간 차량번호들.
-- | exit     | 5P2BI95       |
-- | exit     | 94KL13X       |
-- | exit     | 6P58WS2       |
-- | exit     | 4328GD8       |
-- | exit     | G412CB7       |
-- | exit     | L93JTIZ       |
-- | exit     | 322W7JE       |
-- | exit     | 0NTHK55       |
-- | exit     | 1106N58


--4
-- SELECT name
-- FROM people
-- WHERE license_plate IN
-- (SELECT license_plate
-- FROM bakery_security_logs
-- WHERE year = 2021 AND month = 7 AND day = 28 AND hour = 10 AND 15 <= minute <= 25);

--5 이거 작동안됨
-- SELECT receiver
-- FROM phone_calls
-- WHERE year= 2021 AND month = 7 AND day = 28 AND duration < 1
-- INTERSECT
-- SELECT phone_number
-- FROM people
-- WHERE license_plate IN
-- (SELECT license_plate
-- FROM bakery_security_logs
-- WHERE year = 2021 AND month = 7 AND day = 28 AND hour = 10 AND 15 <= minute <= 25);

-- The earliest flight on July 29 in Fiftyville.
-- SELECT id
-- FROM flights
-- WHERE origin_airport_id =
-- (SELECT id
-- FROM airports
-- WHERE city = "Fiftyville")
-- AND year = 2021 AND month = 7 AND day = 29
-- ORDER BY hour, minute
-- LIMIT 1;

-- SELECT passport_number
-- FROM passengers
-- WHERE flight_id =
-- (SELECT id
--     FROM flights
--     WHERE origin_airport_id =
--         (SELECT id
--             FROM airports
--             WHERE city = "Fiftyville")
--         AND year = 2021 AND month = 7 AND day = 29
--         ORDER BY hour, minute
--         LIMIT 1)
-- INTERSECT
-- SELECT passport_number
-- FROM people
-- WHERE license_plate IN
-- (SELECT license_plate
-- FROM bakery_security_logs
-- WHERE year = 2021 AND month = 7 AND day = 28 AND hour = 10 AND 15 <= minute <= 25);


--FINALLLL
-- SELECT id
-- FROM phone_calls
-- WHERE caller IN
-- (SELECT phone_number
-- FROM people
-- WHERE passport_number IN
-- (SELECT passport_number
-- FROM passengers
-- WHERE flight_id =
-- (SELECT id
--     FROM flights
--     WHERE origin_airport_id =
--         (SELECT id
--             FROM airports
--             WHERE city = "Fiftyville")
--         AND year = 2021 AND month = 7 AND day = 29
--         ORDER BY hour, minute
--         LIMIT 1)
-- INTERSECT
-- SELECT passport_number
-- FROM people
-- WHERE license_plate IN
-- (SELECT DISTINCT license_plate
-- FROM bakery_security_logs
-- WHERE year = 2021 AND month = 7 AND day = 28 AND hour = 10 AND 15 <= minute <= 25)))
-- AND year = 2021 AND month = 7 AND day = 28 AND duration < 60;

-- | passport_number |
-- +-----------------+
-- | 1695452385      |
-- | 1988161715      |
-- | 5773159633      |
-- | 8294398571      |
-- | 8496433585      |
-- +-----------------+
-- +--------+
-- |  name  |
-- +--------+
-- | Sofia  |
-- | Taylor |
-- | Luca   |
-- | Kelsey |
-- | Bruce  |
-- +-----+
-- | id  |
-- +-----+
-- | 221 |
-- | 224 |
-- | 233 |
-- | 251 |
-- | 254 |


-- SELECT phone_number
-- FROM people
-- WHERE passport_number IN
-- (SELECT passport_number
-- FROM passengers
-- WHERE flight_id =
-- (SELECT id
--     FROM flights
--     WHERE origin_airport_id =
--         (SELECT id
--             FROM airports
--             WHERE city = "Fiftyville")
--         AND year = 2021 AND month = 7 AND day = 29
--         ORDER BY hour, minute
--         LIMIT 1)
-- INTERSECT
-- SELECT passport_number
-- FROM people
-- WHERE license_plate IN
-- (SELECT license_plate
-- FROM bakery_security_logs
-- WHERE year = 2021 AND month = 7 AND day = 28 AND hour = 10 AND 15 <= minute <= 25));


--BANK
-- SELECT account_number
-- FROM atm_transactions
-- WHERE account_number IN
-- (SELECT account_number
-- FROM bank_accounts
-- WHERE person_id IN
-- ((SELECT id
-- FROM people
-- WHERE passport_number IN
-- (SELECT passport_number
-- FROM passengers
-- WHERE flight_id =
-- (SELECT id
--     FROM flights
--     WHERE origin_airport_id =
--         (SELECT id
--             FROM airports
--             WHERE city = "Fiftyville")
--         AND year = 2021 AND month = 7 AND day = 29
--         ORDER BY hour, minute
--         LIMIT 1)
-- INTERSECT
-- SELECT passport_number
-- FROM people
-- WHERE license_plate IN
-- (SELECT DISTINCT license_plate
-- FROM bakery_security_logs
-- WHERE year = 2021 AND month = 7 AND day = 28 AND hour = 10 AND 15 <= minute <= 25)))))
-- AND atm_location = "Leggett Street" AND transaction_type = "withdraw" AND year = 2021 AND month = 7 AND day = 28;


-- AND atm_location = "Leggett Street" AND transaction_type = "withdraw" AND year = 2021 AND month = 7 AND day = 28;



-- SELECT account_number
-- FROM bank_accounts
-- WHERE person_id IN
-- ((SELECT id
-- FROM people
-- WHERE passport_number IN
-- (SELECT passport_number
-- FROM passengers
-- WHERE flight_id =
-- (SELECT id
--     FROM flights
--     WHERE origin_airport_id =
--         (SELECT id
--             FROM airports
--             WHERE city = "Fiftyville")
--         AND year = 2021 AND month = 7 AND day = 29
--         ORDER BY hour, minute
--         LIMIT 1)
-- INTERSECT
-- SELECT passport_number
-- FROM people
-- WHERE license_plate IN
-- (SELECT DISTINCT license_plate
-- FROM bakery_security_logs
-- WHERE year = 2021 AND month = 7 AND day = 28 AND hour = 10 AND 15 <= minute <= 25))));




--id
-- SELECT id
-- FROM people
-- WHERE passport_number IN
-- (SELECT passport_number
-- FROM passengers
-- WHERE flight_id =
-- (SELECT id
--     FROM flights
--     WHERE origin_airport_id =
--         (SELECT id
--             FROM airports
--             WHERE city = "Fiftyville")
--         AND year = 2021 AND month = 7 AND day = 29
--         ORDER BY hour, minute
--         LIMIT 1)
-- INTERSECT
-- SELECT passport_number
-- FROM people
-- WHERE license_plate IN
-- (SELECT DISTINCT license_plate
-- FROM bakery_security_logs
-- WHERE year = 2021 AND month = 7 AND day = 28 AND hour = 10 AND 15 <= minute <= 25));

-- SELECT account_number
-- FROM bank_accounts
-- WHERE person_id = 467400;



-- Account_number
SELECT person_id
FROM bank_accounts
INTERSECT
SELECT id
FROM people
WHERE passport_number IN
(SELECT passport_number
FROM passengers
WHERE flight_id =
(SELECT id
    FROM flights
    WHERE origin_airport_id =
        (SELECT id
            FROM airports
            WHERE city = "Fiftyville")
        AND year = 2021 AND month = 7 AND day = 29
        ORDER BY hour, minute
        LIMIT 1)
INTERSECT
SELECT passport_number
FROM people
WHERE license_plate IN
(SELECT DISTINCT license_plate
FROM bakery_security_logs
WHERE year = 2021 AND month = 7 AND day = 28 AND hour = 10 AND 15 <= minute <= 25));