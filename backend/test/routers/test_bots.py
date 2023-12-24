import pytest
from fastapi import HTTPException
from unittest.mock import patch

from app.src.controller.bot import delete_bot_container, stop_bot_container
# TODO 問子華這樣做是不是對的
@patch('app.src.controller.bot.requests.put')
def test_stop_bot_container_success(mock_put):
    # Set up the mock response
    mock_put.return_value.status_code = 200
    mock_put.return_value.json.return_value = {"message": "Container stopped"}

    # Call the function
    stop_bot_container("container123", "http://worker-ip")

    # Assert that the request was made as expected
    mock_put.assert_called_with("http://worker-ip/stop-container?container_id=container123")

@patch('app.src.controller.bot.requests.put')
def test_stop_bot_container_failure(mock_put):
    # Set up the mock response for failure
    mock_put.return_value.status_code = 400

    # Test if the HTTPException is raised as expected
    with pytest.raises(HTTPException):
        stop_bot_container("container123", "http://worker-ip")

@patch('app.src.controller.bot.requests.delete')
def test_delete_bot_container_success(mock_delete):
    # Similar setup for delete_bot_container
    mock_delete.return_value.status_code = 200
    mock_delete.return_value.json.return_value = {"message": "Container deleted"}

    delete_bot_container("container123", "http://worker-ip")
    mock_delete.assert_called_with("http://worker-ip/delete-container?container_id=container123")

@patch('app.src.controller.bot.requests.delete')
def test_delete_bot_container_failure(mock_delete):
    mock_delete.return_value.status_code = 400

    with pytest.raises(HTTPException):
        delete_bot_container("container123", "http://worker-ip")
        
