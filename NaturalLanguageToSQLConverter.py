from connection import Connection
import pandas as pd
from sqlalchemy import MetaData, Table
from dotenv import load_dotenv
import os
import openai

class SQLConverter:

    def __init__(self):
        load_dotenv()
        self.engine = Connection('database.db').get_engine()
        self.user_table = 'user'
        self.api_key = os.getenv('OPENAI_KEY')

    def contact_api(self, message: str):
        data = self.get_user_table_data()
        table_prompt = self.get_table_data_for_prompt(data)

        combined_prompt = self.combine_prompts(table_prompt, message)
        return self.get_response(combined_prompt)
        
    def get_user_table_data(self):
        metadata = MetaData()
        metadata.reflect(bind=self.engine)
        table = metadata.tables[self.user_table]

        query = table.select()
        df = pd.read_sql(query, self.engine)
        self.engine.dispose()

        return df

    def get_table_data_for_prompt(self, df):
        prompt = '''### sqlite SQL table, with its properties:
        #
        # users({})
        #
        '''.format(",".join(str(x) for x in df.columns))
            
        return prompt

    def combine_prompts(self, df, query_prompt):
        query_init_string = f"### A query to answer: {query_prompt}\nSELECT"
        return df + query_init_string

    def get_response(self, prompt):
        openai.api_key = self.api_key 
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=prompt,
            temperature=0,
            max_tokens=150,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0,
            stop=["#", ";"]
        )

        return response
