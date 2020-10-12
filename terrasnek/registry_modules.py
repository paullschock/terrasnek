"""
Module for Terraform Cloud API Endpoint: Registry Modules.
"""

from .endpoint import TFCEndpoint
from ._constants import Entitlements

class TFCRegistryModules(TFCEndpoint):
    """
    The Terraform Cloud Module Registry implements the Registry standard API
    for consuming the modules, both public and private.

    `API Docs (Private Registry) \
        <https://www.terraform.io/docs/cloud/api/modules.html>`_

    `API Docs (Public Registry) \
        <https://www.terraform.io/docs/registry/api.html>`_
    """

    def __init__(self, instance_url, org_name, headers, well_known_paths, verify, log_level):
        super().__init__(instance_url, org_name, headers, well_known_paths, verify, log_level)
        self._modules_v2_base_url = f"{self._api_v2_base_url}/registry-modules"
        self._modules_v1_base_url = f"{self._modules_v1_base_url}"
        self._org_api_v2_base_url = f"{self._api_v2_base_url}/organizations"

    def required_entitlements(self):
        return [Entitlements.PRIVATE_MODULE_REGISTRY]

    # Public Registry API Endpoints
    def list(self, offset=None, limit=None, provider=None, verified=None):
        """
        https://www.terraform.io/docs/registry/api.html#list-modules
        ``GET <base_url>``
        ``GET <base_url>/:namespace``

        `API Doc Reference \
            <https://www.terraform.io/docs/registry/api.html#list-modules>`_
        """
        url = f"{self._modules_v1_base_url}/{self._org_name}"
        return self._list(\
            url, offset=offset, limit=limit, provider=provider, verified=verified)

    def search(self, query, offset=None, limit=None, provider=None, verified=None):
        """
        ``GET <base_url>/search``

        `API Doc Reference \
            <https://www.terraform.io/docs/registry/api.html#search-modules>`_
        """
        url = f"{self._modules_v1_base_url}/search"
        return self._list(url, \
            query=query, offset=offset, limit=limit, provider=provider,\
            verified=verified)

    def show(self, module_name, provider):
        """
        ``GET /registry-modules/show/:organization_name/:name/:provider``

        `API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/modules.html#show-a-module>`_
        """
        url = f"{self._modules_v2_base_url}/show/{self._org_name}/{module_name}/{provider}"
        return self._show(url)

    def list_versions(self, name, provider):
        """
        ``GET <base_url>/:namespace/:name/:provider/versions``

        `API Doc Reference \
            <https://www.terraform.io/docs/registry/api.html#list-available-versions-for-a-specific-module>`_
        """
        url = f"{self._modules_v1_base_url}/{self._org_name}/{name}/{provider}/versions"
        return self._get(url)

    def list_latest_version_all_providers(self, name, offset=None, limit=None):
        """
        ``GET <base_url>/:namespace/:name``

        `API Doc Reference \
            <https://www.terraform.io/docs/registry/api.html#list-latest-version-of-module-for-all-providers>`_
        """
        url = f"{self._modules_v1_base_url}/{self._org_name}/{name}"
        return self._list(url, offset=offset, limit=limit)

    def list_latest_version_specific_provider(self, name, provider):
        """
        ``GET <base_url>/:namespace/:name/:provider``

        `API Doc Reference \
            <https://www.terraform.io/docs/registry/api.html#latest-version-for-a-specific-module-provider>`_
        """
        url = f"{self._modules_v1_base_url}/{self._org_name}/{name}/{provider}"
        return self._get(url)

    def get(self, name, provider, version):
        """
        ``GET <base_url>/:namespace/:name/:provider/:version``

        `API Doc Reference \
            <https://www.terraform.io/docs/registry/api.html#get-a-specific-module>`_
        """
        url = f"{self._modules_v1_base_url}/{self._org_name}/{name}/{provider}/{version}"
        return self._get(url)

    def download_version_source(self, name, provider, version, target_path):
        """
        ``GET <base_url>/:namespace/:name/:provider/:version/download``

        `API Doc Reference \
            <https://www.terraform.io/docs/registry/api.html#download-source-code-for-a-specific-module-version>`_
        """
        url = f"{self._modules_v1_base_url}/{self._org_name}/{name}/{provider}/{version}/download"
        return self._download(url, target_path, header_with_url="X-Terraform-Get")

    def download_latest_source(self, name, provider, target_path):
        """
        ``GET <base_url>/:namespace/:name/:provider/download``

        `API Doc Reference \
            <https://www.terraform.io/docs/registry/api.html#download-the-latest-version-of-a-module>`_
        """
        url = f"{self._modules_v1_base_url}/{self._org_name}/{name}/{provider}/download"
        return self._download(\
            url, target_path, header_with_url="X-Terraform-Get", allow_redirects=True)

    # Private Registry API Endpoints
    def publish_from_vcs(self, payload):
        """
        ``POST /registry-modules``

        `API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/modules.html#publish-a-module-from-a-vcs>`_

        Publishes a new registry module from a VCS repository, with module
        versions managed automatically by the repository's tags. The publishing
        process will fetch all tags in the source repository that look like SemVer
        versions with optional 'v' prefix. For each version, the tag is cloned and
        the config parsed to populate module details (input and output variables,
        readme, submodules, etc.). The Module Registry Requirements define additional
        requirements on naming, standard module structure and tags for releases.

        `Sample payload \
            <https://www.terraform.io/docs/cloud/api/modules.html#sample-payload>`_
        """
        return self._post(self._modules_v2_base_url, data=payload)

    def destroy(self, name, provider=None, version=None):
        """
        ``POST /registry-modules/actions/delete/:organization_name/:name/:provider/:version``
        ``POST /registry-modules/actions/delete/:organization_name/:name/:provider``
        ``POST /registry-modules/actions/delete/:organization_name/:name``

        `API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/modules.html#delete-a-module>`_
        """
        url = f"{self._modules_v2_base_url}/actions/delete/{self._org_name}"

        if name:
            url += f"/{name}"
            if provider:
                url += f"/{provider}"
                if version:
                    url += f"/{version}"

        return self._post(url)

    def create(self, payload):
        """
        ``POST /organizations/:organization_name/registry-modules``

        `API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/modules.html#create-a-module`_

        Creates a new registry module without a backing VCS repository.
        After creating a module, a version must be created and uploaded in order to
        be usable. Modules created this way do not automatically update with new
        versions; instead, you must explicitly create and upload each new version
        with the Create a Module Version endpoint.

        `Sample payload \
            <https://www.terraform.io/docs/cloud/api/modules.html#request-body-1>`_
        """

        url = f"{self._org_api_v2_base_url}/{self._org_name}/registry-modules"
        return self._post(url, data=payload)


    def create_version(self, module_name, provider, payload):
        """
        ``POST /registry-modules/:organization_name/:name/:provider/versions``

        `API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/modules.html#create-a-module-version>`_

        Creates a new registry module version. This endpoint only applies
        to modules without a VCS repository; VCS-linked modules automatically create
        new versions for new tags. After creating the version, the module should be
        uploaded to the returned upload link.

        `Sample payload \
            <https://www.terraform.io/docs/cloud/api/modules.html#request-body-2>`_
        """

        url = f"{self._modules_v2_base_url}/{self._org_name}/{module_name}/{provider}/versions"
        return self._post(url, data=payload)

    def upload_version(self, path_to_tarball, upload_url):
        """
        ``PUT https://archivist.terraform.io/v1/object/<UNIQUE OBJECT ID>``

        `API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/modules.html#upload-a-module-version>`_

        The URL is provided in the upload links attribute in the
        registry-module-versions resource.
        """
        data = None

        with open(path_to_tarball, 'rb') as data_bytes:
            data = data_bytes.read()

        return self._put(upload_url, data=data)
