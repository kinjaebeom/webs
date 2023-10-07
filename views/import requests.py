import requests
import pprint
import numpy as np

pp = pprint.PrettyPrinter(indent=4)
# 24시간마다 변경해야 함
api_key = 'RGAPI-fedf129b-8c53-4536-b364-0e83029a07c6'
request_header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36",
    "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
    "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
    "Origin": "https://developer.riotgames.com",
    "X-Riot-Token": api_key
}

# 유저 puuid 가져오기
def getUserPuuid(summonerName):
    url = f"https://kr.api.riotgames.com/lol/summoner/v4/summoners/by-name/{summonerName}?{api_key}"
    return requests.get(url, headers=request_header).json()['puuid']
# print(get_userPuuid('청파소나타')['puuid'])


# 게임 match_id 찾기
def getMatchId(puuid, start, count):
    url = f"https://asia.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?start={start}&count={count}"
    return requests.get(url, headers=request_header).json()
# pp.pprint(getMatchId("P4Ri8HBanEdTxQeT2cQS1MIN8RFQxaSukyHtFScjRLvUlzVMReZn_Rhzgzxr_HpZjxE_ah3fy4xaiA", 0, 10))

# 게임 정보 가져오기
def getGameInfo(matchId):
    url = f"https://asia.api.riotgames.com/lol/match/v5/matches/{matchId}"
    return requests.get(url, headers=request_header).json()
# pp.pprint(getGameInfo("KR_6710383118"))

# 타임라인으로 게임 정보 가져오기
def getGameInfoTimeline(matchId):
    url = f"https://asia.api.riotgames.com/lol/match/v5/matches/{matchId}/timeline"
    return requests.get(url, headers=request_header).json()

# pp.pprint(getGameInfoTimeline('KR_6709504031')['info']['frames'][10]['participantFrames'])

# pp.pprint(getGameInfoTimeline('KR_6709504031')['info']['frames'][10]['participantFrames']['1']['level'])


# for i in range(1, 11):
#     pp.pprint(getGameInfoTimeline('KR_6709504031')['info']['frames'][10]['participantFrames'][str(i)]['totalGold'])

# pp.pprint(getGameInfoTimeline('KR_6709504031')['info'].keys())


# KDA 가져오기
def getTeamKDA(matchId):
    gameInfo = getGameInfo(matchId)
    gameResult = {'win' : bool, 'lose' : bool}
    gameResult['win'] = {'kills' : 0, 'deaths' : 0, 'assists' : 0}
    gameResult['lose'] = {'kills' : 0, 'deaths' : 0, 'assists' : 0}
    diffScore = {'diffKillScore' : 0, 'diffDeathScore' : 0, 'diffAssistScore' : 0}
    # i번째 플레이어 (블루팀이 먼저 출력)
    for i in range(10):
        # 이긴 팀
        if gameInfo['info']['participants'][i]['win'] == True:
            gameResult['win']['kills'] += gameInfo['info']['participants'][i]['kills']
            gameResult['win']['deaths'] += gameInfo['info']['participants'][i]['deaths']
            gameResult['win']['assists'] += gameInfo['info']['participants'][i]['assists']
        # 진 팀
        if gameInfo['info']['participants'][i]['win'] == False:
            gameResult['lose']['kills'] += gameInfo['info']['participants'][i]['kills']
            gameResult['lose']['deaths'] += gameInfo['info']['participants'][i]['deaths']
            gameResult['lose']['assists'] += gameInfo['info']['participants'][i]['assists']
    return gameResult
# pp.pprint(getGameInfo('KR_6709504031')['info']['participants'][0]['championName'])

# nickName의 start번째 경기부터 count개 경기의 팀 KDA 합 가져오기  (gameKDA{}에 넣을 때 역으로 반전됨)
# 리턴값 == {게임코드 : {우리 팀}, {상대팀}}
def getTeamKDARecord(nickName, start, count):
    userName = getUserPuuid(nickName)
    matchIdList = getMatchId(userName, start, count)
    gameKDA = {}
    for i in matchIdList:
        gameKDA[i] = getTeamKDA(i)
    return gameKDA

# pp.pprint(getTeamKDARecord("청파소나타", 0, 5))
# print(getTeamKDA('KR_6709504031'))


# 게임 정보 확인
# matchId = 'KR_6709504031'
# pp.pprint(getGameInfo(matchId)['info']['participants'][1]['championName'])
# pp.pprint(getGameInfo(matchId)['info']['participants'][1]['summonerName'])
# pp.pprint(getGameInfo(matchId)['info']['participants'][0]['kills'])
# pp.pprint(getGameInfo(matchId)['info']['participants'][0]['deaths'])




