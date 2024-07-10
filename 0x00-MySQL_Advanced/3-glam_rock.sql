
-- This script lists all bands with Glam rock as their main style, ranked by their longevity.
-- Import the provided table dump: metal_bands.sql.zip
-- Column names must be: band_name and lifespan.
-- Use attributes formed and split for computing the lifespan.
-- The script can be executed on any database.

SELECT band_name, 
       IFNULL(YEAR(split), 2022) - YEAR(formed) AS lifespan
FROM metal_bands
WHERE main_style = 'Glam rock'
ORDER BY lifespan DESC;
