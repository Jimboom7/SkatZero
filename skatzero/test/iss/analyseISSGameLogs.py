import numpy as np
from SkatMatch import SkatMatch
import pickle

def getMatchesFromLogFile(logFilePath):
    matches = []
    print('Reading file...')
    with open(logFilePath) as fRaw:

        line = fRaw.readline()
        print(line)

        matchCounter = 0
        fileCounter = 0
        while line:
            if matchCounter % 20000 == 0:
                print(matchCounter)
            try:
                matches.append(SkatMatch(line))
            except:
                pass
            line = fRaw.readline()
            matchCounter += 1
    return matches

def evaluateMatches(matches, players, gameTypesToExclude):
    evalDict = {}
    for player in players:
        print(f'Evaluating matches for player {player}...')
        evalDict[player] = evaluateMatchesForPlayer(matches, player, gameTypesToExclude)
    return evalDict

def evaluateMatchesForPlayer(matches, evalPlayer, gameTypesToExclude):
    playerEvalDict = initPlayerEvalDict()

    for matchInd, match in enumerate(matches):
        if matchInd % 20000 == 0:
            print(matchInd)
        for playerInd, player in enumerate(match.playerNames):
            if player != evalPlayer and player != evalPlayer+':2':
                # Eval-Spieler nicht am Tisch.
                continue

            if match.eingepasst:
                # Eingepasst. Geht nicht in Statistiken ein.
                continue

            to_eval = True
            for gameTypeToExlude in gameTypesToExclude:
                if gameTypeToExlude == match.gameType[0]:
                    # Dieser Spieltyp soll nicht berücksichtigt werden.
                    to_eval = False
            if not to_eval:
                continue
            
            if match.alleinspielerInd == playerInd:
                playerEvalDict['numberOfGamesSolo'] += 1
                seegerFabianScoreSolo = match.baseValuePoints
                seegerFabianScoreSolo += 50 if seegerFabianScoreSolo > 0 else -50
                playerEvalDict['avgSeegerFabianScoreOverall'] += seegerFabianScoreSolo
                playerEvalDict['avgSeegerFabianScoreSolo'] += seegerFabianScoreSolo
                if 'N' not in match.gameType:
                    playerEvalDict['numberOfWinsSolo'] += match.stichPoints >= 61
                    playerEvalDict['numberOfLossesSolo'] += match.stichPoints <= 60
                    playerEvalDict['numberOfWinsSoloNormal'] += match.stichPoints >= 61 and match.stichPoints <= 89
                    playerEvalDict['numberOfLossesSoloNormal'] += match.stichPoints <= 60 and match.stichPoints >= 31
                    playerEvalDict['numberOfWinsSoloSchneider'] += match.stichPoints >= 90
                    playerEvalDict['numberOfLossesSoloSchneider'] += match.stichPoints <= 30
                    playerEvalDict['averageAugenSolo'] += match.stichPoints
                    playerEvalDict['percentageFarbspielSolo'] += 'G' not in match.gameType
                    playerEvalDict['percentageGrandSolo'] += 'G' in match.gameType
                else:
                    playerEvalDict['percentageNullSolo'] += 1
                    playerEvalDict['numberOfWinsSolo'] += seegerFabianScoreSolo > 0
                    playerEvalDict['numberOfLossesSolo'] += seegerFabianScoreSolo < 0
            else:
                playerEvalDict['numberOfGamesOpp'] += 1
                seegerFabianScoreOpp = 40 if match.baseValuePoints < 0 else 0
                playerEvalDict['avgSeegerFabianScoreOverall'] += seegerFabianScoreOpp
                playerEvalDict['avgSeegerFabianScoreOpp'] += seegerFabianScoreOpp
                if 'N' not in match.gameType:
                    playerEvalDict['numberOfWinsOpp'] += match.stichPoints <= 60
                    playerEvalDict['numberOfLossesOpp'] += match.stichPoints >= 61
                    playerEvalDict['numberOfWinsOppNormal'] += match.stichPoints <= 60 and match.stichPoints >= 31
                    playerEvalDict['numberOfLossesOppNormal'] += match.stichPoints >= 61 and match.stichPoints <= 89
                    playerEvalDict['numberOfWinsOppSchneider'] += match.stichPoints <= 30
                    playerEvalDict['numberOfLossesOppSchneider'] += match.stichPoints >= 90
                    playerEvalDict['averageAugenOpp'] += (120 - match.stichPoints)
                    playerEvalDict['percentageFarbspielOpp'] += 'G' not in match.gameType
                    playerEvalDict['percentageGrandOpp'] += 'G' in match.gameType
                else:
                    playerEvalDict['percentageNullOpp'] += 1
                    playerEvalDict['numberOfWinsOpp'] += seegerFabianScoreOpp > 0
                    playerEvalDict['numberOfLossesOpp'] += seegerFabianScoreOpp == 0

    playerEvalDict = calculatePercentages(playerEvalDict)
    return playerEvalDict

