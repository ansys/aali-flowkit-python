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

"""Module for defining the models used in the endpoints."""

from enum import Enum
from typing import Any

from pydantic import BaseModel


class ParameterInfo(BaseModel):
    """Parameter information model.

    Parameters
    ----------
    BaseModel : pydantic.BaseModel
        The base model for the parameter information

    """

    name: str
    type: str


class EndpointInfo(BaseModel):
    """Endpoint information model.

    Parameters
    ----------
    BaseModel : pydantic.BaseModel
        The base model for the endpoint information

    """

    name: str
    path: str
    category: str
    display_name: str
    description: str
    inputs: list[ParameterInfo]
    outputs: list[ParameterInfo]
    definitions: dict[str, Any]


class FunctionCategory(Enum):
    """Enum for function categories."""

    DATA_EXTRACTION = "data_extraction"
    GENERIC = "generic"
    KNOWLEDGE_DB = "knowledge_db"
    LLM_HANDLER = "llm_handler"
    ANSYS_GPT = "ansys_gpt"
