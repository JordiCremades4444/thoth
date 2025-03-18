import os

import mysql.connector
import pandas as pd
import trino
from dotenv import load_dotenv


class QueryEngines:
    """
    A class to manage SQL queries and interactions with databases.

    Attributes:
        credentials (dict): Database credentials loaded from .env file.
        query_file (str): SQL query file name.
        params (list of dict): Query parameters to replace.
        output_file (str): CSV file name to save or load query results.
    """

    def __init__(self):
        """
        Initializes the QueryEngines object by loading credentials and
        setting paths.
        """
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

    def _ensure_directory(self, path):
        """
        Ensures that the specified directory exists.

        Parameters:
            path (str): Directory path to check or create.
        """
        if not os.path.exists(path):
            os.makedirs(path)

    def prepare_query(
        self, query_file, params=None, output_file=None, load_previous=False
    ):
        """
        Prepares the SQL query by reading from a file and replacing parameters.

        Parameters:
            query_file (str): Name of the SQL query file.
            params (list of dict, optional): Parameters in the query.
            output_file (str, optional): CSV file name.
            load_previous (bool, optional): Whether to load previous results.
        """
        self.query_file = query_file
        self.params = params
        self.output_file = output_file
        self.load_previous = load_previous
        self._ensure_directory(self.sql_path)
        self._ensure_directory(self.query_log_path)
        self._ensure_directory(self.output_path)
        with open(os.path.join(self.sql_path, self.query_file), "r") as f:
            self.read_query = f.read()
        self.tp__read_query = self.replace_params()

    def replace_params(self):
        """
        Replaces parameters in the SQL query with provided values.

        Returns:
            str: The SQL query with parameters replaced.
        """
        if self.params:
            for param in self.params:
                self.read_query = self.read_query.replace(
                    f"{{{param['name']}}}", param["value"]
                )
        return self.read_query

    def load_from_csv(self, file_name):
        """
        Loads data from a CSV file into a DataFrame.

        Parameters:
            file_name (str): Name of the CSV file.

        Returns:
            pd.DataFrame: DataFrame containing the loaded data.

        Raises:
            FileNotFoundError: If the CSV file does not exist.
        """
        file_path = os.path.join(self.output_path, f"{file_name}.csv")
        if os.path.exists(file_path):
            return pd.read_csv(file_path)
        raise FileNotFoundError(f"The file {file_path} does not exist.")

    def save_to_csv(self, df, file_name):
        """
        Saves a DataFrame to a CSV file.

        Parameters:
            df (pd.DataFrame): The DataFrame to save.
            file_name (str): Name of the CSV file.
        """
        file_path = os.path.join(self.output_path, f"{file_name}.csv")
        df.to_csv(file_path, index=False)

    def query_run_starburst(self):
        """
        Runs the SQL query on the Starburst database.

        Returns:
            pd.DataFrame: DataFrame containing the query results.
        """
        if self.load_previous:
            return self.load_from_csv(self.output_file)
        self.log_query(self.tp__read_query)
        conn_details = {
            "host": self.credentials["starbust_host"],
            "port": self.credentials["starbust_port"],
            "user": self.credentials["starbust_user"],
            "http_scheme": "https",
            "auth": trino.auth.OAuth2Authentication(),
        }
        with trino.dbapi.connect(**conn_details) as conn:
            df = pd.read_sql(self.tp__read_query, conn)
        if self.output_file:
            self.save_to_csv(df, self.output_file)
        return df

    def query_run_livedb(self):
        """
        Runs the SQL query on the LiveDB (MySQL) database.

        Returns:
            pd.DataFrame: DataFrame containing the query results.
        """
        if self.output_file:
            return self.load_from_csv(self.output_file)
        self.log_query(self.tp__read_query)
        conn_details = {
            "host": self.credentials["livedb_host"],
            "port": self.credentials["livedb_port"],
            "user": self.credentials["livedb_user"],
            "password": self.credentials["livedb_pw"],
            "database": self.credentials["livedb_database"],
        }
        with mysql.connector.connect(**conn_details) as conn:
            cursor = conn.cursor()
            cursor.execute(self.tp__read_query)
            columns_names = [desc[0] for desc in cursor.description]
            df = pd.DataFrame(cursor.fetchall(), columns=columns_names)
        if self.output_file:
            self.save_to_csv(df, self.output_file)
        return df

    def log_query(self, query):
        """
        Logs the SQL query to a file.

        Parameters:
            query (str): The SQL query to log.
        """
        log_file = os.path.join(self.query_log_path, "log.sql")
        with open(log_file, "w") as f:
            f.write(query)
