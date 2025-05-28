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

"""Module for reading the configuration settings from a YAML file."""

import json
import os
from pathlib import Path

from azure.identity import ManagedIdentityCredential
from azure.keyvault.secrets import SecretClient
import yaml


class Config:
    """Represent the configuration settings.

    Attributes
    ----------
    flowkit_python_api_key : str
        The API key for accessing the Aali Flowkit Python service.

    Methods
    -------
    _load_config(config_path: str) -> dict
        Read the YAML configuration file and return its content as
        a dictionary.

    """

    def __init__(self):
        """Initialize the Config object by reading the configuration file.

        Also, check if the 'FLOWKIT_PYTHON_API_KEY' is present in the
        configuration file.

        Raises
        ------
        ValueError
            If the 'FLOWKIT_PYTHON_API_KEY' is not found in the
            configuration file.

        """
        config_path = os.getenv("Aali_CONFIG_PATH", "config.yaml")
        self._yaml = self._load_config(config_path)

        # Define the configuration variables to be parsed from the YAML file
        self.flowkit_python_api_key = str(self._yaml.get("FLOWKIT_PYTHON_API_KEY", ""))
        self.flowkit_python_address = str(self._yaml.get("FLOWKIT_PYTHON_ADDRESS"))
        self.flowkit_python_endpoint = str(self._yaml.get("FLOWKIT_PYTHON_ENDPOINT", "http://localhost:50052"))
        self.flowkit_python_workers = int(self._yaml.get("FLOWKIT_PYTHON_WORKERS", 4))
        self.use_ssl = bool(self._yaml.get("USE_SSL", False))
        self.ssl_cert_public_key_file = str(self._yaml.get("SSL_CERT_PUBLIC_KEY_FILE", ""))
        self.ssl_cert_private_key_file = str(self._yaml.get("SSL_CERT_PRIVATE_KEY_FILE", ""))
        self.extract_config_from_azure_key_vault = bool(self._yaml.get("EXTRACT_CONFIG_FROM_AZURE_KEY_VAULT", False))
        self.azure_managed_identity_id = str(self._yaml.get("AZURE_MANAGED_IDENTITY_ID", ""))
        self.azure_key_vault_name = str(self._yaml.get("AZURE_KEY_VAULT_NAME", ""))

        # If azure key vault configured, read values from vault
        if self.extract_config_from_azure_key_vault:
            self._get_config_from_azure_key_vault()

        # Check the mandatory configuration variables
        if not self.flowkit_python_api_key:
            raise ValueError("FLOWKIT_PYTHON_API_KEY is missing in the configuration file.")

    def _load_config(self, config_path: str) -> dict:
        """Read the YAML configuration file.

        Parameters
        ----------
        config_path : str
            The path to the YAML configuration file.

        Returns
        -------
        dict
            The content of the configuration file as a dictionary.

        Raises
        ------
        FileNotFoundError
            If the configuration file is not found at the given path.

        """
        try:
            with Path(config_path).open("r") as file:
                return yaml.safe_load(file)
        except FileNotFoundError:
            print(f"Configuration file not found at: {config_path}, using default location.")
            try:
                with Path("configs/config.yaml").open("r") as file:
                    return yaml.safe_load(file)
            except FileNotFoundError:
                try:
                    with Path("../../configs/config.yaml").open("r") as file:
                        return yaml.safe_load(file)
                except FileNotFoundError:
                    raise FileNotFoundError("Configuration file not found at the default location.")

    def _get_config_from_azure_key_vault(self):
        """Extract configuration from Azure Key Vault and set attributes."""
        # Get environment variables
        azure_managed_identity_id = os.getenv(self.azure_managed_identity_id)
        azure_key_vault_name = os.getenv(self.azure_key_vault_name)

        # Check if all required environment variables are set
        if not azure_managed_identity_id:
            raise ValueError(f"Environment variable for {self.azure_managed_identity_id} is not set")
        if not azure_key_vault_name:
            raise ValueError(f"Environment variable for {self.azure_key_vault_name} is not set")

        # Create Key Vault URL
        key_vault_url = f"https://{azure_key_vault_name}.vault.azure.net/"

        # Create Managed Identity credential
        credential = ManagedIdentityCredential(client_id=azure_managed_identity_id)

        # Test the managed identity by getting a token
        scope = "https://vault.azure.net/.default"
        token = credential.get_token(scope)
        if not token:
            raise ValueError("Failed to get token from managed ID")

        # Create Azure Key Vault SecretClient
        client = SecretClient(vault_url=key_vault_url, credential=credential)

        # List all secrets
        secret_properties = client.list_properties_of_secrets()

        # Reflect on the fields of the Config class
        global_config_fields = {field: value for field, value in self.__dict__.items() if not field.startswith("_")}

        # Iterate over all secrets
        for secret_property in secret_properties:
            secret_name = secret_property.name
            secret_value = client.get_secret(secret_name).value

            # Format the field name to match the secret name format
            formatted_field_name = secret_name.replace("_", "").upper()

            # Match secret names to Config class fields and set values
            for field_name in global_config_fields:
                # Remove underscores and convert to uppercase for matching
                if field_name.replace("_", "").upper() == formatted_field_name:
                    # Handle different field types
                    field_type = type(getattr(self, field_name))
                    if field_type is str:
                        setattr(self, field_name, secret_value)
                    elif field_type is bool:
                        setattr(self, field_name, secret_value.lower() == "true")
                    elif field_type is int:
                        setattr(self, field_name, int(secret_value))
                    elif field_type is list:
                        setattr(self, field_name, json.loads(secret_value))
                    else:
                        raise ValueError(f"Unsupported field type: {field_type}")


# Initialize the config object
CONFIG = Config()
