import pytest
from unittest.mock import MagicMock, patch
from psycopg2 import sql

from services.sql_queries import SQLQueries


@pytest.fixture
def mock_cursor():
    return MagicMock()

@pytest.fixture
def mock_conn():
    return MagicMock()

def test_get_table_by_name_success(mock_cursor):
    mock_cursor.fetchone.return_value = (True,)

    # Call the method
    result = SQLQueries.get_table_by_name("test_table", mock_cursor)

    # Assertions
    mock_cursor.execute.assert_called_once_with(sql.SQL("""
                SELECT EXISTS (
                    SELECT FROM information_schema.tables 
                    WHERE table_name = %s
                );
            """), ["test_table"])
    assert result == (True,)

def test_get_table_by_name_failure(mock_cursor):
    mock_cursor.execute.side_effect = Exception("Database error")

    result = SQLQueries.get_table_by_name("test_table", mock_cursor)

    mock_cursor.execute.assert_called_once()
    assert result is None

def test_create_table_success(mock_cursor, mock_conn):
    SQLQueries.create_table("test_table", mock_cursor, mock_conn)

    mock_cursor.execute.assert_called_once_with(sql.SQL("""
                    CREATE TABLE test_table (
                        value REAL,
                        timestamp TIMESTAMP
                    );
                """))
    mock_conn.commit.assert_called_once()

def test_create_table_failure(mock_cursor, mock_conn):
    mock_cursor.execute.side_effect = Exception("Create table error")

    SQLQueries.create_table("test_table", mock_cursor, mock_conn)

    mock_cursor.execute.assert_called_once()
    mock_conn.commit.assert_not_called()

def test_insert_value_success(mock_cursor, mock_conn, mocker):
    mock_uuid = mocker.patch('uuid.uuid4', return_value="test-uuid")
    mock_time = mocker.patch('time.strftime', return_value="2024-10-16 12:00:00")

    SQLQueries.insert_value("test_table", mock_cursor, mock_conn, [70])

    mock_cursor.execute.assert_called_once_with(
        sql.SQL("""
                INSERT INTO {table} (id, value, created_at)
                VALUES (%s, %s, %s)
            """).format(table=sql.Identifier("test_table")),
        ("test-uuid", 70, "2024-10-16 12:00:00")
    )
    mock_conn.commit.assert_called_once()

def test_insert_value_failure(mock_cursor, mock_conn):
    mock_cursor.execute.side_effect = Exception("Insert error")
    SQLQueries.insert_value("test_table", mock_cursor, mock_conn, [70])

    mock_cursor.execute.assert_called_once()
    mock_conn.commit.assert_not_called()
