import os

import pandas as pd
import mysql.connector as mysql

from dotenv import load_dotenv
load_dotenv()


def mysql_query(query):
    db_params = {
        'database': 'challenge',
        'user': 'root',
        'password': '#V1tor%*',
        'host': 'localhost',
    }

    connection = mysql.connect(**db_params)
    cursor = connection.cursor()

    cursor.execute(query)

    result = cursor.fetchall()

    column_names = [desc[0] for desc in cursor.description]

    df = pd.DataFrame(result, columns=column_names, index=None)

    cursor.close()
    connection.close()

    return df
