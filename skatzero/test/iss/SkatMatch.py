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
                    cardPlay = cardPlay[17:]
                else:
                    # Spiel hat nur einen Buchstaben (G, C, S, H, D, N)
                    self.gedrueckt = convertCardStringToMat(cardPlay[10:15], '.')
                    self.gameType = cardPlay[8]
                    cardPlay = cardPlay[16:]
            else:
                self.gedrueckt = self.skatCards
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

            if self.gameType not in ['C', 'S', 'H', 'D', 'CH', 'SH', 'HH', 'DH']:
                raise ValueError('Dieser Spieltyp ist hier noch nicht implementiert!')

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



            auswertungSplit = lineParts[14].split(' ')
            self.baseValuePoints = int(auswertungSplit[2][2:])
            self.stichPoints = int(auswertungSplit[5][2:])


    def getLabel(self):
        label = np.zeros((6,), dtype=np.uint8)
        if self.stichPoints == 120:
            label[5] = 1
        elif self.stichPoints >= 90:
            label[4] = 1
        elif self.stichPoints >= 61:
            label[3] = 1
        elif self.stichPoints >= 31:
            label[2] = 1
        elif self.stichPoints >= 1:
            label[1] = 1
        else:
            label[0] = 1
        return label

    def getFeaturesAlleinspieler_v0(self, round, permutate):
        if round >= self.playedFullRounds:
            raise ValueError('Runde existiert gar nicht!')
        if self.gameType not in ['C', 'S', 'H', 'D']:
            raise ValueError('Für diesen Spieltyp noch nicht implementiert!')

        # Reizungen werden weggelassen

        alleinspielerOneHot = np.zeros((3,), dtype=np.uint8)
        alleinspielerOneHot[self.alleinspielerInd] = 1

        # Skat und drücken berücksichtigen, um Starthand zu bestimmen
        playerCards = self.playerCards[self.alleinspielerInd, :, :].copy()
        playerCards += self.skatCards - self.gedrueckt

        cardPlaysOneHot = np.zeros((3, 3, 10, 4, 8), dtype=np.uint8)
        for i in range(cardPlaysOneHot.shape[0]):
            for j in range(cardPlaysOneHot.shape[1]):
                for k in range(round+1):
                    cardIndUInt8 = self.cardPlays[i, j, k]
                    if cardIndUInt8 > 0:
                        farbInd = (cardIndUInt8 - 1) // 8
                        kartenInd = (cardIndUInt8 - 1) - 8 * farbInd
                        cardPlaysOneHot[i, j, k, farbInd, kartenInd] = 1
                        if i == self.alleinspielerInd:
                            playerCards[farbInd, kartenInd] = 0

        # Wenn der Alleinspieler Vorhand oder Mittelhand ist, spätere Karten in dieser Runde löschen
        positionInThisRound = np.where(self.cardPlays[self.alleinspielerInd, :, round] > 0)[0][0]
        if positionInThisRound < 2:
            cardPlaysOneHot[:, positionInThisRound+1:, round, :, :] = 0

        # Beim Farbspiel wird immer Trumpf in die 1. Zeile geschoben
        gedrueckt = self.gedrueckt.copy()
        trumpfInd = ['C', 'S', 'H', 'D'].index(self.gameType[0])
        newFarbOrder = [0, 1, 2, 3]
        newFarbOrder.insert(0, newFarbOrder.pop(trumpfInd))
        playerCards[:, 1:] = playerCards[newFarbOrder, 1:]
        gedrueckt[:, 1:] = gedrueckt[newFarbOrder, 1:]
        cardPlaysOneHot[:, :, :, :, 1:] = cardPlaysOneHot[:, :, :, newFarbOrder, 1:]

        if permutate:
            if 'C' in self.gameType or 'S' in self.gameType or 'H' in self.gameType or 'D' in self.gameType:
                # Farbspiel: Nicht-Trümpfe zufällig austauschen
                newOrder = np.random.permutation([0, 1, 2])
                playerCards[1:, 1:] = playerCards[1:, 1:][newOrder, :]
                gedrueckt[1:, 1:] = gedrueckt[1:, 1:][newOrder, :]
                cardPlaysOneHot[:, :, :, 1:, 1:] = cardPlaysOneHot[:, :, :, 1:, 1:][:, :, :, newOrder, :]
            else:
                raise ValueError('Für diesen Spieltyp noch nicht implementiert!')

        return [alleinspielerOneHot, playerCards, gedrueckt, cardPlaysOneHot]

    def getFeaturesAlleinspieler_v1(self, round, permutate):
        if round >= self.playedFullRounds:
            raise ValueError('Runde existiert gar nicht!')
        if self.gameType not in ['C', 'S', 'H', 'D']:
            raise ValueError('Für diesen Spieltyp noch nicht implementiert!')

        # Reizungen werden weggelassen

        # Skat und drücken berücksichtigen, um Starthand zu bestimmen
        playerCards = self.playerCards[self.alleinspielerInd, :, :].copy()
        playerCards += self.skatCards - self.gedrueckt

        cardPlaysOneHot = np.zeros((3, 3, 10, 4, 8), dtype=np.uint8)
        for i in range(cardPlaysOneHot.shape[0]):
            for j in range(cardPlaysOneHot.shape[1]):
                for k in range(round+1):
                    cardIndUInt8 = self.cardPlays[i, j, k]
                    if cardIndUInt8 > 0:
                        farbInd = (cardIndUInt8 - 1) // 8
                        kartenInd = (cardIndUInt8 - 1) - 8 * farbInd
                        cardPlaysOneHot[i, j, k, farbInd, kartenInd] = 1
                        if i == self.alleinspielerInd:
                            playerCards[farbInd, kartenInd] = 0

        # Wenn der Alleinspieler Vorhand oder Mittelhand ist, spätere Karten in dieser Runde löschen
        positionInThisRound = np.where(self.cardPlays[self.alleinspielerInd, :, round] > 0)[0][0]
        if positionInThisRound < 2:
            cardPlaysOneHot[:, positionInThisRound+1:, round, :, :] = 0

        # Der Alleinspieler bekommt immer den Spieler-Index 0
        playerOrderNew = np.roll(np.array([0, 1, 2]), -self.alleinspielerInd)
        cardPlaysOneHot = cardPlaysOneHot[playerOrderNew, :, :, :, :]

        # Beim Farbspiel wird immer Trumpf in die 1. Zeile geschoben
        gedrueckt = self.gedrueckt.copy()
        trumpfInd = ['C', 'S', 'H', 'D'].index(self.gameType[0])
        newFarbOrder = [0, 1, 2, 3]
        newFarbOrder.insert(0, newFarbOrder.pop(trumpfInd))
        playerCards[:, 1:] = playerCards[newFarbOrder, 1:]
        gedrueckt[:, 1:] = gedrueckt[newFarbOrder, 1:]
        cardPlaysOneHot[:, :, :, :, 1:] = cardPlaysOneHot[:, :, :, newFarbOrder, 1:]

        if permutate:
            if 'C' in self.gameType or 'S' in self.gameType or 'H' in self.gameType or 'D' in self.gameType:
                # Farbspiel: Nicht-Trümpfe zufällig austauschen
                newOrder = np.random.permutation([0, 1, 2])
                playerCards[1:, 1:] = playerCards[1:, 1:][newOrder, :]
                gedrueckt[1:, 1:] = gedrueckt[1:, 1:][newOrder, :]
                cardPlaysOneHot[:, :, :, 1:, 1:] = cardPlaysOneHot[:, :, :, 1:, 1:][:, :, :, newOrder, :]
            else:
                raise ValueError('Für diesen Spieltyp noch nicht implementiert!')

        return [playerCards, gedrueckt, cardPlaysOneHot]

    def getFeaturesAlleinspieler_v2(self, round, permutate):
        if round >= self.playedFullRounds:
            raise ValueError('Runde existiert gar nicht!')
        if self.gameType not in ['C', 'S', 'H', 'D']:
            raise ValueError('Für diesen Spieltyp noch nicht implementiert!')

        # Reizungen werden weggelassen

        # Skat und drücken berücksichtigen, um Starthand zu bestimmen
        playerCards = self.playerCards[self.alleinspielerInd, :, :].copy()
        playerCards += self.skatCards - self.gedrueckt

        cardPlaysOneHot = np.zeros((3, 3, 10, 4, 8), dtype=np.uint8)
        for i in range(cardPlaysOneHot.shape[0]):
            for j in range(cardPlaysOneHot.shape[1]):
                for k in range(round+1):
                    cardIndUInt8 = self.cardPlays[i, j, k]
                    if cardIndUInt8 > 0:
                        farbInd = (cardIndUInt8 - 1) // 8
                        kartenInd = (cardIndUInt8 - 1) - 8 * farbInd
                        cardPlaysOneHot[i, j, k, farbInd, kartenInd] = 1
                        if i == self.alleinspielerInd:
                            playerCards[farbInd, kartenInd] = 0

        # Wenn der Alleinspieler Vorhand oder Mittelhand ist, spätere Karten in dieser Runde löschen
        positionInThisRound = np.where(self.cardPlays[self.alleinspielerInd, :, round] > 0)[0][0]
        if positionInThisRound < 2:
            cardPlaysOneHot[:, positionInThisRound+1:, round, :, :] = 0

        # Der Alleinspieler bekommt immer den Spieler-Index 0
        playerOrderNew = np.roll(np.array([0, 1, 2]), -self.alleinspielerInd)
        cardPlaysOneHot = cardPlaysOneHot[playerOrderNew, :, :, :, :]

        # Beim Farbspiel wird immer Trumpf in die 1. Zeile geschoben
        gedrueckt = self.gedrueckt.copy()
        trumpfInd = ['C', 'S', 'H', 'D'].index(self.gameType[0])
        newFarbOrder = [0, 1, 2, 3]
        newFarbOrder.insert(0, newFarbOrder.pop(trumpfInd))
        playerCards[:, 1:] = playerCards[newFarbOrder, 1:]
        gedrueckt[:, 1:] = gedrueckt[newFarbOrder, 1:]
        cardPlaysOneHot[:, :, :, :, 1:] = cardPlaysOneHot[:, :, :, newFarbOrder, 1:]

        # Merkmal der derzeitigen Augen bestimmen
        # Vorberechnete Augenanzahl aus der vorherigen Runde nutzen
        augenSumAlleinSpieler = np.array([self.alleinspielerAugen[round]])
        # Wenn der Alleinspieler Hinterhand ist, kann man die aktuelle Runde bereits auswerten.
        # Ansonsten zählen nur alle Stiche bis zu dieser Runde.
        if np.sum(self.cardPlays[self.alleinspielerInd, 2, round] > 0):
            thisStichAugen = getStichPointsForRoundFarbspiel(cardPlaysOneHot, round)
            if thisStichAugen > 0:
                augenSumAlleinSpieler += thisStichAugen

        if permutate:
            if 'C' in self.gameType or 'S' in self.gameType or 'H' in self.gameType or 'D' in self.gameType:
                # Farbspiel: Nicht-Trümpfe zufällig austauschen
                newOrder = np.random.permutation([0, 1, 2])
                playerCards[1:, 1:] = playerCards[1:, 1:][newOrder, :]
                gedrueckt[1:, 1:] = gedrueckt[1:, 1:][newOrder, :]
                cardPlaysOneHot[:, :, :, 1:, 1:] = cardPlaysOneHot[:, :, :, 1:, 1:][:, :, :, newOrder, :]
            else:
                raise ValueError('Für diesen Spieltyp noch nicht implementiert!')

        return [augenSumAlleinSpieler, playerCards, gedrueckt, cardPlaysOneHot]

    def getFeaturesAlleinspieler_v3(self, round, permutate):
        if round >= self.playedFullRounds:
            raise ValueError('Runde existiert gar nicht!')
        if self.gameType not in ['C', 'S', 'H', 'D']:
            raise ValueError('Für diesen Spieltyp noch nicht implementiert!')

        # Reizungen werden weggelassen

        # Skat und drücken berücksichtigen, um Starthand zu bestimmen
        playerCards = self.playerCards[self.alleinspielerInd, :, :].copy()
        playerCards += self.skatCards - self.gedrueckt

        cardPlaysOneHot = np.zeros((3, 3, 10, 4, 8), dtype=np.uint8)
        for i in range(cardPlaysOneHot.shape[0]):
            for j in range(cardPlaysOneHot.shape[1]):
                for k in range(round+1):
                    cardIndUInt8 = self.cardPlays[i, j, k]
                    if cardIndUInt8 > 0:
                        farbInd = (cardIndUInt8 - 1) // 8
                        kartenInd = (cardIndUInt8 - 1) - 8 * farbInd
                        cardPlaysOneHot[i, j, k, farbInd, kartenInd] = 1
                        if i == self.alleinspielerInd:
                            playerCards[farbInd, kartenInd] = 0

        # Wenn der Alleinspieler Vorhand oder Mittelhand ist, spätere Karten in dieser Runde löschen
        positionInThisRound = np.where(self.cardPlays[self.alleinspielerInd, :, round] > 0)[0][0]
        if positionInThisRound < 2:
            cardPlaysOneHot[:, positionInThisRound+1:, round, :, :] = 0

        # Der Alleinspieler bekommt immer den Spieler-Index 0
        playerOrderNew = np.roll(np.array([0, 1, 2]), -self.alleinspielerInd)
        cardPlaysOneHot = cardPlaysOneHot[playerOrderNew, :, :, :, :]

        # Beim Farbspiel wird immer Trumpf in die 1. Zeile geschoben
        gedrueckt = self.gedrueckt.copy()
        trumpfInd = ['C', 'S', 'H', 'D'].index(self.gameType[0])
        newFarbOrder = [0, 1, 2, 3]
        newFarbOrder.insert(0, newFarbOrder.pop(trumpfInd))
        playerCards[:, 1:] = playerCards[newFarbOrder, 1:]
        gedrueckt[:, 1:] = gedrueckt[newFarbOrder, 1:]
        cardPlaysOneHot[:, :, :, :, 1:] = cardPlaysOneHot[:, :, :, newFarbOrder, 1:]

        # Merkmal der derzeitigen Augen bestimmen
        # Vorberechnete Augenanzahl aus der vorherigen Runde nutzen
        augenSumAlleinSpieler = np.array([self.alleinspielerAugen[round]])
        augenSumGegenSpieler = np.array([self.gegenspielerAugen[round]])
        # Wenn der Alleinspieler Hinterhand ist, kann man die aktuelle Runde bereits auswerten.
        # Ansonsten zählen nur alle Stiche bis zu dieser Runde.
        if np.sum(self.cardPlays[self.alleinspielerInd, 2, round] > 0):
            thisStichAugen = getStichPointsForRoundFarbspiel(cardPlaysOneHot, round)
            if thisStichAugen > 0:
                augenSumAlleinSpieler += thisStichAugen
        # Wenn der Alleinspieler Mittelhand oder Hinterhand ist, kann man für die Gegenspieler bereits
        # auswerten.
        if np.sum(self.cardPlays[self.alleinspielerInd, 1:, round] > 0):
            thisStichAugen = getStichPointsForRoundFarbspiel(cardPlaysOneHot, round)
            if thisStichAugen < 0:
                augenSumGegenSpieler -= thisStichAugen

        if permutate:
            if 'C' in self.gameType or 'S' in self.gameType or 'H' in self.gameType or 'D' in self.gameType:
                # Farbspiel: Nicht-Trümpfe zufällig austauschen
                newOrder = np.random.permutation([0, 1, 2])
                playerCards[1:, 1:] = playerCards[1:, 1:][newOrder, :]
                gedrueckt[1:, 1:] = gedrueckt[1:, 1:][newOrder, :]
                cardPlaysOneHot[:, :, :, 1:, 1:] = cardPlaysOneHot[:, :, :, 1:, 1:][:, :, :, newOrder, :]
            else:
                raise ValueError('Für diesen Spieltyp noch nicht implementiert!')

        return [augenSumAlleinSpieler, augenSumGegenSpieler, playerCards, gedrueckt, cardPlaysOneHot]

    def getFeaturesAlleinspieler_v4(self, round, permutate):
        if round >= self.playedFullRounds:
            raise ValueError('Runde existiert gar nicht!')
        if self.gameType not in ['C', 'S', 'H', 'D']:
            raise ValueError('Für diesen Spieltyp noch nicht implementiert!')

        # Reizungen werden weggelassen

        # Skat und drücken berücksichtigen, um Starthand zu bestimmen
        alleinspielerCards = self.playerCards[self.alleinspielerInd, :, :].copy()
        alleinspielerCards += self.skatCards - self.gedrueckt

        cardPlaysOneHot = np.zeros((3, 3, 10, 4, 8), dtype=np.uint8)
        for i in range(cardPlaysOneHot.shape[0]):
            for j in range(cardPlaysOneHot.shape[1]):
                for k in range(round+1):
                    cardIndUInt8 = self.cardPlays[i, j, k]
                    if cardIndUInt8 > 0:
                        farbInd = (cardIndUInt8 - 1) // 8
                        kartenInd = (cardIndUInt8 - 1) - 8 * farbInd
                        cardPlaysOneHot[i, j, k, farbInd, kartenInd] = 1
                        if i == self.alleinspielerInd and not k == round:
                            alleinspielerCards[farbInd, kartenInd] = 0

        # Wenn der Alleinspieler Vorhand oder Mittelhand ist, spätere Karten in dieser Runde löschen
        positionInThisRound = np.where(self.cardPlays[self.alleinspielerInd, :, round] > 0)[0][0]
        if positionInThisRound < 2:
            cardPlaysOneHot[:, positionInThisRound+1:, round, :, :] = 0

        # Der Alleinspieler bekommt immer den Spieler-Index 0
        playerOrderNew = np.roll(np.array([0, 1, 2]), -self.alleinspielerInd)
        cardPlaysOneHot = cardPlaysOneHot[playerOrderNew, :, :, :, :]

        # Beim Farbspiel wird immer Trumpf in die 1. Zeile geschoben
        gedrueckt = self.gedrueckt.copy()
        trumpfInd = ['C', 'S', 'H', 'D'].index(self.gameType[0])
        newFarbOrder = [0, 1, 2, 3]
        newFarbOrder.insert(0, newFarbOrder.pop(trumpfInd))
        alleinspielerCards[:, 1:] = alleinspielerCards[newFarbOrder, 1:]
        gedrueckt[:, 1:] = gedrueckt[newFarbOrder, 1:]
        cardPlaysOneHot[:, :, :, :, 1:] = cardPlaysOneHot[:, :, :, newFarbOrder, 1:]

        # Merkmal der derzeitigen Augen bestimmen
        # Vorberechnete Augenanzahl aus der vorherigen Runde nutzen
        augenSumAlleinSpieler = np.array([self.alleinspielerAugen[round]])
        augenSumGegenSpieler = np.array([self.gegenspielerAugen[round]])
        # Wenn der Alleinspieler Hinterhand ist, kann man die aktuelle Runde bereits auswerten.
        # Ansonsten zählen nur alle Stiche bis zu dieser Runde.
        if np.sum(self.cardPlays[self.alleinspielerInd, 2, round] > 0):
            thisStichAugen, stichGewonnen = getStichPointsForRoundFarbspiel(cardPlaysOneHot, round)
            farbInd = (self.cardPlays[self.alleinspielerInd, 2, round] - 1) // 8
            kartenInd = (self.cardPlays[self.alleinspielerInd, 2, round] - 1) - 8 * farbInd
            if kartenInd == 0:
                alleinspielerCards[farbInd, kartenInd] = 0
            else:
                alleinspielerCards[newFarbOrder.index(farbInd), kartenInd] = 0
            if thisStichAugen > 0:
                augenSumAlleinSpieler += thisStichAugen
        # Wenn der Alleinspieler Mittelhand oder Hinterhand ist, kann man für die Gegenspieler bereits
        # auswerten.
        if np.sum(self.cardPlays[self.alleinspielerInd, 1:, round] > 0):
            thisStichAugen, stichGewonnen = getStichPointsForRoundFarbspiel(cardPlaysOneHot, round)
            actualOrderInd = np.where(self.cardPlays[self.alleinspielerInd, 1:, round] > 0)[0] + 1
            farbInd = (self.cardPlays[self.alleinspielerInd, actualOrderInd, round] - 1) // 8
            kartenInd = (self.cardPlays[self.alleinspielerInd, actualOrderInd, round] - 1) - 8 * farbInd
            if kartenInd == 0:
                alleinspielerCards[farbInd, kartenInd] = 0
            else:
                alleinspielerCards[newFarbOrder.index(farbInd), kartenInd] = 0
            if thisStichAugen < 0:
                augenSumGegenSpieler -= thisStichAugen

        if permutate:
            if 'C' in self.gameType or 'S' in self.gameType or 'H' in self.gameType or 'D' in self.gameType:
                # Farbspiel: Nicht-Trümpfe zufällig austauschen
                newOrder = np.random.permutation([0, 1, 2])
                alleinspielerCards[1:, 1:] = alleinspielerCards[1:, 1:][newOrder, :]
                gedrueckt[1:, 1:] = gedrueckt[1:, 1:][newOrder, :]
                cardPlaysOneHot[:, :, :, 1:, 1:] = cardPlaysOneHot[:, :, :, 1:, 1:][:, :, :, newOrder, :]
            else:
                raise ValueError('Für diesen Spieltyp noch nicht implementiert!')

        return [augenSumAlleinSpieler, augenSumGegenSpieler, alleinspielerCards, gedrueckt, cardPlaysOneHot]

    def getFeaturesAlleinspieler_v5(self, round, permutate):
        if round >= self.playedFullRounds:
            raise ValueError('Runde existiert gar nicht!')
        if self.gameType not in ['C', 'S', 'H', 'D']:
            raise ValueError('Für diesen Spieltyp noch nicht implementiert!')

        # Reizungen werden weggelassen

        # Skat und drücken berücksichtigen, um Starthand zu bestimmen
        alleinspielerCards = self.playerCards[self.alleinspielerInd, :, :].copy()
        alleinspielerCards += self.skatCards - self.gedrueckt
        opponentInds = [0, 1, 2]
        opponentInds.pop(self.alleinspielerInd)
        opponentCardsUnshuffled = np.sum(self.playerCards[opponentInds, :, :], axis=0)

        cardPlaysOneHot = np.zeros((3, 3, 10, 4, 8), dtype=np.uint8)
        for i in range(cardPlaysOneHot.shape[0]):
            for j in range(cardPlaysOneHot.shape[1]):
                for k in range(round+1):
                    cardIndUInt8 = self.cardPlays[i, j, k]
                    if cardIndUInt8 > 0:
                        farbInd = (cardIndUInt8 - 1) // 8
                        kartenInd = (cardIndUInt8 - 1) - 8 * farbInd
                        cardPlaysOneHot[i, j, k, farbInd, kartenInd] = 1
                        if i == self.alleinspielerInd:
                            if not k == round:
                                alleinspielerCards[farbInd, kartenInd] = 0
                            else:
                                currentASCardUnshuffled = [farbInd, kartenInd]
                        if not i == self.alleinspielerInd and not k == round:
                            opponentCardsUnshuffled[farbInd, kartenInd] = 0
                        if j == 0 and k == round:
                            bedienCardUnshuffled = [farbInd, kartenInd]

        # Wenn der Alleinspieler Vorhand oder Mittelhand ist, spätere Karten in dieser Runde löschen
        positionInThisRound = np.where(self.cardPlays[self.alleinspielerInd, :, round] > 0)[0][0]
        if positionInThisRound < 2:
            cardPlaysOneHot[:, positionInThisRound+1:, round, :, :] = 0

        # Der Alleinspieler bekommt immer den Spieler-Index 0
        playerOrderNew = np.roll(np.array([0, 1, 2]), -self.alleinspielerInd)
        cardPlaysOneHot = cardPlaysOneHot[playerOrderNew, :, :, :, :]

        # Beim Farbspiel wird immer Trumpf in die 1. Zeile geschoben
        gedrueckt = self.gedrueckt.copy()
        trumpfInd = ['C', 'S', 'H', 'D'].index(self.gameType[0])
        newFarbOrder = [0, 1, 2, 3]
        newFarbOrder.insert(0, newFarbOrder.pop(trumpfInd))
        alleinspielerCards[:, 1:] = alleinspielerCards[newFarbOrder, 1:]
        opponentCardsShuffled = opponentCardsUnshuffled.copy()
        opponentCardsShuffled[:, 1:] = opponentCardsShuffled[newFarbOrder, 1:]
        gedrueckt[:, 1:] = gedrueckt[newFarbOrder, 1:]
        cardPlaysOneHot[:, :, :, :, 1:] = cardPlaysOneHot[:, :, :, newFarbOrder, 1:]
        currentASCardShuffled = currentASCardUnshuffled
        if currentASCardShuffled[1] > 0:
            currentASCardShuffled[0] = newFarbOrder.index(currentASCardUnshuffled[0])
        bedienCardShuffled = bedienCardUnshuffled
        if bedienCardShuffled[1] > 0:
            bedienCardShuffled[0] = newFarbOrder.index(bedienCardUnshuffled[0])

        # Merkmal der derzeitigen Augen bestimmen
        # Vorberechnete Augenanzahl aus der vorherigen Runde nutzen
        augenSumAlleinSpieler = np.array([self.alleinspielerAugen[round]])
        augenSumGegenSpieler = np.array([self.gegenspielerAugen[round]])
        # Wenn der Alleinspieler Hinterhand ist, kann man die aktuelle Runde bereits auswerten.
        # Ansonsten zählen nur alle Stiche bis zu dieser Runde.
        thisStichAugen, stichGewonnen = getStichPointsForRoundFarbspiel(cardPlaysOneHot, round)
        if np.sum(self.cardPlays[self.alleinspielerInd, 2, round] > 0):
            farbInd = (self.cardPlays[self.alleinspielerInd, 2, round] - 1) // 8
            kartenInd = (self.cardPlays[self.alleinspielerInd, 2, round] - 1) - 8 * farbInd
            if kartenInd == 0:
                # Bube (nie geshuffled)
                alleinspielerCards[farbInd, kartenInd] = 0
            else:
                # Farbe: möglicherweise geshuffled
                alleinspielerCards[newFarbOrder.index(farbInd), kartenInd] = 0
            if thisStichAugen > 0:
                augenSumAlleinSpieler += thisStichAugen
            if thisStichAugen < 0:
                augenSumGegenSpieler -= thisStichAugen
        # Wenn der Alleinspieler Mittelhand ist und Vorhand die höhere Karte als Mittelhand hat,
        # kann man für die Gegenspieler bereits auswerten.
        if np.sum(self.cardPlays[self.alleinspielerInd, 1, round] > 0):
            farbInd = (self.cardPlays[self.alleinspielerInd, 1, round] - 1) // 8
            kartenInd = (self.cardPlays[self.alleinspielerInd, 1, round] - 1) - 8 * farbInd
            if kartenInd == 0:
                # Bube (nie geshuffled)
                alleinspielerCards[farbInd, kartenInd] = 0
            else:
                # Farbe: möglicherweise geshuffled
                alleinspielerCards[newFarbOrder.index(farbInd), kartenInd] = 0
            if thisStichAugen < 0:
                 augenSumGegenSpieler -= thisStichAugen

        numTrumpfOpponent = np.sum(opponentCardsShuffled[:, 0]) + np.sum(opponentCardsShuffled[0, 1:])
        numBedienCardsOpponent = 0
        higherBedienCardExists = 0
        if bedienCardShuffled[0] >= 1 and bedienCardShuffled[1] >= 1:
            bedienFarbeShuffled = bedienCardShuffled[0]
            numBedienCardsOpponent = np.sum(opponentCardsShuffled[bedienFarbeShuffled, 1:])
            if currentASCardShuffled[0] == bedienFarbeShuffled and currentASCardShuffled[1] >= 1:
                if np.sum(opponentCardsShuffled[bedienFarbeShuffled, 1:currentASCardShuffled[1]]) > 0:
                    higherBedienCardExists = 1
        higherTrumpfExists = 0
        if currentASCardShuffled[1] == 0:
            if np.sum(opponentCardsShuffled[0:currentASCardShuffled[0], 0]) > 0:
                higherTrumpfExists = 1
        elif currentASCardShuffled[0] == 0:
            if np.sum(opponentCardsShuffled[0, 0:currentASCardShuffled[1]]) > 0 or np.sum(opponentCardsShuffled[:, 0]) > 0:
                higherTrumpfExists = 1
        else:
            if numTrumpfOpponent > 0:
                higherTrumpfExists = 1
        currentlyHighestCardOnTable = int(stichGewonnen)
        backgroundInfo = np.array([currentlyHighestCardOnTable, numTrumpfOpponent, higherTrumpfExists, numBedienCardsOpponent, higherBedienCardExists])

        if permutate:
            if 'C' in self.gameType or 'S' in self.gameType or 'H' in self.gameType or 'D' in self.gameType:
                # Farbspiel: Nicht-Trümpfe zufällig austauschen
                newOrder = np.random.permutation([0, 1, 2])
                alleinspielerCards[1:, 1:] = alleinspielerCards[1:, 1:][newOrder, :]
                gedrueckt[1:, 1:] = gedrueckt[1:, 1:][newOrder, :]
                cardPlaysOneHot[:, :, :, 1:, 1:] = cardPlaysOneHot[:, :, :, 1:, 1:][:, :, :, newOrder, :]
            else:
                raise ValueError('Für diesen Spieltyp noch nicht implementiert!')

        return [augenSumAlleinSpieler, augenSumGegenSpieler, backgroundInfo, alleinspielerCards, opponentCardsShuffled, cardPlaysOneHot[:,:,round,:,:]]