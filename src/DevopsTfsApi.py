from src.getaccess import GetAccess
import requests
from requests_ntlm import HttpNtlmAuth
import warnings
import contextlib
from urllib3.exceptions import InsecureRequestWarning
import urllib3

urllib3.disable_warnings()
old_merge_environment_settings = requests.Session.merge_environment_settings

class DevopsTfsApi(object):
    @contextlib.contextmanager
    def no_ssl_verification(self):
        opened_adapters = set()

        def merge_environment_settings(self, url, proxies, stream, verify, cert):
            # Verification happens only once per connection so we need to close
            # all the opened adapters once we're done. Otherwise, the effects of
            # verify=False persist beyond the end of this context manager.
            opened_adapters.add(self.get_adapter(url))

            settings = old_merge_environment_settings(self, url, proxies, stream, verify, cert)
            settings['verify'] = False

            return settings

        requests.Session.merge_environment_settings = merge_environment_settings

        try:
            with warnings.catch_warnings():
                warnings.simplefilter('ignore', InsecureRequestWarning)
                yield
        finally:
            requests.Session.merge_environment_settings = old_merge_environment_settings

            for adapter in opened_adapters:
                try:
                    adapter.close()
                except:
                    pass

#class DevopsTfsApi(object):
    def __init__(self, tfs_url, api_version):
        self.tfs_url = tfs_url
        self.api_version = api_version
        access = GetAccess()
        self.un = access.parse_yaml('tfsaccess', 'username')
        self.pw = access.parse_yaml('tfsaccess', 'password')

    def get_all_projects(self,collection_name):
        tfs_api = self.tfs_url + collection_name + '/_apis/projects?' + self.api_version
        return requests.get(tfs_api, auth=HttpNtlmAuth(self.un, self.pw), verify=False).json()

    def get_release_metric(self, collection_name, project_name, release_id):
        tfs_api = self.tfs_url + collection_name + '/' + project_name + '/_apis/release/releases?$expand=environments&definitionId=' + release_id + '&' + self.api_version
        """print(tfs_api)"""
        return requests.get(tfs_api, auth=HttpNtlmAuth(self.un, self.pw),verify=False).json()

    def get_release_id(self, collection_name, project_name):
        tfs_api = self.tfs_url + collection_name + '/' + project_name + '/_apis/release/definitions?' + self.api_version +'&$top=1000000'
        """print(tfs_api)"""
        return requests.get(tfs_api, auth=HttpNtlmAuth(self.un, self.pw),verify=False).json()

    def getAllRepos(self,collection_name):
        tfs_api = self.tfs_url + collection_name + "/_apis/git/repositories?" + self.api_version +'&$top=1000000'
        return requests.get(tfs_api, auth=HttpNtlmAuth(self.un, self.pw),verify=False).json()

    def get_allrepos_project(self,collection_name, project_name):
        tfs_api = self.tfs_url + collection_name + '/' + project_name + '/_apis/git/repositories?' + self.api_version
        return requests.get(tfs_api, auth=HttpNtlmAuth(self.un, self.pw),verify=False).json()

    def getMetricCommit(self,collection_name, repo_ID):
        tfs_api = self.tfs_url + collection_name + '/_apis/git/repositories/' + str(repo_ID) + \
                  '/commits?searchCriteria.fromDate=2019-01-01&$top=10000000000&'+ self.api_version
        return requests.get(tfs_api, auth=HttpNtlmAuth(self.un, self.pw),verify=False).json()

    def getMetricChangeset(self, collection_name, csID):
        tfs_api = self.tfs_url + collection_name + '/_apis/tfvc/changesets/'+ str(csID) + \
                  '/changes?fromDate=2018-02-01&toDate=2018-03-01&$top=1000000&' + self.api_version
        return requests.get(tfs_api, auth=HttpNtlmAuth(self.un, self.pw),verify=False).json()

    def getFirstChangeset(self, collection_name):
        tfs_api = self.tfs_url + collection_name + '/_apis/tfvc/changesets?fromDate=2018-02-01&toDate=2018-03-01&$top=1000000'
        return requests.get(tfs_api, auth=HttpNtlmAuth(self.un, self.pw),verify=False).json()

    def getListofBuilds(self, collection_name, project_name):
        tfs_api = self.tfs_url + collection_name + '/' + project_name + '/_apis/build/definitions?'+ self.api_version
        return requests.get(tfs_api, auth=HttpNtlmAuth(self.un, self.pw),verify=False).json()

    def getPropertiesofBuilds(self, collection_name, project_name, build_id):
        tfs_api = self.tfs_url + collection_name + '/' + project_name + '/_apis/build/definitions/' + str(build_id)+'?' + self.api_version
        return requests.get(tfs_api, auth=HttpNtlmAuth(self.un, self.pw),verify=False).json()

    def get_build_metric(self, collection_name, project_name, build_id):
        tfs_api = self.tfs_url + collection_name + '/' + project_name + "/_apis/build/builds?definitions=" + str(build_id) + "&statusFilter=completed"
        return requests.get(tfs_api, auth=HttpNtlmAuth(self.un, self.pw),verify=False).json()

    def getPropertiesofReleases(self, collection_name, project_name, release_id):
        tfs_api = self.tfs_url + collection_name + '/' + project_name + '/_apis/release/definitions/' + str(release_id)+'?'+ self.api_version
        return requests.get(tfs_api, auth=HttpNtlmAuth(self.un, self.pw), verify=False).json()

    def get_all_Xaml_builds(self, collection_name, project_name):
        tfs_api = self.tfs_url + collection_name + '/' + project_name + "/_apis/build/builds?" + self.api_version
        return requests.get(tfs_api, auth=HttpNtlmAuth(self.un, self.pw),verify=False).json()

    def get_all_XAML_def(self, collection_name, project_name):
        tfs_api = self.tfs_url + collection_name + '/' + project_name + "/_apis/build/definitions?" + self.api_version
        return requests.get(tfs_api, auth=HttpNtlmAuth(self.un, self.pw),verify=False).json()

    def get_XAML_Requests(self, collection_name, project_name):
        tfs_api = self.tfs_url + collection_name + '/' + project_name + "/_apis/build/requests?status=Completed&" + self.api_version
        return requests.get(tfs_api, auth=HttpNtlmAuth(self.un, self.pw),verify=False).json()

    def get_all_Branches(self, collection_name):
        tfs_api = self.tfs_url + collection_name + '/' + "/_apis/branches?" + self.api_version
        return requests.get(tfs_api, auth=HttpNtlmAuth(self.un, self.pw),verify=False).json()

    def getCSbyBranch(self, collection_name, branch):
        tfs_api = self.tfs_url + collection_name + '/_apis/tfvc/changesets?searchCriteria.versionType='+branch+'&fromDate=2018-02-01&toDate=2018-03-01&$top=1000000'
        return requests.get(tfs_api, auth=HttpNtlmAuth(self.un, self.pw),verify=False).json()

    def getServiceEndpoints(self, collection_name, project_name):
        tfs_api = self.tfs_url + collection_name + '/' + project_name +"/_apis/serviceendpoint/endpoints?" + self.api_version + '-preview.1&$top=1000000'
        return requests.get(tfs_api, auth=HttpNtlmAuth(self.un, self.pw),verify=False).json()

    def getListofReleases(self, collection_name, project_name):
        tfs_api = self.tfs_url + collection_name + '/' + project_name + '/_apis/release/definitions?'+ self.api_version +'&$top=1000000'
        return  requests.get(tfs_api, auth=HttpNtlmAuth(self.un, self.pw),verify=False).json()

    def getListofPolicyConfiguration(self, collection_name, project_name):
        tfs_api = self.tfs_url + collection_name + '/' + project_name +'/_apis/policy/configurations?' + self.api_version
        return requests.get(tfs_api, auth=HttpNtlmAuth(self.un, self.pw),verify=False).json()
    
    def getListofPolicyConfigurationWithScopeRepoID(self, collection_name, project_name,repoID,branchName):
        tfs_api = self.tfs_url + collection_name + '/' + project_name +'/_apis/policy/configurations?vctype=git&scope='+repoID+'%3Arefs%2Fheads%2F'+branchName+'&' + self.api_version
        return requests.get(tfs_api, auth=HttpNtlmAuth(self.un, self.pw),verify=False).json()

    def getRepoProperty(self,collection_name,project_name,repository_id):
        tfs_api = self.tfs_url + collection_name+ '/' + project_name + '/_apis/git/repositories/'+repository_id+"?" + self.api_version
        return requests.get(tfs_api, auth=HttpNtlmAuth(self.un, self.pw),verify=False).json()
    
    def getAllPRonProject(self,collection_name,project_name):
        tfs_api = self.tfs_url + collection_name + '/' + project_name+ "/_apis/git/pullrequests?" + self.api_version +'&$top=1000000'
        return requests.get(tfs_api, auth=HttpNtlmAuth(self.un, self.pw),verify=False).json()
    
    def getAllPRonProjectbyReviewerbyStatus(self,collection_name,project_name, status, reviewerID):
        tfs_api = self.tfs_url + collection_name + '/' + project_name+ '/_apis/git/pullrequests?searchCriteria.status='+status+'&active&searchCriteria.reviewerId='+ reviewerID +'&' + self.api_version
        return requests.get(tfs_api, auth=HttpNtlmAuth(self.un, self.pw),verify=False).json()
    
    def getEvaluationsonPRbyArtficatID(self,collection_name,project_name,projectId, pullRequestId):
        tfs_api = self.tfs_url + collection_name + '/' + project_name+ '/_apis/policy/evaluations?artifactId=vstfs:///CodeReview/CodeReviewId/'+projectId+'/'+pullRequestId+'&'+ self.api_version+'-preview.1'
        return requests.get(tfs_api, auth=HttpNtlmAuth(self.un, self.pw),verify=False).json()

