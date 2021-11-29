from src.DevopsTfsApi import DevopsTfsApi
import csv

tfs = DevopsTfsApi(tfs_url='https://{instance}/', api_version='api-version=6.0')
collectionName = 'Default_Collection'
projectName = 'AI'
devopsReviewerID = '****************' #id of reviewer, can get from a PR that the reviewer is already assigned

Dict={}
allPRsonDevops = tfs.getAllPRonProjectbyReviewerbyStatus(collectionName,projectName, 'active', devopsReviewerID)
for pr in allPRsonDevops['value']:
    myList = []
    pullRequestId = pr['pullRequestId']
    repoName = pr['repository']['name']
    projectID = pr['repository']['project']['id']
    creationDate = pr['creationDate']
    isDraft = pr['isDraft']
    revDisplayName = pr['reviewers'][0]['displayName']
    revvote= pr['reviewers'][0]['vote']
    if (revvote == 0):
        myList = [pullRequestId, repoName, projectID, creationDate[:10], isDraft, revDisplayName, revvote]
        Dict[pullRequestId] = myList
        #print(pullRequestId, repoName, projectID, creationDate[:10], isDraft, revDisplayName, revvote)
        
EvaluationDict ={}
for d in Dict.items():
    #print(d[0], d[1][2])
    evalutions = tfs.getEvaluationsonPRbyArtficatID(collectionName,'APIs',str(d[1][2]), str(d[0]))
    myList = []
    if (evalutions['count'] !=0):
        for ev in evalutions['value']:
            tempDict ={}
            status = ev['status']
            name = ev['configuration']['type']['displayName']
            tempDict[name]=status
            myList.insert(0, tempDict)
            #print(tempDict)
        print(myList)
        EvaluationDict[d[0]]=myList

print(EvaluationDict)

