"""
Module for Terraform Cloud API Endpoint: Policies.
"""

from .endpoint import TFCEndpoint
from ._constants import Entitlements

class TFCPolicies(TFCEndpoint):
    """
    Policies are configured on a per-organization level and are organized
    and grouped into policy sets, which define the workspaces on which
    policies are enforced during runs. In these workspaces, the plan's changes
    are validated against the relevant policies after the plan step.

    `API Docs \
        <https://www.terraform.io/docs/cloud/api/policies.html>`_
    """
    def __init__(self, instance_url, org_name, headers, well_known_paths, verify, log_level):
        super().__init__(instance_url, org_name, headers, well_known_paths, verify, log_level)
        self._endpoint_base_url = f"{self._api_v2_base_url}/policies"
        self._org_api_v2_base_url = f"{self._api_v2_base_url}/organizations/{org_name}/policies"

    def required_entitlements(self):
        return [Entitlements.SENTINEL]

    def create(self, payload):
        """
        ``POST /organizations/:organization_name/policies``

        `API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/policies.html#create-a-policy>`_

        This creates a new policy object for the organization, but does not upload
        the actual policy code

        `Sample payload \
            <https://www.terraform.io/docs/cloud/api/policies.html#sample-payload>`_
        """
        return self._create(self._org_api_v2_base_url, payload)

    def list(self, page=None, page_size=None, search=None):
        """
        ``GET /organizations/:organization_name/policies``

        `API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/policies.html#list-policies>`_

        Query parameter(s) (`details \
            <https://www.terraform.io/docs/cloud/api/policies.html#query-parameters>`_):
            - ``page`` (Optional)
            - ``page_size`` (Optional)
            - ``search`` (Optional)
        """
        return self._list(\
            self._org_api_v2_base_url, page=page, page_size=page_size, search=search)

    def show(self, policy_id):
        """
        ``GET /policies/:policy_id``

        `API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/policies.html#show-a-policy>`_
        """
        url = f"{self._endpoint_base_url}/{policy_id}"
        return self._show(url)

    def update(self, policy_id, payload):
        """
        ``PATCH /policies/:policy_id``

        `API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/policies.html#update-a-policy>`_

        This endpoint can update the enforcement mode of an existing policy. To
        update the policy code itself, use the upload endpoint.

        `Sample payload \
            <https://www.terraform.io/docs/cloud/api/policies.html#sample-payload-2>`_
        """
        url = f"{self._endpoint_base_url}/{policy_id}"
        return self._update(url, payload)

    def upload(self, policy_id, payload):
        """
        ``PUT /policies/:policy_id/upload``

        `API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/policies.html#upload-a-policy>`_

        This endpoint uploads code to an existing Sentinel policy.

        `Sample payload \
            <https://www.terraform.io/docs/cloud/api/policies.html#sample-payload-1>`_
        """
        url = f"{self._endpoint_base_url}/{policy_id}/upload"
        return self._put(url, octet=True, data=payload)

    def destroy(self, policy_id):
        """
        ``DELETE /policies/:policy_id``

        `API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/policies.html#delete-a-policy>`_
        """
        url = f"{self._endpoint_base_url}/{policy_id}"
        return self._destroy(url)
