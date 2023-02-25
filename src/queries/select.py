# Carlos Giovanny Encinia Gonzalez
# carlos.encinia@ext.cemex.com

DUMMY_QUERY = """
            SELECT
              *
            FROM
              DEV_SND_GBL_GA.DATA_ENGINEERING.TX_COMPRAS_VW_LABELING_DUMMY
            WHERE
              ({keywords_search}
              OR NIVEL_PREDICTED = '{pur_line_desc}')
              AND TO_DATE(PUR_POSTING_DATE, 'yyyyMMdd') 
              BETWEEN '{start_date}' AND '{end_date}'
            LIMIT {sample}"""
QUERY_RECORD = """
            SELECT * FROM  DEV_SND_GBL_GA.DATA_ENGINEERING.TblRecordInferenceLabel"""
QUERY_RECORD_INFERENCE = """
                            SELECT
                              I.FK_ID,
                              I.Nivel1_PREDICTED,
                              O.*
                            FROM
                              DEV_SND_GBL_GA.DATA_ENGINEERING.TblRecordInferenceLabel AS I
                            JOIN (
                                SELECT
                                  FK_ID,
                                  MAX(CAST(Datetime AS TIMESTAMP)) AS max_datetime
                                FROM 
                                  DEV_SND_GBL_GA.DATA_ENGINEERING.TblRecordInferenceLabel
                                GROUP BY
                                  FK_ID
                            ) I_max
                            ON
                              I.fk_id = I_max.fk_id AND I.Datetime = I_max.max_datetime
                            JOIN
                              DEV_SND_GBL_GA.DATA_ENGINEERING.TX_COMPRAS_VW_LABELING_DUMMY AS O
                            ON
                              CONCAT(
                                    O.PUR_COUNTRY,
                                    O.PUR_PO_NUM,
                                    O.PUR_PO_ITEM,
                                    O.PUR_PO_DOC_TYPE,
                                    O.PUR_PO_MATDOC,
                                    O.PUR_PO_IT_MATDOC, 
                                    O.PUR_C_COST_TYPE,
                                    CASE
                                      WHEN O.PUR_ADD_COST_TYPE IS NULL THEN 'NAN'
                                      ELSE O.PUR_ADD_COST_TYPE
                                    END
                                    ) = I.FK_ID
                            WHERE Nivel1_PREDICTED = {}
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
