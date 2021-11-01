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
    bLast = bLast.replace("-", "")
    bLast = bLast.replace("'", "")
    for x in statName.split():
        if (x == statName.split()[0]):
            sFirstLetter = statName.split()[0][0]
            continue
        sLast = sLast + x
    sLast = sLast.replace("-", "")
    sLast = sLast.replace("'", "")
    if ((bLast in sLast or sLast in bLast) and sFirstLetter == bFirstLetter):
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
    sLast = sLast.replace("-", "")
    sLast = sLast.replace("'", "")
    return (sLast + " " + sFirstLetter + '.')

def cleanBetName(lastF):
    lastF = lastF.lower()
    bLast = ""
    for x in lastF.split():
        if (x == lastF.split()[len(lastF.split()) - 1]):
            bFirstLetter = x.split(".")
            break
        bLast = bLast + x
    bLast = bLast.replace("-", "")
    bLast = bLast.replace("'", "")
    return (bLast, bFirstLetter)
