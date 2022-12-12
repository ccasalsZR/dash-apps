/*
 * BACKORDER
 */

SELECT COUNT(DISTINCT VBFA.VBELV) AS BACKORDER
FROM ACCESS_DASH.ERP_ZGLUE_VBFA_DASH VBFA
LEFT JOIN ACCESS_DASH.ERP_ZGLUE_CHCNL_VKEK_DASH VKEK ON VKEK.VBELN = VBFA.VBELV
INNER JOIN ( -- OPEN ORDERS
	SELECT ORDER_ID
	FROM ACCESS_DASH.P1_AVANTIS_OPEN_DASH
	WHERE (OPEN_TOTAL + GODOT) > 0
	) OPEN_ORD ON OPEN_ORD.ORDER_ID = VBFA.VBELV
WHERE VKEK.PSTYV = 'YTA2'
	AND VKEK.BSTNR = ''