import unittest
import os
from .base import TestTFEBaseTestCase

from terrasnek.api import TFE

class TestTFETeamTokens(TestTFEBaseTestCase):

    @classmethod
    def setUpClass(self):
        super(TestTFETeamTokens, self).setUpClass()
        self._team = self._api.teams.create(self._team_create_payload)["data"]
        self._team_id = self._team["id"]

    @classmethod
    def tearDownClass(self):
        self._api.teams.destroy(self._team_id)

    def test_team_token_lifecycle(self):
        # Create a test token and make sure we get an ID back
        created_token = self._api.team_tokens.create(self._team_id)["data"]
        self.assertIsNotNone(created_token["id"])

        # Then destroy it. There is no lookup so there's nothing to test here. 
        self._api.team_tokens.destroy(self._team_id)