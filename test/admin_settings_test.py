"""
Module for testing the Terraform Cloud API Endpoint: Admin Settings.
"""

from .base import TestTFCBaseTestCase

import random


class TestTFCAdminSettings(TestTFCBaseTestCase):
    """
    Class for testing the Terraform Cloud API Endpoint: Admin Settings.
    """

    def test_admin_settings_general(self):
        """
        Test the Admin Settings API endpoints: list_general, update_general.
        """
        all_general = self._api.admin_settings.list_general()["data"]
        self.assertEqual("general-settings", all_general["type"])

        updated_rate_limit = random.randint(45, 60)
        update_payload = {
            "data": {
                "attributes": {
                    "api-rate-limiting-enabled": True,
                    "api-rate-limit": updated_rate_limit
                }
            }
        }
        updated_settings = self._api.admin_settings.update_general(update_payload)["data"]
        self.assertEqual(updated_rate_limit, updated_settings["attributes"]["api-rate-limit"])

    def test_admin_settings_cost_estimation(self):
        """
        Test the Admin Settings API endpoints: list_cost_estimation,
        update_cost_estimation.
        """

        all_cost_est = self._api.admin_settings.list_cost_estimation()["data"]
        self.assertEqual("cost-estimation-settings", all_cost_est["type"])

        update_payload = {
            "data": {
                "attributes": {
                    "enabled": True,
                    "aws-enabled": True,
                    "aws-access-key-id": "foo",
                    "aws-secret-key": "bar"
                }
            }
        }
        updated_cost_est = self._api.admin_settings.update_cost_estimation(update_payload)["data"]
        self.assertTrue(updated_cost_est["attributes"]["enabled"])
        self.assertTrue(updated_cost_est["attributes"]["aws-enabled"])

    def test_admin_settings_saml(self):
        """
        Test the Admin Settings API endpoints: list_saml, update_saml,
        revoke_previous_saml_idp_cert.
        """
        all_saml = self._api.admin_settings.list_saml()["data"]
        self.assertEqual("saml-settings", all_saml["type"])

        update_payload = {
            "data": {
                "attributes": {
                    "enabled": True,
                    "debug": False,
                    "idp-cert": "NEW-CERTIFICATE",
                    "slo-endpoint-url": "https://example.com/slo",
                    "sso-endpoint-url": "https://example.com/sso",
                    "attr-username": "Username",
                    "attr-groups": "MemberOf",
                    "attr-site-admin": "SiteAdmin",
                    "site-admin-role": "site-admins",
                    "sso-api-token-session-timeout": 1209600
                }
            }
        }
        updated_saml = self._api.admin_settings.update_saml(update_payload)["data"]
        self.assertTrue(updated_saml["attributes"]["enabled"])

        # TODO: revoke_previous_saml_idp_cert

    def test_admin_settings_smtp(self):
        """
        Test the Admin Settings API endpoints: list_smtp, update_smtp.
        """
        all_smtp = self._api.admin_settings.list_smtp()["data"]
        self.assertEqual("smtp-settings", all_smtp["type"])

        update_payload = {
            "data": {
                "attributes": {
                    "enabled": True,
                    "host": "example.com",
                    "port": 25,
                    "sender": "sample_user@example.com",
                    "auth": "login",
                    "username": "sample_user",
                    "password": "sample_password",
                    "test-email-address": "test@example.com"
                }
            }
        }

        # TODO: When a request to this endpoint is submitted, a test message will be
        # sent to the specified test-email-address. If the test message delivery fails,
        # the API will return an error code indicating the reason for the failure.

        # updated_smtp = self._api.admin_settings.update_smtp(update_payload)["data"]
        # self.assertTrue(updated_smtp["attributes"]["enabled"])

    def test_admin_settings_twilio(self):
        """
        Test the Admin Settings API endpoints: list_twilio, update_twilio,
        verify_twilio.
        """
        all_twilio = self._api.admin_settings.list_twilio()["data"]
        self.assertEqual("twilio-settings", all_twilio["type"])

        """
        # TODO: need to use a real twilio account to verify against here.

        update_payload = {
            "data": {
                "attributes": {
                    "enabled": True,
                    "account-sid": "12345abcd",
                    "auth-token": "sample_token",
                    "from-number": "555-555-5555"
                }
            }
        }

        updated_twilio = self._api.admin_settings.update_twilio(update_payload)["data"]
        print(updated_twilio)
        self.assertTrue(updated_twilio["attributes"]["enabled"])

        verify_payload = {
            "data": {
                "attributes": {
                "test-number": "555-555-0000"
                }
            }
        }
        verified_twilio = self._api.admin_settings.verify_twilio(verify_payload)
        print(verified_twilio)
        """

    def test_admin_settings_customization(self):
        """
        Test the Admin Settings API endpoints: list_customization,
        update_customization.
        """
        all_customization = self._api.admin_settings.list_customization()["data"]
        self.assertEqual("customization-settings", all_customization["type"])

        # Update the support email, confirm it works
        email_to_update_to = "foo@bar.com"
        update_payload = {
            "data": {
                "attributes": {
                    "support-email-address": email_to_update_to
                }
            }
        }
        updated_customization = self._api.admin_settings.update_customization(update_payload)["data"]
        self.assertEqual(email_to_update_to, updated_customization["attributes"]["support-email-address"])