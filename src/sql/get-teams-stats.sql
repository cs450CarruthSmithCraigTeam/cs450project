SELECT
	`yearID`,
	`name`,
	(W / G) AS `WIN`,
	(R / G) AS `R/G`,
	(H /AB) AS `AVG`,
	`ERA`,
	((`HA` + `BBA`) / (9 * `G`)) AS `WHIP`
FROM `Teams`
WHERE `yearID` < 2017 AND `yearID` > 1975
ORDER BY `WIN` DESC;

-- To output to a file, you can run:
-- SELECT
-- 	`yearID`,
-- 	`name`,
-- 	(W / G) AS `WIN`,
-- 	(R / G) AS `R/G`,
-- 	(H /AB) AS `AVG`,
-- 	`ERA`,
-- 	((`HA` + `BBA`) / (9 * `G`)) AS `WHIP`
-- FROM `Teams`
-- WHERE `yearID` < 2017 AND `yearID` > 1975
-- ORDER BY `WIN` DESC
-- INTO OUTFILE '<your_output_filename>'
-- FIELDS TERMINATED BY ','
-- ENCLOSED BY '"'
-- LINES TERMINATED BY '\n';
