CREATE_RECORD = """
                CREATE TABLE IF NOT EXISTS DEV_SND_GBL_GA.DATA_ENGINEERING.TblRecordInferenceLabel (
                FK_ID VARCHAR(150),
                DATETIME TIMESTAMP_TZ,
                PUR_POSTING_DATE VARCHAR(8),
                USER VARCHAR(255),
                ACTIVE_LEARNING BOOLEAN,
                PUR_PO_TEXT VARCHAR(255),
                PUR_COUNTRY VARCHAR(3), 
                PUR_PO_NUM VARCHAR(10), 
                PUR_PO_ITEM NUMBER(38,5), 
                PUR_PO_DOC_TYPE VARCHAR(4),
                PUR_PO_MATDOC VARCHAR(10),
                PUR_PO_IT_MATDOC NUMBER(38,5),
                PUR_C_COST_TYPE VARCHAR(13),
                PUR_ADD_COST_TYPE VARCHAR(4),
                PUR_LINE_DESC_BI_PREDICTED VARCHAR(60), 
                PUR_LINE_DESC_BI_PROBABILITY FLOAT,
                PUR_LINE_DESC_PREDICTED VARCHAR(60), 
                PUR_LINE_DESC_PROBABILITY FLOAT,
                Nivel1_PREDICTED VARCHAR(60), 
                Nivel1_PROBABILITY FLOAT,
                Nivel2_PREDICTED VARCHAR(60), 
                Nivel2_PROBABILITY FLOAT,
                Nivel3_PREDICTED VARCHAR(60), 
                Nivel3_PROBABILITY FLOAT,
                Nivel4_PREDICTED VARCHAR(60), 
                Nivel4_PROBABILITY FLOAT
              );"""

DROP_TABLE_DEV = "DROP TABLE DEV_SND_GBL_GA.DATA_ENGINEERING.TblRecordInferenceLabel;"

INSERT_RECORD = """
                INSERT INTO DEV_SND_GBL_GA.DATA_ENGINEERING.TblRecordInferenceLabel(
                FK_ID,
                DATETIME,
                PUR_POSTING_DATE,
                USER,
                ACTIVE_LEARNING,
                PUR_PO_TEXT,
                PUR_COUNTRY, 
                PUR_PO_NUM, 
                PUR_PO_ITEM, 
                PUR_PO_DOC_TYPE,
                PUR_PO_MATDOC,
                PUR_PO_IT_MATDOC,
                PUR_C_COST_TYPE,
                PUR_ADD_COST_TYPE,
                PUR_LINE_DESC_BI_PREDICTED, 
                PUR_LINE_DESC_BI_PROBABILITY,
                PUR_LINE_DESC_PREDICTED, 
                PUR_LINE_DESC_PROBABILITY,
                Nivel1_PREDICTED, 
                Nivel1_PROBABILITY,
                Nivel2_PREDICTED, 
                Nivel2_PROBABILITY,
                Nivel3_PREDICTED, 
                Nivel3_PROBABILITY,
                Nivel4_PREDICTED, 
                Nivel4_PROBABILITY
                )
                VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                       %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
"""