# --------------------------------------------------------------------10분 후 게임 데이터------------------------------------------------------------------------------------

# 승리 팀, 패배 팀 participantId로 나누기
def teamClassfication(matchId):
    gameInfo = getGameInfo(matchId)['info']['participants']
    winTeamMember = []
    loseTeamMember = []
    for i in range(1, 11):
        if gameInfo[i-1]['win'] == True:
            winTeamMember.append(gameInfo[i-1]['participantId'])
        elif gameInfo[i-1]['win'] == False:
            loseTeamMember.append(gameInfo[i-1]['participantId'])

    return winTeamMember, loseTeamMember


# 게임 시작 10분 후의 데이터 셋 (탑, 정글, 미드, 원딜, 서폿)
def getDataSet(matchId, frame):
    # matchId = 'KR_6709504031'
    gameInfo = getGameInfoTimeline(matchId)['info']['frames']
    # gameInfo = getGameInfo(matchId)['info']['participants']
    winTeamMember, loseTeamMember = teamClassfication(matchId)
    dataSet = {}
    winTeamValue = {'level' : [], 
                    'minionsKilled' : [], 
                    'jungleMinionsKilled' : [], 
                    'killInfo' : {'killerId' : [], 'assistId' : []}, 
                    'wardCreatorId' : [], 
                    'wardKillerId' : [],
                    'inhibitorBreakerId' : [],
                    'towerBreakerId' : [],
                    'dragonKill' : [],
                    'riftheraldKill' : []}
    loseTeamValue = {'level' : [], 
                     'minionsKilled' : [], 
                     'jungleMinionsKilled' : [], 
                     'killInfo' : {'killerId' : [], 'assistId' : []}, 
                     'wardCreatorId' : [], 
                     'wardKillerId' : [],
                     'inhibitorBreakerId' : [],
                     'towerBreakerId' : [],
                     'dragonKill' : [],
                     'riftheraldKill' : []}

    # 킬, 어시스트 유저 assistingParticipantId 구하기
    for i in range(frame):
        events = gameInfo[i]['events']
        for j in range(len(events)):
            # 킬/어시
            if events[j]['type'] == 'CHAMPION_KILL':
                killerId = events[j]['killerId']
                assistId = None
                if 'assistingParticipantIds' in events[j]:
                    assistId = events[j]['assistingParticipantIds']
                if killerId in winTeamMember:
                    winTeamValue['killInfo']['killerId'].append(killerId)
                    winTeamValue['killInfo']['assistId'].append(assistId)
                elif killerId in loseTeamMember:
                    loseTeamValue['killInfo']['killerId'].append(killerId)
                    loseTeamValue['killInfo']['assistId'].append(assistId)
            # 와드 설치
            if  events[j]['type'] == 'WARD_PLACED':
                wardCreatorId = events[j]['creatorId']
                if wardCreatorId in winTeamMember:
                    winTeamValue['wardCreatorId'].append(wardCreatorId)
                elif wardCreatorId in loseTeamMember:
                    loseTeamValue['wardCreatorId'].append(wardCreatorId)
            # 와드 파괴
            if  events[j]['type'] == 'WARD_KILL':
                wardKillerId = events[j]['killerId']
                if wardCreatorId in winTeamMember:
                    winTeamValue['wardKillerId'].append(wardKillerId)
                elif wardCreatorId in loseTeamMember:
                    loseTeamValue['wardKillerId'].append(wardKillerId)
            # 구조물 파괴
            if events[j]['type'] == 'BUILDING_KILL':
                # 억제기
                if events[j]['buildingType'] == 'INHIBITOR_BUILDING':
                    buildingKillerId = events[j]['killerId']
                    if buildingKillerId in winTeamMember:
                        winTeamValue['inhibitorBreakerId'].append(buildingKillerId)
                    elif buildingKillerId in loseTeamMember:
                        loseTeamValue['inhibitorBreakerId'].append(buildingKillerId)
                # 타워
                if events[j]['buildingType'] == 'TOWER_BUILDING':
                    buildingKillerId = events[j]['killerId']
                    if buildingKillerId in winTeamMember:
                        winTeamValue['towerBreakerId'].append(buildingKillerId)
                    elif buildingKillerId in loseTeamMember:
                        loseTeamValue['towerBreakerId'].append(buildingKillerId)
            # 엘리트 몬스터 킬
            if events[j]['type'] == 'ELITE_MONSTER_KILL':
                # 드래곤
                if events[j]['monsterType'] == 'DRAGON':
                    mosterKillerId = events[j]['killerId']
                    dragonType = events[j]['monsterSubType']
                    dragonKillTimestamp = events[j]['timestamp']
                    dragonKillInfo = [dragonKillTimestamp, dragonType]
                    if mosterKillerId in winTeamMember:
                        winTeamValue['dragonKill'].append(dragonKillInfo)
                    elif mosterKillerId in loseTeamMember:
                        loseTeamValue['dragonKill'].append(dragonKillInfo)
                if events[j]['monsterType'] == 'RIFTHERALD':
                    mosterKillerId = events[j]['killerId']
                    riftheraldKillTimestamp = events[j]['timestamp']
                    if mosterKillerId in winTeamMember:
                        winTeamValue['riftheraldKill'].append(riftheraldKillTimestamp)
                    elif mosterKillerId in loseTeamMember:
                        loseTeamValue['riftheraldKill'].append(riftheraldKillTimestamp)


    # 레벨, 미니언 킬, 정글몹 킬 구하기
    for i in range(1, 11):
        participantFrames = gameInfo[frame]['participantFrames'][str(i)]
        if i in winTeamMember:
            winTeamValue['level'].append(participantFrames['level'])
            winTeamValue['minionsKilled'].append(participantFrames['minionsKilled'])
            winTeamValue['jungleMinionsKilled'].append(participantFrames['jungleMinionsKilled'])
        elif i in loseTeamMember:
            loseTeamValue['level'].append(participantFrames['level'])
            loseTeamValue['minionsKilled'].append(participantFrames['minionsKilled'])
            loseTeamValue['jungleMinionsKilled'].append(participantFrames['jungleMinionsKilled'])
    dataSet['diffLevel'] = sum(np.array(winTeamValue['level']) - np.array(loseTeamValue['level']))
    dataSet['diffMinionsKilled'] = sum(np.array(winTeamValue['minionsKilled']) - np.array(loseTeamValue['minionsKilled']))
    dataSet['diffJungleMinionsKilled'] = sum(np.array(winTeamValue['jungleMinionsKilled']) - np.array(loseTeamValue['jungleMinionsKilled']))
    # 0번 인덱스의 diffKillScore에 관한 어시스트는 diffAssistScore의 0번 인덱스임
    dataSet['diffKillScore'] = len(winTeamValue['killInfo']['killerId']) - len(loseTeamValue['killInfo']['killerId'])
    dataSet['diffAssistScore'] = sum(len(i) for i in winTeamValue['killInfo']['assistId'] if i != None) - sum(len(i) for i in loseTeamValue['killInfo']['assistId'] if i != None)
    dataSet['diffWardCreateScore'] = len(winTeamValue['wardCreatorId']) - len(loseTeamValue['wardCreatorId'])
    dataSet['diffWardKillScore'] = len(winTeamValue['wardKillerId']) - len(loseTeamValue['wardKillerId'])
    dataSet['diffInhibitorBreakScore'] = len(winTeamValue['inhibitorBreakerId']) - len(loseTeamValue['inhibitorBreakerId'])
    dataSet['diffTowerBreakScore'] = len(winTeamValue['towerBreakerId']) - len(loseTeamValue['towerBreakerId'])
    # 첫 용을 먹은 팀
    if not loseTeamValue['dragonKill']:
        dataSet['fistDragon'] = 'winTeam'
    elif not winTeamValue['dragonKill']:
        dataSet['fistDragon'] = 'loseTeam'
    else:
        if winTeamValue['dragonKill'][0] < loseTeamValue['dragonKill'][0]:
            dataSet['fistDragon'] = 'winTeam'
        else:
            dataSet['fistDragon'] = 'loseTeam'
    # 첫 전령을 먹은 팀
    if not loseTeamValue['riftheraldKill']:
        dataSet['firstRiftherald'] = 'winTeam'
    elif not winTeamValue['dragonKill']:
        dataSet['firstRiftherald'] = 'loseTeam'
    else:
        if winTeamValue['riftheraldKill'][0] < loseTeamValue['riftheraldKill'][0]:
            dataSet['firstRiftherald'] = 'winTeam'
        else:
            dataSet['firstRiftherald'] = 'loseTeam'

        
    # else:
    print(winTeamValue)
    print(loseTeamValue)
    
    return dataSet



pp.pprint(getDataSet('KR_6709504031', 15))


# [0]['participantId']
# teamId[1]['win']
# pp.pprint(teamId)


# gameInfo = getGameInfo('KR_6709504031')['info']['participants']
# idx = 1
# pp.pprint(gameInfo[idx]['participantId'])
# pp.pprint(gameInfo[idx]['teamId'])
# pp.pprint(gameInfo[idx]['summonerName'])