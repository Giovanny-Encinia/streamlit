# Carlos Giovanny Encinia Gonzalez
# carlos.encinia@ext.cemex.com

# WIP, this query will change when we can write the tbl record inference in prod database
QUERY_SPEND = """
            SELECT
              *
            FROM
              PRD_TDS_GBL_PROCUREMENT.DAT.TX_COMPRAS_VW_OPT
            WHERE
              ({keywords_search})
              AND TO_DATE(PUR_POSTING_DATE, 'yyyyMMdd') 
              BETWEEN '{start_date}' AND '{end_date}'
              AND PUR_COUNTRY IN ('CO')
              AND PUR_PO_NUM IS NOT NULL 
              AND PUR_PO_NUM != ''
              AND (PUR_LINE_DESC IS NULL OR PUR_LINE_DESC = '') 
              AND (PUR_CATEG_DESC IS NULL OR PUR_LINE_DESC = '') 
              AND PUR_VENDOR_CODE like '0005%'
              AND PUR_PO_TEXT IS NOT NULL
              AND PUR_COUNTRY IS NOT NULL
              AND PUR_PO_NUM IS NOT NULL
              AND PUR_PO_ITEM IS NOT NULL
              AND PUR_PO_IT_MATDOC IS NOT NULL 
              AND PUR_C_COST_TYPE IS NOT NULL
            LIMIT {sample}"""
# This query will not be used in the future when the record inference exists in de prod database
# but the structure for the final query is the same
QUERY_RECORD = """
              WITH CTE AS (
                SELECT
                  *,
                  ROW_NUMBER() OVER (PARTITION BY FK_ID ORDER BY Datetime DESC) AS time
                FROM
                  DEV_SND_GBL_GA.DATA_ENGINEERING.TblRecordInferenceLabel
              )
              SELECT 
                *
              FROM
                CTE
              WHERE
                time = 1 AND
              ({keywords_search} OR {condition_pred})
              AND TO_DATE(PUR_POSTING_DATE, 'yyyyMMdd') 
              BETWEEN '{start_date}' AND '{end_date}'
              AND PUR_COUNTRY IN ('CO')
             """
QUERY_SEARCH_UNIQUE = """
    SELECT
       *
    FROM
      PRD_TDS_GBL_PROCUREMENT.DAT.TX_COMPRAS_VW_OPT
    WHERE
      1 = 1
      AND PUR_COUNTRY IN ('{country}')
      AND PUR_PO_NUM LIKE '%{number}%'
      AND PUR_PO_DOC_TYPE LIKE '%{doc}%'
      AND PUR_PO_MATDOC LIKE '%{matdoc}%'
      AND PUR_C_COST_TYPE LIKE '{cost_type}'
"""
QUERY_SEARCH_UNIQUE_INFERENCE = """
    WITH CTE AS (
                SELECT
                  *,
                  ROW_NUMBER() OVER (PARTITION BY FK_ID ORDER BY Datetime DESC) AS time
                FROM
                  DEV_SND_GBL_GA.DATA_ENGINEERING.TblRecordInferenceLabel
              )
              SELECT 
                *
              FROM
                CTE
              WHERE
                time = 1
                AND PUR_COUNTRY IN ('{country}')
                AND PUR_PO_NUM LIKE '%{number}%'
                AND PUR_PO_DOC_TYPE LIKE '%{doc}%'
                AND PUR_PO_MATDOC LIKE '%{matdoc}%'
                AND PUR_C_COST_TYPE LIKE '{cost_type}'
"""
