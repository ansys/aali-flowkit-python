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

"""Utils module for FastAPI related operations."""

import inspect
from typing import Any, get_type_hints

from allie.flowkit.models.functions import EndpointInfo, ParameterInfo
from fastapi.routing import APIRoute
from pydantic import BaseModel


def extract_field_type(field_info: dict):
    """Extract the field type from a given schema field information.

    Parameters
    ----------
    field_info : dict
        The field information from the schema.

    Returns
    -------
    str
        The extracted field type.

    """
    field_type = field_info.get("type", "Unknown")
    if field_type == "object":
        dict_field = field_info.get("additionalProperties", {})
        dict_type = dict_field.get("type", "Unknown")
        return f"dict[string][{dict_type}]"
    if field_type == "array":
        items = field_info.get("items", {})
        item_type = extract_field_type(items)
        return f"array<{item_type}>"
    elif field_type == "string" and field_info.get("format") == "binary":
        return "string(binary)"
    elif "$ref" in field_info and field_type == "Unknown":
        ref = field_info["$ref"]
        ref_name = ref.split("/")[-1]
        return ref_name
    return field_type


def extract_fields_from_schema(schema: dict):
    """Extract fields and their types from a schema.

    Parameters
    ----------
    schema : dict
        The schema dictionary.

    Returns
    -------
    list
        A list of ParameterInfo objects representing the fields.

    """
    fields = []
    properties = schema.get("properties", {})
    for field_name, field_info in properties.items():
        fields.append(ParameterInfo(name=field_name, type=extract_field_type(field_info)))
    return fields


def get_parameters_info(params: dict):
    """Get parameter information from function parameters.

    Parameters
    ----------
    params : dict
        A dictionary of function parameters.

    Returns
    -------
    list
        A list of ParameterInfo objects representing the parameters.

    """
    parameters_info = []
    for param in params.values():
        # If the param is a header skip it
        if "alias" in str(param.default) and "annotation" in str(param.default):
            continue
        if isinstance(param.annotation, bytes):
            param_info = ParameterInfo(name=param.name, type="bytes")
            parameters_info.append(param_info)
        elif hasattr(param.annotation, "model_json_schema"):
            schema = param.annotation.model_json_schema()
            param_info = extract_fields_from_schema(schema)
            parameters_info.extend(param_info)
        else:
            param_info = ParameterInfo(name=param.name, type=str(param.annotation))
            parameters_info.append(param_info)
    return parameters_info


def get_return_type_info(return_type: type[BaseModel]):
    """Get return type information from the function's return type.

    Parameters
    ----------
    return_type : type[BaseModel]
        The return type of the function.

    Returns
    -------
    list
        A list of ParameterInfo objects representing the return type fields.

    """
    if hasattr(return_type, "model_json_schema"):
        schema = return_type.model_json_schema()
        return extract_fields_from_schema(schema)
    return [ParameterInfo(name="return", type=str(return_type.__name__))]


def extract_definitions_from_schema(schema: dict) -> dict[str, Any]:
    """Extract definitions from a schema.

    Parameters
    ----------
    schema : dict
        The schema dictionary.

    Returns
    -------
    dict
        A dictionary of definitions.

    """
    definitions = schema.get("$defs", {})
    return definitions


def get_definitions_from_params(params: dict) -> dict[str, Any]:
    """Get definitions from function parameters.

    Parameters
    ----------
    params : dict
        A dictionary of function parameters.

    Returns
    -------
    dict
        A dictionary of definitions extracted from the parameters.

    """
    definitions = {}
    for param in params.values():
        if hasattr(param.annotation, "model_json_schema"):
            schema = param.annotation.model_json_schema()
            definitions.update(extract_definitions_from_schema(schema))
    return definitions


def get_definitions_from_return_type(return_type: type[BaseModel]) -> dict[str, Any]:
    """Get definitions from the function's return type.

    Parameters
    ----------
    return_type : type[BaseModel]
        The return type of the function.

    Returns
    -------
    dict
        A dictionary of definitions extracted from the return type.

    """
    if hasattr(return_type, "model_json_schema"):
        schema = return_type.model_json_schema()
        return extract_definitions_from_schema(schema)
    return {}


def extract_endpoint_info(function_map: dict[str, Any], routes: list[APIRoute]) -> list[EndpointInfo]:
    """Extract endpoint information from the given routes.

    Parameters
    ----------
    function_map : dict[str, Any]
        A dictionary mapping function names to their implementations.
    routes : list[APIRoute]
        A list of APIRoute objects representing the API routes.

    Returns
    -------
    list
        A list of EndpointInfo objects representing the endpoints.

    """
    endpoint_list = []
    for route in routes:
        if hasattr(route, "endpoint"):
            func_name = route.endpoint.__name__
            if func_name in function_map:
                signature = inspect.signature(route.endpoint)
                inputs = get_parameters_info(signature.parameters)
                return_type = get_type_hints(route.endpoint).get("return", None)
                outputs = get_return_type_info(return_type) if return_type else []

                # Get definitions from both inputs and outputs
                input_definitions = get_definitions_from_params(signature.parameters)
                output_definitions = get_definitions_from_return_type(return_type) if return_type else {}
                definitions = {**input_definitions, **output_definitions}

                # Extract category and display name from decorators
                category = getattr(route.endpoint, "category", "Uncategorized")
                display_name = getattr(route.endpoint, "display_name", func_name)

                # Extract the description from the docstring
                description = inspect.getdoc(route.endpoint) or "No description available"

                endpoint_info = EndpointInfo(
                    name=func_name,
                    path=route.path,
                    inputs=inputs,
                    outputs=outputs,
                    definitions=definitions,
                    category=category,
                    display_name=display_name,
                    description=description,
                )
                endpoint_list.append(endpoint_info)
    return endpoint_list
