from src.DevopsTfsApi import DevopsTfsApi
import csv

tfs = DevopsTfsApi(tfs_url='https://{instance}/', api_version='api-version=6.1')
collectionName = 'Default_Collection'
project_Name = ['AI', 'Backend', 'Web']

file = csv.writer(open('D:/Repos/rapor/AzureDevopsRepos.csv', 'w', encoding='utf16'), delimiter='\t', lineterminator='\n')
file.writerow(["Project Name","Repo ID","Repo Name"])
for pj in project_Name:
    repos = tfs.get_allrepos_project(collectionName,pj)
    for repo in repos['value']:
        print(pj,repo['id'],repo['name'])
        lines= (pj, repo['id'],repo['name'])
        file.writerow(lines)
