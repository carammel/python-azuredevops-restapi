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
    url = pr['url']
    revDisplayName = pr['reviewers'][0]['displayName']
    revvote= pr['reviewers'][0]['vote']
    if (revvote == 0):
        myList = [pullRequestId, repoName, projectID, creationDate[:10], url, revDisplayName, revvote]
        Dict[pullRequestId] = myList
        #print(pullRequestId, repoName, projectID, creationDate[:10], url, revDisplayName, revvote)
        
EvaluationDict ={}
for d in Dict.items():
    #print(d[0], d[1][2])
    evalutions = tfs.getEvaluationsonPRbyArtficatID(collectionName,'AI',str(d[1][2]), str(d[0]))
    myList = []
    if (evalutions['count'] !=0):
        for ev in evalutions['value']:
            tempDict ={}
            status = ev['status']
            name = ev['configuration']['type']['displayName']
            tempDict[name]=status
            myList.insert(0, tempDict)
            #print(tempDict)
        #print(myList)
        EvaluationDict[d[0]]=myList

#print(EvaluationDict)

 
#print ("{:<8} {:<35} {:<25} {:<25} {:<25}".format('PRID', 'Val','Result', 'RepoName', 'CreationDate'))
"""output = ("{:<8} {:<35} {:<25} {:<25} {:<25}".format('PRID', 'Val','Result', 'RepoName', 'CreationDate'))
for k, v in EvaluationDict.items():
    #print (k,v)
    for i in v:
        #print(i)
        for z, w in i.items():
            #print ("{:<8} {:<35} {:<25} {:<25} {:<25}".format(k, z, w,Dict[k][1],Dict[k][3]))
            output += ("\n"+"{:<8} {:<35} {:<25} {:<25} {:<25}".format(k, z, w,Dict[k][1],Dict[k][3]))
    output += ("\n------------------------------------------------------------------------------------------------------------------------")
            #print(k,z,w)

print(output)"""


output = "<table><tr><th>PRID</th><th>RepoName</th><th>CreationDate</th><th>Val</th><th>Result</th></tr>"
for k, v in EvaluationDict.items():
    url= "https://devops/Dev_Collection/APIs/_git/"+Dict[k][1]+"/pullrequest/"+str(k)
    output += ("<tr><td rowspan='"+ str(len(v)+1) +"'>" +"<a href='"+url+"'>"+str(k)+"</a></td><td rowspan='"+ str(len(v)+1) +"'>"+Dict[k][1]+"</td><td rowspan='"+ str(len(v)+1) +"'>" + str(Dict[k][3])+"</td></tr>")
    for i in v:
        for z, w in i.items():
            output += ("<tr><td>"+z+"</td><td>"+w+"</td></tr>")
output += ("</table>")

print("##vso[task.setvariable variable=PYoutput]"+output)
