SELECT COUNT(1) AS AMOUNT_FAILED
FROM ACCESS_DASH.WM4_ZRG_APP_GUI_001_DASH 
WHERE 1 = 1
    AND EXCL_FROM_MONITOR <> 'X';