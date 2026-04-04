"""Tests for mod mutation resolver."""

from unittest.mock import AsyncMock, MagicMock

import pytest
from graphql import GraphQLResolveInfo

from apigateway.resolvers.mutation.mod import CreateModInput, resolve_create_mod


@pytest.mark.asyncio
async def test_create_mod_with_title_field() -> None:
    """Test that createMod mutation correctly processes 'title' field."""
    # Arrange
    mock_client = AsyncMock()
    mock_response = MagicMock()
    mock_response.mod_id = 123
    mock_response.s3_key = "test-key"
    mock_response.upload_url = "https://example.com/upload"
    mock_client.create_mod.return_value = mock_response

    mock_info = MagicMock(spec=GraphQLResolveInfo)
    mock_info.context = {"clients": {"mod_service": mock_client}}

    input_data = {
        "title": "Test Mod Title",
        "author_id": "456",
        "filename": "test.zip",
        "description": "Test description",
    }

    # Act
    result = await resolve_create_mod(None, mock_info, input_data)

    # Assert
    assert result["mod_id"] == 123
    assert result["s3_key"] == "test-key"
    assert result["upload_url"] == "https://example.com/upload"

    # Verify that the client was called with correct parameters
    mock_client.create_mod.assert_called_once_with(
        "Test Mod Title",  # title
        456,  # author_id (converted from string)
        "test.zip",  # filename
        "Test description",  # description
    )


@pytest.mark.asyncio
async def test_create_mod_input_validation() -> None:
    """Test that CreateModInput correctly validates and converts fields."""
    # Arrange
    input_data = {
        "title": "Another Test Mod",
        "author_id": "789",
        "filename": "another.zip",
        "description": "Another description",
    }

    # Act
    validated = CreateModInput.model_validate(input_data)

    # Assert
    assert validated.title == "Another Test Mod"
    assert validated.author_id == 789  # Should be converted to int
    assert validated.filename == "another.zip"
    assert validated.description == "Another description"
