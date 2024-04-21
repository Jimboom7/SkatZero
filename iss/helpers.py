import numpy as np

def convertCardStringToMat(cardString, delimiter):
    cardMat = np.zeros((4, 8), dtype=np.uint8)
    strSplit = cardString.split(delimiter)
    for card in strSplit:
        cardMat[getIndsOfCardName(card)] = True
    return cardMat

def getIndsOfCardName(cardName):
    farben = ['C', 'S', 'H', 'D']
    werte = ['J', 'A', 'T', 'K', 'Q', '9', '8', '7']
    ind0 = farben.index(cardName[0])
    ind1 = werte.index(cardName[1])
    return ind0, ind1

def getCardName(ind0, ind1):
    farben = ['Kreuz', 'Pik', 'Herz', 'Karo']
    werte = ['Bube', 'Ass', '10', 'König', 'Dame', '9', '8', '7']
    return f'{farben[ind0]} {werte[ind1]}'

def getMatIndFromUInt8(indUint8):
    cardFarbInd = (indUint8 - 1) // 8
    cardKartenInd = (indUint8 - 1) - 8 * cardFarbInd
    return cardFarbInd, cardKartenInd

def getUInt8FromMatInds(cardFarbInd, cardKartenInd):
    thisCardUInt8 = (cardFarbInd * 8 + cardKartenInd) + 1
    return thisCardUInt8

def printCardMat(cardMat, printOnlyOnes):
    farben = ['Kreuz', 'Pik', 'Herz', 'Karo']
    werte = ['Bube', 'Ass', '10', 'König', 'Dame', '9', '8', '7']
    for i in range(4):
        if printOnlyOnes:
            if cardMat[i, 0] == 1:
                print(f'{farben[i]} {werte[0]}')
        else:
            if not np.isnan(cardMat[i, 0]):
                print(f'{farben[i]} {werte[0]} \t {cardMat[i, 0]}')

    for i in range(4):
        for j in range(1, 8):
            if printOnlyOnes:
                if cardMat[i, j] == 1:
                    print(f'{farben[i]} {werte[j]}')
            else:
                if not np.isnan(cardMat[i, j]):
                    print(f'{farben[i]} {werte[j]} \t {cardMat[i, j]}')


def getStichPointsAlleinspieler(thisStichAsMat, thisStichASInd, gameType):
    """ Annahme: Ausspielreihenfolge ist Vorhand, Mittelhand, Hinterhand.
        Erwartet genau einen Stich: ausspielInd x 4 x 8 - Matrix"""
    if gameType not in ['C', 'S', 'H', 'D', 'CH', 'SH', 'HH', 'DH']:
        raise ValueError('Dieser Spieltyp ist hier noch nicht implementiert!')

    wholeStich = np.sum(thisStichAsMat, axis=0)

    trumpfInd = ['C', 'S', 'H', 'D'].index(gameType[0])
    # bestimmen, wer den Stich gewonnen hat
    # Trumpf hat, wenn vorhanden, immer Vorrang

    if np.any(wholeStich[:, 0] > 0):
        # höchster Bube entscheidet
        besterFarbInd = np.min(np.where(wholeStich[:, 0])[0])
        # hat Spieler den besten Buben?
        gewinnerInd = np.where(thisStichAsMat[:, besterFarbInd, 0])[0][0]

    elif np.any(wholeStich[trumpfInd, 1:] > 0):
        # höchster Nicht-Buben-Trumpf entscheidet
        besterKartenInd = np.min(np.where(wholeStich[trumpfInd, :])[0])
        # hat Spieler den besten Nicht-Buben-Trumpf?
        gewinnerInd = np.where(thisStichAsMat[:, trumpfInd, besterKartenInd])[0][0]

    else:
        # kein Trumpf: Bedienfarbe ermitteln aus Vorhandausspiel
        vorhandAusspielMat = thisStichAsMat[0, :, :]
        bedienFarbInd = np.where(vorhandAusspielMat)[0][0]
        # höchsten Wert der Bedienfarbe bestimmen
        besterKartenInd = np.min(np.where(wholeStich[bedienFarbInd, :])[0])
        # hat Spieler die beste Bedienkarte?
        gewinnerInd = np.where(thisStichAsMat[:, bedienFarbInd, besterKartenInd])[0][0]

    # Runde aufaddieren und Punkte bestimmen (negativ, wenn Gegner Stich macht)
    if gewinnerInd == thisStichASInd:
        return getPointsForMat(wholeStich), gewinnerInd
    else:
        return -getPointsForMat(wholeStich), gewinnerInd


