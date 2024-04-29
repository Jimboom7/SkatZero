import numpy as np
from helpers import *

class SkatMatch:
    # Spieler mit Index 0 ist immer Vorhand (hören)

    def __init__(self, rawLogLine):
        self.parseRawLine(rawLogLine)

    def parseRawLine(self, line):
        lineParts = line.split('[')
        self.playerNames = [lineParts[7].partition(']')[0], lineParts[8].partition(']')[0], lineParts[9].partition(']')[0]]
        self.playerElos = [np.nan, np.nan, np.nan]
        for i in range(3):
            try:
                self.playerElos[i] = float(lineParts[i + 10].partition(']')[0])
            except:
                pass

        try:
            self.alleinspielerInd = int(lineParts[14][2])
            self.eingepasst = False
        except:
            self.alleinspielerInd = np.nan
            self.eingepasst = True

        p0Cards = lineParts[13][2:31]
        p1Cards = lineParts[13][32:61]
        p2Cards = lineParts[13][62:91]
        skatCards = lineParts[13][92:97]

        self.cards = {}
        self.cards[self.playerNames[0]] = p0Cards.split(".")
        self.cards[self.playerNames[1]] = p1Cards.split(".")
        self.cards[self.playerNames[2]] = p2Cards.split(".")

        self.playerCards = np.stack([convertCardStringToMat(p0Cards, '.'), convertCardStringToMat(p1Cards, '.'), convertCardStringToMat(p2Cards, '.')])
        self.skatCards = convertCardStringToMat(skatCards, '.')

        reizAndPlay = lineParts[13][98:]

        self.maxReizungen = [0, 0, 0]
        self.skatTaken = np.nan
        self.stichPoints = np.nan
        self.gedrueckt = np.nan
        self.cardPlays = np.nan
        self.gameType = ''
        self.playedFullRounds = 0

        if not self.eingepasst:
            reizAndPlaySplit = reizAndPlay.split(' s w ')
            self.skatTaken = len(reizAndPlaySplit) > 1
            if not self.skatTaken:
                reizAndPlaySplit = reizAndPlay.partition('H') #erstes H ist die Handspielansage
            reizungen = reizAndPlaySplit[0]
            cardPlay = reizAndPlaySplit[-1]
            if self.skatTaken:
                reizungen = reizungen[:-2]
                if 'NO' in cardPlay:
                    # Null Ouvert ist das einzige Spiel ohne Hand mit zwei Buchstaben
                    self.gedrueckt = convertCardStringToMat(cardPlay[11:16], '.')
                    self.gameType = 'NO'
                    if cardPlay[16] == '.':
                        # Alle 12 Karten werden aufgelistet
                        cardPlay = cardPlay[47:]
                    else:
                        # Nur 2 Karten werden aufgelistet
                        cardPlay = cardPlay[17:]
                else:
                    # Spiel hat nur einen Buchstaben (G, C, S, H, D, N)
                    self.gedrueckt = convertCardStringToMat(cardPlay[10:15], '.')
                    self.gameType = cardPlay[8]
                    cardPlay = cardPlay[16:]
            else:
                self.gedrueckt = self.skatCards

                if cardPlay[0] == 'H': # HH
                    reizungen += 'H'
                    cardPlay = cardPlay[1:]
                if cardPlay[0] == 'O': # NHO
                    reizungen += 'O'
                    cardPlay = cardPlay[31:]

                if cardPlay[0] == ' ':
                    # Normales Handspiel ohne Zusätze
                    reizungenParts = reizungen.rpartition(' ')
                    reizungen = reizungenParts[0][:-2]
                    self.gameType = reizungenParts[-1] + 'H'
                    cardPlay = cardPlay[1:]
                    pass
                else:
                    raise ValueError('Zusätze werden im Moment nicht unterstützt!')

            assert cardPlay[0] in ['0', '1', '2'], 'Hier ist etwas schiefgelaufen'
            assert reizungen[-1] == 'p' or reizungen[-2:] == '18', 'Hier ist etwas schiefgelaufen'

            reizungenSplit = reizungen.split(' ')[::-1]
            for i in range(3):
                compareChar = str(i)
                for j, element in enumerate(reizungenSplit):
                    if element == compareChar:
                        if reizungenSplit[j-1] == 'y':
                            self.maxReizungen[i] = int(reizungenSplit[j+1])
                            break
                        elif reizungenSplit[j-1].isnumeric():
                            self.maxReizungen[i] = int(reizungenSplit[j-1])
                            break

            alleinspielerStartCards = self.playerCards[self.alleinspielerInd, :, :].copy()
            alleinspielerStartCards += self.skatCards - self.gedrueckt

            auswertungSplit = lineParts[14].split(' ')
            self.baseValuePoints = int(auswertungSplit[2][2:])
            self.stichPoints = int(auswertungSplit[5][2:])

            if self.gameType not in ['C', 'S', 'H', 'D', 'CH', 'SH', 'HH', 'DH']:
                return

            # Ausspielphase
            self.cardPlays = np.zeros((3, 3, 10), dtype=np.uint8) #pInd, vorhand-/mittelhand-/hinterhandInd, rundenInd; Inhalt: 1-32 oder 0 (keine Karte)
            self.alleinspielerAugen = np.zeros((11,), dtype=np.int8) - 1 #[gedrueckt, Runde 0, Runde 1, ...]
            self.alleinspielerAugen[0] = getPointsForMat(self.gedrueckt)
            self.gegenspielerAugen = np.zeros((11,), dtype=np.int8) - 1
            self.gegenspielerAugen[0] = 0
            cardPlaysSplit = cardPlay.split(' ')
            cnt = 0
            ende = False
            for i in range(10):
                if ende:
                    break
                thisStichAsMat = np.zeros((3, 4, 8))
                for j in range(3):
                    playerIndStr = cardPlaysSplit[cnt]
                    if cardPlaysSplit[cnt] not in ['0', '1', '2']:
                        ende = True
                        break
                    playerInd = int(playerIndStr)
                    cnt += 1
                    if cardPlaysSplit[cnt] in ['SC', 'RE']: #SChenken? REst bei mir?
                        ende = True
                        break

                    thisCardInd1, thisCardInd2 = getIndsOfCardName(cardPlaysSplit[cnt])
                    thisStichAsMat[j, thisCardInd1, thisCardInd2] = 1

                    thisCardAsUInt8 = getUInt8FromMatInds(thisCardInd1, thisCardInd2)
                    cnt += 1
                    self.cardPlays[playerInd, j, i] = thisCardAsUInt8
                    if playerInd == self.alleinspielerInd:
                        thisStichASInd = j

                if not ende:
                    self.playedFullRounds += 1
                    thisStichAugen = getStichPointsAlleinspieler(thisStichAsMat, thisStichASInd, self.gameType)[0]
                    if thisStichAugen >= 0:
                        self.alleinspielerAugen[i + 1] = self.alleinspielerAugen[i] + thisStichAugen
                        self.gegenspielerAugen[i + 1] = self.gegenspielerAugen[i]
                    else:
                        self.alleinspielerAugen[i + 1] = self.alleinspielerAugen[i]
                        self.gegenspielerAugen[i + 1] = self.gegenspielerAugen[i] - thisStichAugen


