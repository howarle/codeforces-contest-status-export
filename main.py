import requests
import json
import time
import hashlib

apiKey = "your_cf_api_key"
apiSecret = "your_cf_api_key_secret"
contestId = "your_context_id"
problemCount = 12


def getContestStatus(contestId):
    if type(contestId) is int:
        contestId = str(contestId)
    unix_time = str(int(time.time()))

    url_contain = 'contest.status?apiKey=' + apiKey + \
        '&contestId=' + contestId + '&count=999999&time='+unix_time
    hashc = '723456/' + url_contain + '#'+apiSecret
    hashc = hashlib.sha512(bytes(hashc, 'utf-8')).hexdigest()
    urlf = 'http://codeforces.com/api/' + \
        url_contain + '&apiSig=723456'+str(hashc)
    print(urlf)
    response = requests.get(urlf)
    ret = json.loads(response.content.decode('utf-8'))
    return ret['result']


def cfStatus2ResolverFormate(cfstatus):
    st = {}
    idList = set()
    for cfstatu in cfstatus:
        if (cfstatu["verdict"] == "COMPILATION_ERROR"):
            continue
        id = cfstatu["id"]
        st[id] = {}
        st[id]["user_id"] = cfstatu["author"]["members"][0]["handle"]
        st[id]["problem_index"] = str(
            ord(cfstatu["problem"]["index"]) - ord('A') + 1)
        st[id]["verdict"] = ("AC" if cfstatu["verdict"] == "OK" else "WA")
        st[id]["submitted_seconds"] = cfstatu["relativeTimeSeconds"]
        idList.add(st[id]["user_id"])
    ret = {}
    ret["solutions"] = st
    ret["users"] = {}
    for usr in idList:
        ret["users"][usr] = {}
        ret["users"][usr]["name"] = usr
        ret["users"][usr]["college"] = usr
        ret["users"][usr]["is_exclude"] = False
    return ret


def json_file_update(file, data):
    json.dump(data, open(file, 'w', encoding='utf-8'),
              sort_keys=True, indent=4)


def main():
    ret = getContestStatus(contestId)
    ret = cfStatus2ResolverFormate(ret)
    ret["problem_count"] = problemCount
    json_file_update("contest.json", ret)


main()
