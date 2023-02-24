CREATE_RECORD = """
                CREATE TABLE IF NOT EXISTS DEV_SND_GBL_GA.DATA_ENGINEERING.TblRecordInferenceLabel (
                FK_ID VARCHAR(255),
                DATETIME TIMESTAMP_TZ,
                USER VARCHAR(255),
                ACTIVE_LEARNING BOOLEAN,
                PUR_PO_TEXT VARCHAR(255),
                PUR_COUNTRY VARCHAR(5), 
                PUR_PO_NUM VARCHAR(30), 
                PUR_PO_ITEM INT, 
                PUR_PO_DOC_TYPE VARCHAR(8),
                PUR_PO_MATDOC VARCHAR(15),
                PUR_PO_IT_MATDOC FLOAT ,
                PUR_C_COST_TYPE VARCHAR(30),
                PUR_ADD_COST_TYPE VARCHAR(10) 
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
