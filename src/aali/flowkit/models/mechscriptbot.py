# Copyright (C) 2025 ANSYS, Inc. and/or its affiliates.
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

"""Model for the MechanicalScriptingBot endpoint."""

from pydantic import BaseModel


class MechScriptBotRequest(BaseModel):
    """Request model for the MechanicalScriptingBot endpoint.

    Parameters
    ----------
    BaseModel : pydantic.BaseModel
        The base model for the request.

    """

    question: str
    mech_script_bot_url: str
    full_human_memory: list[str]
    full_ai_memory: list[str]
    full_variables: list[str]
    full_mechanical_objects: list[str]


class MechScriptBotResponse(BaseModel):
    """Response model for the MechanicalScriptingBot endpoint.

    Parameters
    ----------
    BaseModel : pydantic.BaseModel
        The base model for the response.

    """

    output: str
    updated_human_memory: list[str]
    updated_ai_memory: list[str]
    updated_variables: list[str]
    updated_mechanical_objects: list[str]
