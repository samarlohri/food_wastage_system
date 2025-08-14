# ---------------- Providers ----------------
GET_ALL_PROVIDERS = "SELECT * FROM providers;"
INSERT_PROVIDER = """
INSERT INTO providers (Provider_ID, Name, Type, Address, City, Contact)
VALUES (%s, %s, %s, %s, %s, %s);
"""
UPDATE_PROVIDER = """
UPDATE providers
SET Name=%s, Type=%s, Address=%s, City=%s, Contact=%s
WHERE Provider_ID=%s;
"""
DELETE_PROVIDER = "DELETE FROM providers WHERE Provider_ID=%s;"

# ---------------- Receivers ----------------
GET_ALL_RECEIVERS = "SELECT * FROM receivers;"
INSERT_RECEIVER = """
INSERT INTO receivers (Receiver_ID, Name, Type, City, Contact)
VALUES (%s, %s, %s, %s, %s);
"""
UPDATE_RECEIVER = """
UPDATE receivers
SET Name=%s, Type=%s, City=%s, Contact=%s
WHERE Receiver_ID=%s;
"""
DELETE_RECEIVER = "DELETE FROM receivers WHERE Receiver_ID=%s;"

# ---------------- Food Listings ----------------
GET_ALL_FOOD_LISTINGS = "SELECT * FROM food_listings;"
INSERT_FOOD_LISTING = """
INSERT INTO food_listings
(Food_Name, Quantity, Expiry_Date, Provider_ID, Provider_Type, Location, Food_Type, Meal_Type)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
"""
UPDATE_FOOD_LISTING = """
UPDATE food_listings
SET Food_Name=%s, Quantity=%s, Expiry_Date=%s, Provider_ID=%s, Provider_Type=%s, Location=%s, Food_Type=%s, Meal_Type=%s
WHERE Food_ID=%s;
"""
DELETE_FOOD_LISTING = "DELETE FROM food_listings WHERE Food_ID=%s;"

# ---------------- Claims ----------------
GET_ALL_CLAIMS = "SELECT * FROM claims;"
INSERT_CLAIM = """
INSERT INTO claims (Claim_ID, Food_ID, Receiver_ID, Status, Claim_Date, Claim_Time)
VALUES (%s, %s, %s, %s, %s, %s);
"""
UPDATE_CLAIM = """
UPDATE claims
SET Food_ID=%s, Receiver_ID=%s, Status=%s, Claim_Date=%s, Claim_Time=%s
WHERE Claim_ID=%s;
"""
DELETE_CLAIM = "DELETE FROM claims WHERE Claim_ID=%s;"


# 📊 Analytics / Non-CRUD Queries

# ----------------------------
# A. Providers & Receivers
# ----------------------------
PROVIDERS_PER_CITY = """
SELECT City, COUNT(*) AS Provider_Count
FROM providers
GROUP BY City
ORDER BY Provider_Count DESC
"""

RECEIVERS_PER_CITY = """
SELECT City, COUNT(*) AS Receiver_Count
FROM receivers
GROUP BY City
ORDER BY Receiver_Count DESC
"""

TOP_PROVIDER_TYPE_BY_FOOD = """
SELECT Provider_Type, SUM(Quantity) AS Total_Quantity
FROM food_listings
GROUP BY Provider_Type
ORDER BY Total_Quantity DESC
LIMIT 1
"""

PROVIDERS_CONTACT_BY_CITY = """
SELECT Name, Contact
FROM providers
WHERE City = %s
"""

RECEIVERS_WITH_MOST_CLAIMS = """
SELECT r.Name, COUNT(c.Claim_ID) AS Claim_Count
FROM claims c
JOIN receivers r ON c.Receiver_ID = r.Receiver_ID
GROUP BY r.Name
ORDER BY Claim_Count DESC
"""

# ----------------------------
# B. Food Listings & Availability
# ----------------------------
TOTAL_FOOD_QUANTITY = "SELECT SUM(Quantity) AS Total_Quantity FROM food_listings"

CITY_WITH_MOST_LISTINGS = """
SELECT Location, COUNT(*) AS Listing_Count
FROM food_listings
GROUP BY Location
ORDER BY Listing_Count DESC
LIMIT 1
"""

MOST_COMMON_FOOD_TYPES = """
SELECT Food_Type, COUNT(*) AS Count
FROM food_listings
GROUP BY Food_Type
ORDER BY Count DESC
"""

# ----------------------------
# C. Claims & Distribution
# ----------------------------
CLAIMS_PER_FOOD_ITEM = """
SELECT f.Food_Name, COUNT(c.Claim_ID) AS Claim_Count
FROM claims c
JOIN food_listings f ON c.Food_ID = f.Food_ID
GROUP BY f.Food_Name
ORDER BY Claim_Count DESC
"""

PROVIDER_WITH_MOST_COMPLETED_CLAIMS = """
SELECT p.Name, COUNT(c.Claim_ID) AS Successful_Claims
FROM claims c
JOIN food_listings f ON c.Food_ID = f.Food_ID
JOIN providers p ON f.Provider_ID = p.Provider_ID
WHERE c.Status = 'Completed'
GROUP BY p.Name
ORDER BY Successful_Claims DESC
LIMIT 1
"""

CLAIM_STATUS_PERCENTAGE = """
SELECT Status, 
       COUNT(*) AS Count,
       ROUND((COUNT(*) / (SELECT COUNT(*) FROM claims)) * 100, 2) AS Percentage
FROM claims
GROUP BY Status
"""

# ----------------------------
# D. Analysis & Insights
# ----------------------------
AVG_QUANTITY_CLAIMED_PER_RECEIVER = """
SELECT r.Name, AVG(f.Quantity) AS Avg_Quantity
FROM claims c
JOIN receivers r ON c.Receiver_ID = r.Receiver_ID
JOIN food_listings f ON c.Food_ID = f.Food_ID
GROUP BY r.Name
"""

MOST_CLAIMED_MEAL_TYPE = """
SELECT Meal_Type, COUNT(*) AS Claim_Count
FROM claims c
JOIN food_listings f ON c.Food_ID = f.Food_ID
GROUP BY Meal_Type
ORDER BY Claim_Count DESC
LIMIT 1
"""

TOTAL_DONATED_BY_PROVIDER = """
SELECT p.Name, SUM(f.Quantity) AS Total_Donated
FROM food_listings f
JOIN providers p ON f.Provider_ID = p.Provider_ID
GROUP BY p.Name
ORDER BY Total_Donated DESC
"""
