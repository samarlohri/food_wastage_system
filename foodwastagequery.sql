create database food_wastage;
use food_wastage;

CREATE TABLE providers (
    Provider_ID INT PRIMARY KEY,
    Name VARCHAR(100),
    Type VARCHAR(50),
    Address VARCHAR(255),
    City VARCHAR(50),
    Contact VARCHAR(20)
);

CREATE TABLE receivers (
    Receiver_ID INT PRIMARY KEY,
    Name VARCHAR(100),
    Type VARCHAR(50),
    City VARCHAR(50),
    Contact VARCHAR(30)
);

CREATE TABLE food_listings (
    Food_ID INT PRIMARY KEY,
    Food_Name VARCHAR(100),
    Quantity INT,
    Expiry_Date VARCHAR(20),
    Provider_ID INT,
    Provider_Type VARCHAR(50),
    Location VARCHAR(50),
    Food_Type VARCHAR(30),
    Meal_Type VARCHAR(30),
    FOREIGN KEY (Provider_ID) REFERENCES providers(Provider_ID)
);
SET SQL_SAFE_UPDATES = 0;
UPDATE food_listings
SET Expiry_Date = STR_TO_DATE(Expiry_Date, '%c-%e-%Y');

select * from food_listings;

CREATE TABLE claims (
    Claim_ID INT PRIMARY KEY,
    Food_ID INT,
    Receiver_ID INT,
    Status VARCHAR(20),
    Timestamp VARCHAR(30),
    FOREIGN KEY (Food_ID) REFERENCES food_listings(Food_ID),
    FOREIGN KEY (Receiver_ID) REFERENCES receivers(Receiver_ID)
);
 

ALTER TABLE claims
ADD COLUMN Claim_Date DATE,
ADD COLUMN Claim_Time TIME;

UPDATE claims
SET Claim_Date = STR_TO_DATE(Timestamp, '%c-%e-%Y %H:%i'),
    Claim_Time = STR_TO_DATE(Timestamp, '%c-%e-%Y %H:%i');

ALTER TABLE claims
DROP COLUMN Timestamp;
 
 
 -- 15 queries of sql
-- 1.) 
select Count(*) From Providers;
select Count(*) From Receivers;
select Count(*) From food_listings;
select Count(*) From claims;

-- 2.) Ensure no NULLs in key relationships
select * from claims 
where Food_ID is null or Receiver_ID is null;

-- 3.)  Providers & receivers count per city
select city, Count(*) as providers_count
from providers
group by city
order by providers_count desc;

select city , count(*) as receivers_count
from receivers
group by city
order by receivers_count desc;


-- 4.) Provider type contributing the most food

select provider_type, SUM(Quantity) AS Total_Quantity
FROM food_listings
GROUP BY Provider_Type
ORDER BY Total_Quantity DESC
LIMIT 1;

-- 5.) Contact info of providers in a specific city 

select name, contact
from providers
where city = 'New Jessica';

-- 6.) Receivers with the most claims

SELECT r.Name, COUNT(c.Claim_ID) AS Claim_Count
FROM claims c
JOIN receivers r ON c.Receiver_ID = r.Receiver_ID
GROUP BY r.Name
ORDER BY Claim_Count DESC;

-- 7.)Total quantity of food available
select sum(quantity) as total_quantity
from food_listings;

-- 8.)  City with highest number of food listings

SELECT Location, COUNT(*) AS Listing_Count
FROM food_listings
GROUP BY Location
ORDER BY Listing_Count DESC
LIMIT 1;

-- 9.) most common food type
SELECT Food_Type, COUNT(*) AS Count
FROM food_listings
GROUP BY Food_Type
ORDER BY Count DESC
limit 1;

-- 10.)Number of claims per food item

SELECT f.Food_Name, COUNT(c.Claim_ID) AS Claim_Count
FROM claims c
JOIN food_listings f ON c.Food_ID = f.Food_ID
GROUP BY f.Food_Name
ORDER BY Claim_Count DESC;

-- 11.) Provider with most successful claims

SELECT p.Name, COUNT(c.Claim_ID) AS Successful_Claims
FROM claims c
JOIN food_listings f ON c.Food_ID = f.Food_ID
JOIN providers p ON f.Provider_ID = p.Provider_ID
WHERE c.Status = 'Completed'
GROUP BY p.Name
ORDER BY Successful_Claims DESC
LIMIT 1;

-- 12.) Percentage of claim statuses

SELECT Status, 
       COUNT(*) AS Count,
       ROUND((COUNT(*) / (SELECT COUNT(*) FROM claims)) * 100, 2) AS Percentage
FROM claims
GROUP BY Status;

-- 13.) Average quantity of food claimed per receiver

SELECT r.Name, AVG(f.Quantity) AS Avg_Quantity
FROM claims c
JOIN receivers r ON c.Receiver_ID = r.Receiver_ID
JOIN food_listings f ON c.Food_ID = f.Food_ID
GROUP BY r.Name;

-- 14.) Most claimed meal type

SELECT Meal_Type, COUNT(*) AS Claim_Count
FROM claims c
JOIN food_listings f ON c.Food_ID = f.Food_ID
GROUP BY Meal_Type
ORDER BY Claim_Count DESC
LIMIT 1;

-- 15.)Total quantity donated by each provider

SELECT p.Name, SUM(f.Quantity) AS Total_Donated
FROM food_listings f
JOIN providers p ON f.Provider_ID = p.Provider_ID
GROUP BY p.Name
ORDER BY Total_Donated DESC;



