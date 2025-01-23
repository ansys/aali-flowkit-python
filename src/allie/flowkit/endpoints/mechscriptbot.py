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
async def triggerMechanicalScriptingBot(request: MechScriptBotRequest, api_key: str = Header(...)) -> MechScriptBotResponse:
    """Endpoint for triggering the MechanicalScriptingBot application.

    Parameters
    ----------
    request : MechScriptBotRequest
        An object containing the input query and other relevant parameters for the MechanicalScriptingBot application.
    api_key : str
        The API key for authentication.

    """

    if api_key != CONFIG.flowkit_python_api_key:
        raise HTTPException(status_code=401, detail="Invalid API key")
    
    url = str(CONFIG._yaml.get("MECH_SCRIPT_BOT_URL", ""))

    request_dict = request.model_dump()
    request_dict_copy = {key:val for key, val in request_dict.items()}

    full_variables_list = request.full_variables
    full_variables_dict = {variable.split(':')[0] : variable.split(':')[1] for variable in full_variables_list}
    request_dict_copy["full_variables"] = full_variables_dict

    request_dict_copy["full_memory"] = [request.full_human_memory, request.full_ai_memory]

    response_dict = requests.get(url=url, json=request_dict_copy).json()

    output = f"```{response_dict["output"]}"

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