def getStichPointsForRoundFarbspiel(cardPlays, round):
    """ Annahme: Trumpf ist Farbindex 0, Spielerindex ist Index 0!
        Erwartet alle Stiche: spInd x orderInd x round x 4 x 8 - Matrix """
    cardPlaysThisRound = cardPlays[:, :, round, :, :]
    wholeStich = np.sum(cardPlaysThisRound[:, :, :, :], axis=(0, 1))
    stichGewonnen = False
    # bestimmen, wer den Stich gewonnen hat
    # Trumpf hat, wenn vorhanden, immer Vorrang

    if np.any(wholeStich[:, 0] > 0):
        # höchster Bube entscheidet
        besterFarbInd = np.min(np.where(wholeStich[:, 0])[0])
        # hat Spieler den besten Buben?
        if np.max(cardPlaysThisRound[0, :, besterFarbInd, 0]) == 1:
            stichGewonnen = True

    elif np.any(wholeStich[0, 1:] > 0):
        # höchster Nicht-Buben-Trumpf entscheidet
        besterKartenInd = np.min(np.where(wholeStich[0, :])[0])
        # hat Spieler den besten Nicht-Buben-Trumpf?
        if np.max(cardPlaysThisRound[0, :, 0, besterKartenInd]) == 1:
            stichGewonnen = True

    else:
        # kein Trumpf: Bedienfarbe ermitteln aus Vorhandausspiel
        vorhandAusspielMat = np.sum(cardPlaysThisRound[:, 0, :, :], axis=0)
        bedienFarbInd = np.where(vorhandAusspielMat)[0][0]
        # höchsten Wert der Bedienfarbe bestimmen
        besterKartenInd = np.min(np.where(wholeStich[bedienFarbInd, :])[0])
        # hat Spieler die beste Bedienkarte?
        if np.max(cardPlaysThisRound[0, :, bedienFarbInd, besterKartenInd]) == 1:
            stichGewonnen = True

    # Runde aufaddieren und Punkte bestimmen (negativ, wenn Gegner Stich macht)
    if stichGewonnen:
        return getPointsForMat(wholeStich), stichGewonnen
    else:
        return -getPointsForMat(wholeStich), stichGewonnen

def getPointsForMat(cardMat):
    columnSum = np.sum(cardMat, axis=0)
    points = np.sum(columnSum * getPointsForColumnInd(np.arange(8)))
    return points

def getPointsForColumnInd(columnInd):
    # Spaltenindex aus der 2D-Darstellung erwartet
    points = np.array([2, 11, 10, 4, 3, 0, 0, 0])
    return points[columnInd]

def getLegalMoves(bedienCardUInt8, cardMat, gameType):
    # prüft, welche Karten der Spieler mit cardMat schmeißen darf,
    # wenn bedienCardUInt8 als erste Karte auf dem Tisch liegt
    legalMask = getLegalMask(bedienCardUInt8, gameType)
    cardMat = cardMat.copy()
    if np.any(cardMat[legalMask]):
        # Bedienen ist möglich. Rest ist verboten.
        cardMat[np.logical_not(legalMask)] = 0
    return cardMat

def getLegalMask(bedienCardUInt8, gameType):
    """Annahme: Farben sind normal sortiert (C, S, H, D)"""
    if gameType not in ['C', 'S', 'H', 'D', 'CH', 'SH', 'HH', 'DH']:
        raise ValueError('Dieser Spieltyp ist hier noch nicht implementiert!')

    bedienFarbInd, bedienKartenInd = getMatIndFromUInt8(bedienCardUInt8)
    trumpfInd = ['C', 'S', 'H', 'D'].index(gameType[0])

    legalMask = np.zeros((4, 8), dtype=np.bool)
    if bedienKartenInd == 0 or bedienFarbInd == trumpfInd:
        # Trumpf (Bube oder Trumpf-Farbe)
        legalMask[:, 0] = True
        legalMask[trumpfInd, :] = True
    else:
        # Normale Bedienfarbe
        legalMask[bedienFarbInd, 1:] = True
    return legalMask
