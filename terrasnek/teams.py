"""
Module for Terraform Cloud API Endpoint: Teams.
"""

from .endpoint import TFCEndpoint
from ._constants import Entitlements

class TFCTeams(TFCEndpoint):
    """
    The Teams API is used to create, edit, and destroy teams as well as manage a team's
    organization-level permissions. The Team Membership API is used to add or remove users
    from a team. Use the Team Access API to associate a team with privileges on an
    individual workspace.

    `API Docs \
        <https://www.terraform.io/docs/cloud/api/teams.html>`_
    """

    def __init__(self, instance_url, org_name, headers, well_known_paths, verify, log_level):
        super().__init__(instance_url, org_name, headers, well_known_paths, verify, log_level)
        self._teams_api_v2_base_url = f"{self._api_v2_base_url}/teams"
        self._org_api_v2_base_url = f"{self._api_v2_base_url}/organizations/{org_name}/teams"

    def required_entitlements(self):
        return [Entitlements.TEAMS]

    def create(self, payload):
        """
        ``POST /organizations/:organization_name/teams``

        `API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/teams.html#create-a-team>`_

        `Sample payload \
            <https://www.terraform.io/docs/cloud/api/teams.html#sample-payload>`_
        """
        return self._create(self._org_api_v2_base_url, payload)

    def destroy(self, team_id):
        """
        ``DELETE /teams/:team_id``

        `API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/teams.html#delete-a-team>`_
        """
        url = f"{self._teams_api_v2_base_url}/{team_id}"
        return self._destroy(url)

    def list(self):
        """
        ``GET organizations/:organization_name/teams``

        `API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/teams.html#list-teams>`_
        """
        return self._list(self._org_api_v2_base_url)

    def show(self, team_id):
        """
        ``GET /teams/:team_id``

        `API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/teams.html#show-team-information>`_
        """
        url = f"{self._teams_api_v2_base_url}/{team_id}"
        return self._show(url)

    def update(self, team_id, payload):
        """
        ``PATCH /teams/:team_id``

        `API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/teams.html#update-a-team>`_

        `Sample payload \
            <https://www.terraform.io/docs/cloud/api/teams.html#sample-payload-1>`_
        """
        url = f"{self._teams_api_v2_base_url}/{team_id}"
        return self._update(url, payload)
