# Allie FlowKit Python

Welcome to Allie FlowKit Python. This repository hosts Python functions similar to [Allie FlowKit](https://github.com/ansys/allie-flowkit) and provides a service for exposing APIs for each external function added to it. You can use these functions to build Allie workflows, enabling a flexible and modular approach to creating and executing workflows with Allie.

## Table of contents
- [Introduction](#introduction)
- [Objectives](#objectives)
- [How it works](#how-it-works)
- [Getting started](#getting-started)
    - [Run locally](#run-locally)
        - [Prerequisites](#prerequisites)
        - [Installation](#installation)
        - [Usage](#usage)
    - [Run as a Docker container](#run-as-a-docker-container)
- [Adding custom functions](#adding-custom-functions)
  - [Example](#example)
- [Example functions](#example-functions)
- [Contributing](#contributing)

## Introduction

Allie FlowKit Python is designed to host the code for a Python service that exposes a REST API for each external function added to it. These functions can be seamlessly integrated into Allie workflows and executed by the Allie agent, making it easier for teams to customize and extend their workflow capabilities.

## Objectives

Using Allie Flowkit Python lets you achieve these key objectives:

- Host Python functions similar to those in [Allie FlowKit](https://github.com/ansys/allie-flowkit).
- Provide a service that exposes these functions as REST APIs.
- Enable the creation of custom Allie workflows using these functions.
- Allow other teams to add their needed functions to support their specific Allie workflows.

## How it works

Allie Flowkit Python supports these actions:

1. **Function integration:** Add external functions to this repository and expose them as REST APIs.
2. **Workflow execution:** Include functions from Allie FlowKit Python in Allie workflows.
3. **API calls:** When an Allie workflow includes a function from Allie FlowKit Python, the Allie agent calls the function via a REST API with the required inputs.
4. **Function execution:** The function is executed in Allie FlowKit Python, and the output is returned as the body of the REST response.

## Getting started

Allie FlowKit Python can be run locally or as a Docker container. Follow the instructions below to get started.

### Run locally

#### Prerequisites

- Python 3.7 or later
- pip (Python package installer)
- A running instance of the Allie Flowkit

#### Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/allie-flowkit-python.git
    cd allie-flowkit-python
    ```

2. Install the project:
    ```sh
    pip install .
    ```

#### Usage

1. Start the service:
    ```sh
    allie-flowkit-python --host 0.0.0.0 --port 50052 --workers 1
    ```
    You can specify the host, port, and number of workers as needed.

2. The service will expose the functions as REST APIs on the specified port (default: 50052).

3. Integrate these APIs into your Allie workflows as needed.

### Run as a Docker container

1. Build the Docker container image with the following command:

```bash
    docker build -f docker/Dockerfile . -t allie-flowkit-python:latest
```

2. Run the Docker container and expose the port on your desired endpoint. You can also specify the number of workers as needed:

```bash
    docker run -d -e WORKERS=5 --rm --name allie-flowkit-python -p 50052:50052 allie-flowkit-python:latest
```

## Adding custom functions

1. **Create a New Function:**
   - Add your function code as an endpoint to a new Python file in the `allie/flowkit/endpoints` directory.
   - Use the `allie/flowkit/endpoints/splitter.py` file and its endpoints as an example.
   - Explicitly define the input and output of the function using Pydantic models, as these will be used by the Allie Agent to call the function.
   - Add the category and display name of the function to the endpoint definition.

2. **Add the models for the function:**
   - Create the models for the input and output of the function in the `allie/flowkit/models` directory.
   - Use the `allie/flowkit/models/splitter.py` file and its models as an example.

3. **Add the endpoints to the service:**
   - Import your module in the `allie/flowkit/flowkit_service.py` file and add the router to the service.

4. **Add the function to the function map:**
    - Add your function to the `function_map` dictionary in the `allie/flowkit/flowkit_service.py` file.

### Example´

1. **Create a new file for all your custom functions:**
- In the `allie/flowkit/endpoints` directory, create a new Python file named `custom_endpoint.py`.

2. **Create the models for the custom function:**
- In the `allie/flowkit/models` directory, create a new Python file named `custom_model.py`.

    **custom_model.py**:
    ```python
    from pydantic import BaseModel


    class CustomRequest(BaseModel):
        """Model for the input data required for the custom function.

        Parameters
        ----------
        BaseModel : pydantic.BaseModel
            Base model for the request.

        """

        input_data: str


    class CustomResponse(BaseModel):
        """Model for the output data of the custom function.

        Parameters
        ----------
        BaseModel : pydantic.BaseModel
            Base model for the response.

        """

        output_data: str
    ```

3. **Define your custom function:**
- Add your function to ``custom_endpoint.py``, explicitly defining the input and output using Pydantic models, and the category and display name of the function.

    **custom_endpoint.py**:
    ```python
    from fastapi import FastAPI, APIRouter
    from allie.flowkit.models.custom_model import CustomRequest, CustomResponse


    @router.post("/custom_function", response_model=CustomResponse)
    @category(FunctionCategory.GENERIC)
    @display_name("Custom Function")
    async def custom_function(request: CustomRequest) -> CustomResponse:
        """Endpoint for custom function.

        Parameters
        ----------
        request : CustomRequest
            Object containing the input data required for the function.

        Returns
        -------
        CustomResponse
            Object containing the output data of the function.

        """
        # Your custom processing logic here
        result = ...
        return result
    ```

4. **Import the module and add the router to the service:**
- Import the module in the ``allie/flowkit/flowkit_service.py`` file and add the router to the service.

    **flowkit_service.py**:
    ```python
    from allie.flowkit.endpoints import custom_endpoint

    flowkit_servie.include_router(splitter.router, prefix="/splitter", tags=["splitter"])
    flowkit_servie.include_router(
        custom_endpoint.router, prefix="/custom_endpoint", tags=["custom_endpoint"]
    )
    ```

5. **Add the function to the function map:**
- Add your function to the ``function_map`` dictionary in the ``allie/flowkit/flowkit_service.py`` file.

    **flowkit_service.py**:
    ```python
    function_map = {
        "split_ppt": splitter.split_ppt,
        "split_pdf": splitter.split_pdf,
        "split_py": splitter.split_py,
        "custom_function": custom_endpoint.custom_function,
    }
    ```

## Example functions

The repository includes some standard functions prefilled by the Allie team. You can use these as references or starting points for adding your own custom functions.

## Contributing

We welcome contributions from all teams. To contribute, perform these steps:

1. Clone the repository.
2. Create a branch for your feature or bug fix.
3. Commit your changes and push your branch to the repository.
4. Open a pull request to merge your changes into the main repository.

---

Thank you for using Allie FlowKit Python. We hope this repository helps you create powerful and flexible Allie workflows. Happy coding!
