def ELO(Ra, Rb, result, K=25):

    if result == 'Обрати першу вайфу':
        Sa = 1
        Sb = 0
    elif result == 'Обрати другу вайфу':
        Sa = 0
        Sb = 1
    elif result == 'Не знаю жодної':
        Sa = 0.5
        Sb = 0.5

    Ea = 1/(1+10**((Rb-Ra)/400))
    Eb = 1/(1+10**((Ra-Rb)/400))
    
    Ka = K
    Kb = K
    if abs(Ra-1200) > 600:
        Ka = 15
    elif abs(Ra-1200) > 100:
        Ka = 20
    if abs(Rb-1200) > 600:
        Kb = 15
    elif abs(Rb-1200) > 100:
        Kb = 20


    change1 = round(Ka*(Sa-Ea))
    change2 = -round(Kb*(Sa-Ea))

    return change1, change2
    
