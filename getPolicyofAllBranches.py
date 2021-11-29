from src.DevopsTfsApi import DevopsTfsApi
import csv

tfs = DevopsTfsApi(tfs_url='https://{instance}/', api_version='api-version=6.0')
collectionName = 'Default_Collection'
project_Name = ['AI','Backend', 'Web']

#for write tp csv file
file = csv.writer(open('D:/Repos/rapor/AzureDevopsRepoPolicys.csv', 'w', encoding='utf16'), delimiter='\t', lineterminator='\n')
file.writerow(["RepoID","Project Name","refName", "matchKind", "typeDisplayName","isEnabled"])
#for write to txt file
#file = open('D:/cikti/AzureDevopsBuildOpVariables.txt', 'w', encoding="utf-8")
for pj in project_Name:
    policys = tfs.getListofPolicyConfiguration(collectionName, pj)
    for policy in policys['value']:
        typeDisplayName=policy['type']['displayName']
        if typeDisplayName == "Build":
            isEnabled= policy['isEnabled']
            RepoID = policy['settings']['scope'][0]['repositoryId']
            refName = policy['settings']['scope'][0]['refName']
            matchKind = policy['settings']['scope'][0]['matchKind']
            print(RepoID,pj,refName,matchKind,typeDisplayName,isEnabled)
            lines= (RepoID,pj,refName,matchKind,typeDisplayName,isEnabled)
            file.writerow(lines)
        elif typeDisplayName == "Comment requirements":
            isEnabled= policy['isEnabled']
            RepoID = policy['settings']['scope'][0]['repositoryId']
            refName = policy['settings']['scope'][0]['refName']
            matchKind = policy['settings']['scope'][0]['matchKind']
            print(RepoID,pj,refName,matchKind,typeDisplayName,isEnabled)
            lines= (RepoID,pj,refName,matchKind,typeDisplayName,isEnabled)
            file.writerow(lines)
        elif typeDisplayName == "Require a merge strategy":
            isEnabled= policy['isEnabled']
            RepoID = policy['settings']['scope'][0]['repositoryId']
            refName = policy['settings']['scope'][0]['refName']
            matchKind = policy['settings']['scope'][0]['matchKind']
            print(RepoID,pj,refName,matchKind,typeDisplayName,isEnabled)
            lines= (RepoID,pj,refName,matchKind,typeDisplayName,isEnabled)
            file.writerow(lines)
        elif typeDisplayName == "Minimum number of reviewers":
            isEnabled= policy['isEnabled']
            RepoID = policy['settings']['scope'][0]['repositoryId']
            refName = policy['settings']['scope'][0]['refName']
            matchKind = policy['settings']['scope'][0]['matchKind']
            print(RepoID,pj,refName,matchKind,typeDisplayName,isEnabled)
            lines= (RepoID,pj,refName,matchKind,typeDisplayName,isEnabled)
            file.writerow(lines)
        elif typeDisplayName == "Work item linking":
            isEnabled= policy['isEnabled']
            RepoID = policy['settings']['scope'][0]['repositoryId']
            refName = policy['settings']['scope'][0]['refName']
            matchKind = policy['settings']['scope'][0]['matchKind']
            print(RepoID,pj,refName,matchKind,typeDisplayName,isEnabled)
            lines= (RepoID,pj,refName,matchKind,typeDisplayName,isEnabled)
            file.writerow(lines)
        elif typeDisplayName == "Required reviewers":
            isEnabled= policy['isEnabled']
            RepoID = policy['settings']['scope'][0]['repositoryId']
            refName = policy['settings']['scope'][0]['refName']
            matchKind = policy['settings']['scope'][0]['matchKind']
            print(RepoID,pj,refName,matchKind,typeDisplayName,isEnabled)
            lines= (RepoID,pj,refName,matchKind,typeDisplayName,isEnabled)
            file.writerow(lines)