def initPlayerEvalDict():
    playerEvalDict = {}
    playerEvalDict['avgSeegerFabianScoreOverall'] = 0
    playerEvalDict['avgSeegerFabianScoreSolo'] = 0
    playerEvalDict['avgSeegerFabianScoreOpp'] = 0

    playerEvalDict['numberOfGamesSolo'] = 0
    playerEvalDict['numberOfWinsSolo'] = 0
    playerEvalDict['numberOfWinsSoloNormal'] = 0
    playerEvalDict['numberOfWinsSoloSchneider'] = 0
    playerEvalDict['numberOfLossesSolo'] = 0
    playerEvalDict['numberOfLossesSoloNormal'] = 0
    playerEvalDict['numberOfLossesSoloSchneider'] = 0
    playerEvalDict['averageAugenSolo'] = 0
    playerEvalDict['percentageFarbspielSolo'] = 0
    playerEvalDict['percentageGrandSolo'] = 0
    playerEvalDict['percentageNullSolo'] = 0

    playerEvalDict['numberOfGamesOpp'] = 0
    playerEvalDict['numberOfWinsOpp'] = 0
    playerEvalDict['numberOfWinsOppNormal'] = 0
    playerEvalDict['numberOfWinsOppSchneider'] = 0
    playerEvalDict['numberOfLossesOpp'] = 0
    playerEvalDict['numberOfLossesOppNormal'] = 0
    playerEvalDict['numberOfLossesOppSchneider'] = 0
    playerEvalDict['averageAugenOpp'] = 0
    playerEvalDict['percentageFarbspielOpp'] = 0
    playerEvalDict['percentageGrandOpp'] = 0
    playerEvalDict['percentageNullOpp'] = 0
    return playerEvalDict

def calculatePercentages(playerEvalDict):
    numGamesSolo = playerEvalDict['numberOfGamesSolo']
    if numGamesSolo > 0:
        playerEvalDict['averageAugenSolo'] /= numGamesSolo
        playerEvalDict['percentageFarbspielSolo'] /= numGamesSolo
        playerEvalDict['percentageGrandSolo'] /= numGamesSolo
        playerEvalDict['percentageNullSolo'] /= numGamesSolo
        playerEvalDict['avgSeegerFabianScoreSolo'] /= numGamesSolo

    numGamesOpp = playerEvalDict['numberOfGamesOpp']
    if numGamesOpp > 0:
        playerEvalDict['averageAugenOpp'] /= numGamesOpp
        playerEvalDict['percentageFarbspielOpp'] /= numGamesOpp
        playerEvalDict['percentageGrandOpp'] /= numGamesOpp
        playerEvalDict['percentageNullOpp'] /= numGamesOpp
        playerEvalDict['avgSeegerFabianScoreOpp'] /= numGamesOpp

    totalGames = numGamesSolo + numGamesOpp
    if totalGames > 0:
        playerEvalDict['avgSeegerFabianScoreOverall'] /= totalGames
    return playerEvalDict


if __name__ == '__main__':
    # Parameter
    issLogFilePath = 'D:/Skat/Daten/iss_Hubert47_6.sgf'
    playersToEvaluate = ['Hubert47', 'kermit']
    gameTypesToExclude = [] #'G' = Grand, 'N' = Null

    # Logfile parsen und in Liste mit Objekten der Klasse "SkatMatch" übersetzen
    matches = getMatchesFromLogFile(issLogFilePath)

    evalDict = evaluateMatches(matches, playersToEvaluate, gameTypesToExclude)

    print('Ende')
