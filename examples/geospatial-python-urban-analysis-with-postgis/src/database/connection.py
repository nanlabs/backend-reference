import os
from dotenv import load_dotenv
from sqlalchemy.engine import Engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import create_engine

load_dotenv()

def get_db_connection() -> Engine:
    """ Return a connection to the database
    Returns:
        Engine: SQLAlchemy engine instance
    Raises:
        SQLAlchemyError: If connection cannot be established
    """
    
    db_name = os.environ["DB_NAME"]
    db_user = os.environ["DB_USER"]
    db_password = os.environ["DB_PASSWORD"]
    db_host = os.environ["DB_HOST"]
    db_port = os.environ["DB_PORT"]
    
    try:
       return create_engine(f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}")
    except Exception as e:
        raise SQLAlchemyError(f"Failed to establish database connection: {str(e)}") from e
