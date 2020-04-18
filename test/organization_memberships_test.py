"""
Module for testing the Terraform Cloud API Endpoint: Organization Memberships.
"""

from .base import TestTFCBaseTestCase


class TestTFCOrganizationMemberships(TestTFCBaseTestCase):
    """
    Class for testing the Terraform Cloud API Endpoint: Organization Membershipsl.
    """

    def setUp(self):
        # TODO: figure out how to make these not spammy or burdensome
        org_create_payload = self._get_org_create_payload()
        self._created_org = self._api.organizations.create(org_create_payload)
        self._created_org_name = org_create_payload["data"]["attributes"]["name"]
        self._created_org_id = self._created_org["data"]["id"]

    def tearDown(self):
        self._api.organizations.destroy(self._created_org_name)

    def test_org_memberships_lifecycle(self):
        """
        Test the Organization Memberships API endpoints: invite, lst_for_org,
        lst_for_user, show, remove.
        """

        # Get the existing org memberships for the logged in user
        orgs_for_user = self._api.organization_memberships.lst_for_user()
        num_org_memberships = len(orgs_for_user["data"])
        self.assertEqual(num_org_memberships, 2)

        # Get teams for created org
        self._api.set_organization(self._created_org_id)
        teams = self._api.teams.lst()
        owners_team = teams["data"][0]
        owners_team_id = owners_team["id"]

        # Invite a user
        invite_payload = self._get_org_membership_invite_payload(owners_team_id)
        invite = self._api.organization_memberships.invite(invite_payload)
        invited_user_email = invite["data"]["attributes"]["email"]
        self.assertEqual(invited_user_email, self._test_email)

        # Show a user's org membership using the org membership ID
        org_membership_id = invite["data"]["id"]
        shown_membership = self._api.organization_memberships.show(org_membership_id)
        shown_membership_id = shown_membership["data"]["id"]
        self.assertEqual(org_membership_id, shown_membership_id)

        # List all users for the org we configured the client for
        users_for_org = self._api.organization_memberships.lst_for_org()
        num_users_in_org = len(users_for_org["data"])
        self.assertEqual(num_users_in_org, 2)

        # Remove the user
        removal = self._api.organization_memberships.remove(org_membership_id)
        users_for_org = self._api.organization_memberships.lst_for_org()
        num_users_in_org = len(users_for_org["data"])
        self.assertEqual(num_users_in_org, 1)