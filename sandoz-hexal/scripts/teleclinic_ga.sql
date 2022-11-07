
SELECT "Campaign"  
	,SUM("Users") AS USERS
	,SUM("NewUsers") AS NEW_USERS
	,SUM("Sessions") AS SESSIONS 
FROM ECOSYSTEM_PROD.MODEL.GA_LPMETRICS_PATIENT_WEB_APP_VIEW
WHERE 1 = 1
	AND "Date" BETWEEN '%start_date%' AND '%end_date%'
	AND "Campaign" IN ('2417-docmorris-care-schilddruese','2430-docmorris-care-ed-asynchron')
GROUP BY "Campaign";

