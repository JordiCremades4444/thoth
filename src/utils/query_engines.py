import os

import mysql.connector
import pandas as pd
import trino
from dotenv import load_dotenv
from google.cloud import bigquery


class QueryEngines:
    """
    A class to manage SQL queries and interactions with databases.
    """

    def __init__(self):
        load_dotenv()
        self.credentials = {
            "starbust_host": os.getenv("STARBUST_HOST"),
            "starbust_port": os.getenv("STARBUST_PORT"),
            "starbust_user": os.getenv("STARBUST_USER"),
            "livedb_host": os.getenv("LIVEDB_HOST"),
            "livedb_port": os.getenv("LIVEDB_PORT"),
            "livedb_user": os.getenv("LIVEDB_USER"),
            "livedb_pw": os.getenv("LIVEDB_PW"),
            "livedb_database": os.getenv("LIVEDB_DATABASE"),
        }
        self.sql_path = os.path.join(os.getcwd(), "sql")
        self.query_log_path = os.path.join(os.getcwd(), "query_log")
        self.output_path = os.path.join(os.getcwd(), "query_outputs")

        self.__ensure_directory_exists(self.sql_path)
        self.__ensure_directory_exists(self.query_log_path)
        self.__ensure_directory_exists(self.output_path)
        self.__authenticate_bigquery()

    def __ensure_directory_exists(self, directory_path):
        if not os.path.exists(directory_path):
            os.makedirs(directory_path)

    def __ensure_file_exists(self, file_path):
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"The file {file_path} does not exist.")

    def __replace_params(self):
        if self.params:
            for key, value in self.params.items():
                self.read_query = self.read_query.replace(f"{{{key}}}", value)
        return self.read_query

    def __prepare_query(self, query_file, params=None):
        self.query_file = query_file
        self.params = params

        with open(os.path.join(self.sql_path, self.query_file), "r") as f:
            self.read_query = f.read()

        self.read_query = self.__replace_params()

        return self.read_query

    def __log_query(self, query):
        log_file = os.path.join(self.query_log_path, "log.sql")
        with open(log_file, "w") as f:
            f.write(query)

    def __get_conn_details_starburst(self):
        conn_details = {
            "host": self.credentials["starbust_host"],
            "port": self.credentials["starbust_port"],
            "user": self.credentials["starbust_user"],
            "http_scheme": "https",
            "auth": trino.auth.OAuth2Authentication(),
        }

        return conn_details

    def __query_data_trino(self, query_replaced):
        conn_details = self.__get_conn_details_starburst()
        with trino.dbapi.connect(**conn_details) as conn:
            df = pd.read_sql(query_replaced, conn)

        return df

    def __query_data_bigquery(self, query_replaced):
        clint = bigquery.Client(project="dhub-glovo")

        query_job = clint.query(query_replaced)
        rows = query_job.result()
        df = pd.DataFrame([dict(row) for row in rows])

        return df

    def __save_to_csv(self, df, file_name):
        file_path = os.path.join(self.output_path, f"{file_name}.csv")
        print(file_path)
        df.to_csv(file_path, index=False)

    def __load_from_csv(self, csv_file):
        file_path = os.path.join(self.output_path, f"{csv_file}.csv")
        df = pd.read_csv(file_path)

        return df

    def run_query_starburst(
        self, query_file, params=None, csv_file=None, load_csv_file=False
    ):
        """
        Runs the SQL query or loads from a CSV file on the Starburst database.
        """
        if load_csv_file:
            self.__ensure_file_exists(
                os.path.join(self.output_path, f"{csv_file}.csv")
            )  # Check if the file exists

            df = self.__load_from_csv(csv_file)

        else:
            self.__ensure_file_exists(
                os.path.join(self.sql_path, query_file)
            )  # Check if the file exists

            query_replaced = self.__prepare_query(
                query_file, params
            )  # Prepare the query

            self.__log_query(query_replaced)  # Log the query

            df = self.__query_data_trino(query_replaced)  # Run the query

            self.__save_to_csv(df, csv_file)  # Save the query results to a CSV file

        return df

    def __build_sql_query(self, table_name):
        query = f"select * from {table_name} limit 10"

        return query

    def run_table_explorer_starburst(self, table_name):
        """
        Returns a DataFrame of a table. Used for exploratory data analysis.
        """

        query = self.__build_sql_query(table_name)

        df = self.__query_data_trino(query)

        return df

    def __authenticate_bigquery(self):
        os.system("gcloud auth application-default login --billing-project dhub-glovo")

    def run_query_bigquery(
        self, query_file, params=None, csv_file=None, load_csv_file=False
    ):
        """
        Runs the SQL query or loads from a CSV file on the BigQuery database.
        """

        if load_csv_file:
            self.__ensure_file_exists(os.path.join(self.output_path, f"{csv_file}.csv"))

            df = self.__load_from_csv(csv_file)

        else:
            self.__ensure_file_exists(
                os.path.join(self.sql_path, query_file)
            )  # Check if the file exists

            query_replaced = self.__prepare_query(
                query_file, params
            )  # Prepare the query

            self.__log_query(query_replaced)  # Log the query

            df = self.__query_data_bigquery(query_replaced)  # Run the query

            self.__save_to_csv(df, csv_file)  # Save the query results to a CSV file

        return df

    def run_table_explorer_bigquery(self, table_name):
        """
        Returns a DataFrame of a table. Used for exploratory data analysis.
        """

        query = self.__build_sql_query(table_name)

        df = self.__query_data_bigquery(query)

        return df
