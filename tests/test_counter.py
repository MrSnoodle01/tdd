"""
Test Cases for Counter Web Service

Create a service that can keep a track of multiple counters
- API must be RESTful - see the status.py file. Following these guidelines, you can make assumptions about
how to call the web service and assert what it should return.
- The endpoint should be called /counters
- When creating a counter, you must specify the name in the path.
- Duplicate names must return a conflict error code.
- The service must be able to update a counter by name.
- The service must be able to read the counter
"""

import pytest

# we need to import the unit under test - counter
from src.counter import app 

# we need to import the file that contains the status codes
from src import status 

@pytest.fixture()
def client():
  return app.test_client()

@pytest.mark.usefixtures("client")
class TestCounterEndPoints:
    """Test cases for Counter-related endpoints"""

    def test_create_a_counter(self, client):
        """It should create a counter"""
        result = client.post('/counters/foo')
        assert result.status_code == status.HTTP_201_CREATED

    def test_duplicate_a_counter(self, client):
        """It should return an error for duplicates"""
        result = client.post('/counters/bar')
        assert result.status_code == status.HTTP_201_CREATED
        result = client.post('/counters/bar')
        assert result.status_code == status.HTTP_409_CONFLICT

    def test_update_a_counter(self, client):
        # create counter
        result = client.post('/counters/result')
        assert result.status_code == status.HTTP_201_CREATED
        counterVal = result.json['result']

        # update counter
        result = client.put('/counters/result')
        assert result.status_code == status.HTTP_200_OK
        postCounterVal = result.json['result']

        # ensure counter did get updated
        assert(counterVal+1 == postCounterVal)

    def test_get_a_counter(self, client):
        # create counter
        result2 = client.post('/counters/result2')
        assert result2.status_code == status.HTTP_201_CREATED
        counterVal = result2.json['result2']

        # get counter val
        result2 = client.get('/counters/result2')
        assert result2.status_code == status.HTTP_200_OK
        postCounterVal = result2.json['result2']

        # make sure that values match
        assert(counterVal == postCounterVal)

    def test_delete_counter(self, client):
        """delete a counter"""
        result = client.delete('/counters/randName')
        assert result.status_code == status.HTTP_204_NO_CONTENT