# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

import os

from azure.identity import DefaultAzureCredential
from azure.mgmt.containerservice import ContainerServiceClient
from dotenv import load_dotenv

load_dotenv()

def main():
    # Create client
    # # For other authentication approaches, please see: https://pypi.org/project/azure-identity/
    client = ContainerServiceClient(
        credential=DefaultAzureCredential(),
        subscription_id='60f3ac75-ce11-4deb-9030-d3896b73c46c'
    )

    # Get versions
    result = client.container_services.list_orchestrators(location="eastus", resource_type="managedClusters")
    print(result.serialize())


if __name__ == "__main__":
    main()
