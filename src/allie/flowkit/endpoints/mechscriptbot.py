# Copyright (C) 2024 ANSYS, Inc. and/or its affiliates.
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

"""Module for triggering the MechanicalScriptingBot application."""

from allie.flowkit.config._config import CONFIG
from allie.flowkit.models.functions import FunctionCategory
from allie.flowkit.models.mechscriptbot import MechScriptBotRequest, MechScriptBotResponse
from allie.flowkit.utils.decorators import category, display_name
from fastapi import APIRouter, Header, HTTPException
import requests

router = APIRouter()


@router.post("/trigger", response_model=MechScriptBotResponse)
@category(FunctionCategory.GENERIC)
@display_name("MechanicalScriptingBot")
async def triggermechscriptbot(request: MechScriptBotRequest, api_key: str = Header(...)) -> MechScriptBotResponse:
    """Endpoint for triggering the MechanicalScriptingBot application.

    Parameters
    ----------
    request : MechScriptBotRequest
        An object containing the input query and other relevant parameters for the MechanicalScriptingBot application.
    api_key : str
        The API key for authentication.

    Returns
    -------
    MechScriptBotResponse
        An object containing the output and other relevant metadata for the MechanicalScriptingBot application.

    """

    if api_key != CONFIG.flowkit_python_api_key:
        raise HTTPException(status_code=401, detail="Invalid API key")
    
    url = request.mech_script_bot_url

    request_dict = request.model_dump()
    request_dict_copy = {key:val for key, val in request_dict.items()}

    full_variables_list = request.full_variables
    full_variables_dict = {variable.split(':')[0] : variable.split(':')[1] for variable in full_variables_list}
    request_dict_copy["full_variables"] = full_variables_dict

    request_dict_copy["full_memory"] = [request.full_human_memory, request.full_ai_memory]

    response_dict = requests.get(url=url, json=request_dict_copy).json()

    output = f"```{response_dict['output']}"

    human_new_mem, ai_new_mem = tuple(response_dict["new_memory"])
    updated_human_memory = request.full_human_memory + [human_new_mem]
    updated_ai_memory = request.full_ai_memory + [ai_new_mem]

    new_variables_list = [f"{var_name}:{var_type}" for var_name, var_type in (response_dict["new_variables"]).items()]
    updated_variables = request.full_variables + new_variables_list

    updated_mechanical_objects = request.full_mechanical_objects + response_dict["new_mechanical_objects"]

    return MechScriptBotResponse(
        output=output,
        updated_human_memory=updated_human_memory,
        updated_ai_memory=updated_ai_memory,
        updated_variables=updated_variables,
        updated_mechanical_objects=updated_mechanical_objects
    )

