def same_name(betName, statName):
    betName = betName.lower()
    statName = statName.lower()
    bLast = ""
    sLast = ""
    for x in betName.split():
        if (x == betName.split()[len(betName.split()) - 1]):
            bFirstLetter = x.split(".")[0]
            break
        bLast = bLast + x
    bLast = bLast.replace("-", " ")
    for x in statName.split():
        if (x == statName.split()[0]):
            sFirstLetter = statName.split()[0][0]
            continue
        sLast = sLast + x
    if (bLast == sLast and sFirstLetter == bFirstLetter):
        return (True)
    else:
        return (False)

def last_f_convert(firstLast):
    firstLast = firstLast.lower()
    sLast = ""
    for x in firstLast.split():
        if (x == firstLast.split()[0]):
            sFirstLetter = firstLast.split()[0][0]
            continue
        sLast = sLast + x
    return (sLast + " " + sFirstLetter + '.')

def cleanBetName(lastF):
    lastF = lastF.lower()
    if ("-" in lastF):
        lastF = lastF.replace("-", " ")
    return (lastF)
