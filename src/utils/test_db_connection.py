import unittest
from init_db import init_db
from unittest.mock import patch, MagicMock

class TestDBConnection(unittest.TestCase):

    @patch('db_connection.MongoClient')
    def test_init_db_unit_testing(self, mock_mongo_client):
        # Mock environment variables and MongoClient
        with patch.dict('os.environ', {'IS_UNIT_TESTING': 'True'}):
            db = init_db()
            self.assertIsNone(db)  # Expecting None as the database should not initialize during unit tests

    @patch('db_connection.MongoClient')
    def test_init_db_success(self, mock_mongo_client):
        # Mock MongoClient to simulate a successful connection
        mock_client_instance = MagicMock()
        mock_mongo_client.return_value = mock_client_instance
        mock_client_instance.__getitem__.return_value = "MockDB"

        db = init_db()
        self.assertEqual(db, "MockDB")  # Expecting "MockDB" as the return value from the successful connection

    @patch('db_connection.MongoClient')
    def test_init_db_failure(self, mock_mongo_client):
        # Mock MongoClient to simulate a connection failure
        mock_mongo_client.side_effect = pymongo.errors.ConnectionFailure

        with self.assertLogs(level='ERROR') as log:
            db = init_db()
            self.assertIsNone(db)  # Expecting None as the database should not initialize due to connection failure
            self.assertIn('Could not connect to MongoDB', log.output[0])  # Check if the correct error message was logged

if __name__ == '__main__':
    unittest.main()
