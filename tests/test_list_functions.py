# Copyright (C) 2024 - 2025 ANSYS, Inc. and/or its affiliates.
# SPDX-License-Identifier: MIT
#
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
"""Test module for list functions."""

import re

from allie.flowkit import flowkit_service
from fastapi.testclient import TestClient
import pytest

# Initialize the test client
client = TestClient(flowkit_service)


def normalize_text(text):
    """Remove extra spaces, newlines, and indentation."""
    return re.sub(r"\s+", " ", text.strip())


def normalize_response_data(data):
    """Normalize descriptions in the list of functions."""
    for item in data:
        if "description" in item:
            item["description"] = normalize_text(item["description"])
    return data


@pytest.mark.asyncio
async def test_list_functions():
    """Test listing available functions."""
    response = client.get("/", headers={"api-key": "test_api_key"})
    assert response.status_code == 200
    response_data = response.json()

    expected_response_start = [
        {
            "name": "split_ppt",
            "path": "/splitter/ppt",
            "category": "data_extraction",
            "display_name": "Split PPT",
            "description": """Endpoint for splitting text in a PowerPoint document into chunks.
            Parameters
            ----------
            request : SplitterRequest
            An object containing 'document_content' in Base64,
            'chunk_size', and 'chunk_overlap'
            api_key : str
            The API key for authentication.""",
            "inputs": [
                {"name": "document_content", "type": "string(binary)"},
                {"name": "chunk_size", "type": "integer"},
                {"name": "chunk_overlap", "type": "integer"},
            ],
            "outputs": [{"name": "chunks", "type": "array<string>"}],
            "definitions": {},
        },
        {
            "name": "split_py",
            "path": "/splitter/py",
            "category": "data_extraction",
            "display_name": "Split Python Code",
            "description": """Endpoint for splitting Python code into chunks.
            Parameters
            ----------
            request : SplitterRequest
            An object containing 'document_content' in Base64,
            'chunk_size', and 'chunk_overlap'
            api_key : str
            The API key for authentication.
            Returns
            -------
            SplitterResponse
            An object containing a list of text chunks.""",
            "inputs": [
                {"name": "document_content", "type": "string(binary)"},
                {"name": "chunk_size", "type": "integer"},
                {"name": "chunk_overlap", "type": "integer"},
            ],
            "outputs": [{"name": "chunks", "type": "array<string>"}],
            "definitions": {},
        },
        {
            "name": "split_pdf",
            "path": "/splitter/pdf",
            "category": "data_extraction",
            "display_name": "Split PDF",
            "description": """Endpoint for splitting text in a PDF document into chunks.
            Parameters
            ----------
            request : SplitterRequest
            An object containing 'document_content' in Base64,
            'chunk_size', and 'chunk_overlap'.
            api_key : str
            The API key for authentication.
            Returns
            -------
            SplitterResponse
            An object containing a list of text chunks.""",
            "inputs": [
                {"name": "document_content", "type": "string(binary)"},
                {"name": "chunk_size", "type": "integer"},
                {"name": "chunk_overlap", "type": "integer"},
            ],
            "outputs": [{"name": "chunks", "type": "array<string>"}],
            "definitions": {},
        },
    ]

    # Normalize both actual and expected data
    normalized_response = normalize_response_data(response_data[:3])
    normalized_expected = normalize_response_data(expected_response_start)

    assert normalized_response == normalized_expected

    # Test invalid API key
    response = client.get("/", headers={"api-key": "invalid_api_key"})
    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid API key"}
