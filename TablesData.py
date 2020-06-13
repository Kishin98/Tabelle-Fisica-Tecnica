import pandas as pd
import os, re

kelvin = re.compile(r'\d+(\.|\,)?\d+k$')
celsius = re.compile(r'\d+(\.|\,)?\d+c$')
findNumber = re.compile(r'(\d+(\.|\,))?\d+')
commandPattern1 = re.compile(r'''(^f:(a|r)
                                \so:(hl|hv|sl|sv|vl|vv|ps|ts)
                                \s(p|t):(-?(\d+(\.|\,))?\d+)$
                                )''', re.VERBOSE)
commandPattern2 = re.compile(r'''(^f:(a|r) #bifase fornendo titolo o titolo fornendo v/h/s
                                \so:(h|s|v|x)
                                \s(p|t):(-?(\d+(\.|\,))?\d+)
                                \s(h|s|x|v):(-?(\d+(\.|\,))?\d+)
                                )''', re.VERBOSE)
commandPattern3 = re.compile(r'''(^f:(as|rs)
                                \so:(h|s|v)
                                \sp:(-?(\d+(\.|\,))?\d+)
                                \s(t|h|s|v):(-?(\d+(\.|\,))?\d+)
                                )''', re.VERBOSE)

firstDataPattern = re.compile(r'(p|t):(-?(\d+(\.|\,))?\d+)')

def getFluid(command):
    start = 0
    finish = 0
    for i in range(0, len(command)):
        if(command[i] == 'f'):
            start = i + 2
        if(command[i] == ' '):
            finish = i
            break
    return command[start: finish]

def getOperation(command):
    start = 0
    finish = 0
    for i in range(0, len(command)):
        if(command[i] == 'o'):
            start = i + 2
        if(command[i] == ' ' and start != 0):
            finish = i
            break
    return command[start: finish]

def getFirstData(command):
    temp = re.search(firstDataPattern, command).group()
    return temp[2:len(temp)]

def getTypeOfFirstData(command):
    temp = re.search(firstDataPattern, command).group()
    return temp[0]

def getTypeOfSecondData(command):
    for i in range(len(command) - 1, 0, -1):
        if(command[i] == ' '):
            return command[i + 1]

def getSecondData(command):
    for i in range(len(command) - 1, 0, -1):
        if(command[i] == ' '):
            return command[i + 3:len(command)]

def getOperands(operation):
    if(operation == 'h'):
        return ['hl', 'hvl']
    if(operation == 's'):
        return ['sl', 'svl']
    if(operation == 'v'):
        return ['vl', 'vvl']

def getPressureFormat(pressure):
    if(len(pressure) == 5):
        return pressure
    n = 5 - len(pressure)
    if('.' in pressure):
        return pressure + '0'*n
    return pressure + '.' + '0'*(n - 1)

def findTitolo(typeOfSecondData, secondData, row, fluid, typeOfFirstData, operation):
    l = float(row[getOperands(typeOfSecondData)[0]])
    vl = float(row[getOperands(typeOfSecondData)[1]])
    result = (secondData - l)/(vl)
    print('\nRiga della tabella' + ' ' + fluid + '-' + typeOfFirstData + ':\n')
    print('-' * os.get_terminal_size().columns)
    print(row)
    print('-' * os.get_terminal_size().columns)
    print(operation + ' = ' + '(' + typeOfSecondData + ' - ' + typeOfSecondData + 'l)/' + typeOfSecondData + 'vl =')
    print(operation + ' = ' + '(' + str(secondData) + ' - ' + str(l) + ')/' + str(vl) + ' =')
    print(operation + " = " + str(result) + '\n')
    print('-' * os.get_terminal_size().columns)
    return result

def findVHS(secondData, row, fluid, typeOfFirstData, operation):
    l = float(row[getOperands(operation)[0]])
    vl = float(row[getOperands(operation)[1]])
    result = l + secondData*vl
    print('\nRiga della tabella' + ' ' + fluid + '-' + typeOfFirstData + ':\n')
    print('-' * os.get_terminal_size().columns)
    print(row)
    print('-' * os.get_terminal_size().columns)
    print(operation + ' = ' + operation + 'l + x * ' + operation + 'vl =')
    print(operation + ' = ' + str(l) + ' + ' + str(secondData) + ' * ' + str(vl) + ' =')
    print(operation + " = " + str(result) + '\n')
    print('-' * os.get_terminal_size().columns)
    return result

# f:a o:hl t:20      trovare hl dell'acqua con la temperatura
# f:a o:sv p:2      trovare sv dell'acqua con la pressione
# f:r o:x p:2 s:0.9222    trovare il titolo del R134a con pressione e entropia
# f:as o:h p:2 t:250    trovare h dell'acqua surriscaldata con pressione e temperatura
# f:as o:h p:2 s:6.7854  trovare h dell'acqua surriscaldata con pressione e entropia 

print('Istruzioni:')
print('Se è necessario solo un dato in ingresso:')
print('f:<fluido> o:<incognita da trovare> <primo dato>:<valore numerico>')
print('Se sono necessari 2 dati in ingresso:')
print('f:<fluido> o:<incognita da trovare> <primo dato>:<valore numerico> <secondo dato>:<valore numerico>')
print('Valori accettabili:')
print('<fluido> : a -> acqua satura; as -> acqua surriscaldata; r -> R134a saturo; rs -> R14a surriscaldato')
print('<incognita da trovare> : h -> entalpia(bifase o surriscaldato); hl -> entalpia licquido saturo; hv -> entalpia vapore saturo\n'+
's -> entropia(bifase o surriscaldato); sl -> entropia liquido saturo; sv -> entropia vapore saturo\n' + 
'v -> volume specifico(bifase o surriscaldato); vl -> volume specifico liquido saturo; vv -> volume specifico vapore saturo\n' + 
'x -> titolo di vapore; ts -> temperatura di saturazione; ps -> pressione di saturazione')
print('<primo dato>: p -> pressione [MPa]; t -> premperatura [°C]; NB: con as e rs si potrà fornire solo la pressione come primo dato di ingresso!')
print('<secondo dato>: p -> pressione [MPa]; t -> premperatura [°C]; h -> entalpia [kj/kg]; s -> entropia [kj/kg*k]\n' + 
'v -> volume specifico [m^3/kg]; x -> titolo; NB: con as e rs è NON è possibile fornire la pressione e il titolo come secondo dato!')
print('-' * os.get_terminal_size().columns)
print('Esempi:')
print('f:a o:hl t:20    -> ottengo entalpia di liquido saturo dell\'acqua a 20°C')
print('f:r o:h p:2 x:0.87   -> ottengo entalpia di R134a con titolo di vapore = 0.87 a 2MPa')
print('f:as o:h p:3 t:225   -> ottengo entalpia dell\'acqua surriscaldata a 3MPa e 225°C')
print('-' * os.get_terminal_size().columns)
while(True):
    command = input('Inserisci un istruzione (\'exit\' per terminare; \'help\' per vedere il format delle istruzioni): ')
    if(command == 'exit'):
        break
    if(commandPattern1.match(command)): #a, r with 1 data
        fluid = getFluid(command)
        typeOfFirstData = getTypeOfFirstData(command)
        table = pd.read_excel(fluid + typeOfFirstData + '.xlsx')
        operation = getOperation(command)
        firstData = float(getFirstData(command))
        row = table.loc[table[typeOfFirstData] == firstData]
        if(row.empty):
            print('-' * os.get_terminal_size().columns)
            print('La ' + typeOfFirstData + ' inserita non c\'è nelle tabelle!')
            print('-' * os.get_terminal_size().columns)
        else:
            result = float(row[operation])
            print('\nRiga della tabella' + ' ' + fluid + '-' + typeOfFirstData + ':\n')
            print('-' * os.get_terminal_size().columns)
            print(row)
            print('-' * os.get_terminal_size().columns)
            print(operation + ": " + str(result) + '\n')
            print('-' * os.get_terminal_size().columns)
    elif(commandPattern2.match(command)): # a, r with 2 data
        fluid = getFluid(command)
        typeOfFirstData = getTypeOfFirstData(command)
        typeOfSecondData = getTypeOfSecondData(command)
        firstData = float(getFirstData(command))
        secondData = float(getSecondData(command))
        table = pd.read_excel(fluid + typeOfFirstData + '.xlsx')
        row = table.loc[table[typeOfFirstData] == firstData]
        if(row.empty):
            print('-' * os.get_terminal_size().columns)
            print('La ' + typeOfFirstData + ' inserita non c\'è nelle tabelle!')
            print('-' * os.get_terminal_size().columns)
        else:
            operation = getOperation(command)
            if((operation == 'h' or operation == 's' or operation == 'v') and typeOfSecondData == 'x'):
                result = findVHS(secondData, row, fluid, typeOfFirstData, operation)
            elif(operation == 'x' and (typeOfSecondData == 'h' or typeOfSecondData == 's' or typeOfSecondData == 'v')):
                result = findTitolo(typeOfSecondData, secondData, row, fluid, typeOfFirstData, operation)
            elif((operation == 'h' and typeOfSecondData == 's') or (operation == 's' and typeOfSecondData == 'h') or 
            (operation == 'v' and typeOfSecondData == 's') or (operation == 's' and typeOfSecondData == 'v') or
            (operation == 'h' and typeOfSecondData == 'v') or (operation == 'v' and typeOfSecondData == 'h')):
                print('-' * os.get_terminal_size().columns)
                print('Calcolo il titolo con '+ typeOfSecondData +' :')
                titolo = findTitolo(typeOfSecondData, secondData, row, fluid, typeOfFirstData, 'x')
                print('Calcolo ' + operation + ' con il titolo calcolato precedentemente: ')
                result = findVHS(titolo, row, fluid, typeOfFirstData, operation)
            else:
                print('-' * os.get_terminal_size().columns)
                print('ERROR!')
                print('-' * os.get_terminal_size().columns)
    elif(commandPattern3.match(command)): # as, rs with 2 data
        fluid = getFluid(command)
        operation = getOperation(command)
        pressure = getFirstData(command)
        secondData = float(getSecondData(command))
        typeOfSecondData = getTypeOfSecondData(command)
        if(len(pressure) > 5 or (len(pressure) >= 4 and not '.' in pressure)):
            print('La p inserita non c\'è nelle tabelle!\n')
        else:
            try:
                table = pd.read_excel(fluid + getPressureFormat(pressure) + '.xlsx')
                row = table.loc[table[typeOfSecondData] == secondData]
                if(row.empty):
                    smaller = table.loc[table[typeOfSecondData] == table[typeOfSecondData][table[typeOfSecondData] < secondData].max()]
                    greater = table.loc[table[typeOfSecondData] == table[typeOfSecondData][table[typeOfSecondData] > secondData].min()]
                    if(smaller.empty or greater.empty):
                        print(typeOfSecondData + ' è fuori range!')
                        print('-' * os.get_terminal_size().columns)
                        print('Ecco il range disponibile:')
                        print(table[typeOfSecondData])
                        print('-' * os.get_terminal_size().columns)
                        raise Exception
                    print('INTERPOLATIOOOOOOOON!!!!!!!\n')
                    print('-' * os.get_terminal_size().columns)
                    print('Riga valori minori tabella'+ fluid +' (p = '+ pressure + 'MPa) : ')
                    print(smaller)
                    print('-' * os.get_terminal_size().columns)
                    print('Riga valori maggiori tabella'+ fluid +' (p = '+ pressure + 'MPa) : ')
                    print(greater)
                    print('-' * os.get_terminal_size().columns)
                    smallerOperation = float(smaller[operation])
                    greaterOperation = float(greater[operation])
                    smallerSecondData = float(smaller[typeOfSecondData])
                    greaterSecondData = float(greater[typeOfSecondData])
                    result = smallerOperation + ((secondData - smallerSecondData)/(greaterSecondData - smallerSecondData)) * (greaterOperation - smallerOperation)
                    print('-' * os.get_terminal_size().columns)
                    print(operation + ' = ' + operation + 'min '+ '+ ((' + typeOfSecondData + ' - ' + typeOfSecondData + 'min' + ')/(' + typeOfSecondData + 'max ' + ' - ' + typeOfSecondData + 'min' + ')) * (' + operation + 'max ' + ' - ' + operation + 'min' + ')' 
                    + ' = \n' + operation + ' = '  + str(smallerOperation)+ ' + ((' + str(secondData) + ' - ' + str(smallerSecondData) + ')/(' + str(greaterSecondData) + ' - ' + str(smallerSecondData) + ')) * (' + str(greaterOperation) + ' - ' + str(smallerOperation) + ')'
                    + '=\n' + operation + ' = ' +str(result) + '\n')
                    print('-' * os.get_terminal_size().columns)
                else:
                    result = float(row[operation])
                    print('-' * os.get_terminal_size().columns)
                    print('Riga tabella '+ fluid +' (p = '+ pressure + 'MPa) : ')
                    print(row)
                    print('-' * os.get_terminal_size().columns)
                    print(operation + ": " + str(result) + '\n')
                    print('-' * os.get_terminal_size().columns)
            except:
                print('ERROR(La p potrebbe non esserci nelle tabelle oppure un parametro inserito è fuori range)!\n')
            
    elif(command == 'help'):
        print('-' * os.get_terminal_size().columns)
        print('Istruzioni:')
        print('Se è necessario solo un dato in ingresso:')
        print('f:<fluido> o:<incognita da trovare> <primo dato>:<valore numerico>')
        print('Se sono necessari 2 dati in ingresso:')
        print('f:<fluido> o:<incognita da trovare> <primo dato>:<valore numerico> <secondo dato>:<valore numerico>')
        print('Valori accettabili:')
        print('<fluido> : a -> acqua satura; as -> acqua surriscaldata; r -> R134a saturo; rs -> R14a surriscaldato')
        print('<incognita da trovare> : h -> entalpia(bifase o surriscaldato); hl -> entalpia licquido saturo; hv -> entalpia vapore saturo\n'+
        's -> entropia(bifase o surriscaldato); sl -> entropia liquido saturo; sv -> entropia vapore saturo\n' + 
        'v -> volume specifico(bifase o surriscaldato); vl -> volume specifico liquido saturo; vv -> volume specifico vapore saturo\n' + 
        'x -> titolo di vapore; ts -> temperatura di saturazione; ps -> pressione di saturazione')
        print('<primo dato>: p -> pressione [MPa]; t -> premperatura [°C]; NB: con as e rs si potrà fornire solo la pressione come primo dato di ingresso!')
        print('<secondo dato>: p -> pressione [MPa]; t -> premperatura [°C]; h -> entalpia [kj/kg]; s -> entropia [kj/kg*k]\n' + 
        'v -> volume specifico [m^3/kg]; x -> titolo; NB: con as e rs è NON è possibile fornire la pressione e il titolo come secondo dato!')
        print('-' * os.get_terminal_size().columns)
        print('Esempi:')
        print('f:a o:hl t:20    -> ottengo entalpia di liquido saturo dell\'acqua a 20°C')
        print('f:r o:h p:2 x:0.87   -> ottengo entalpia di R134a con titolo di vapore = 0.87 a 2MPa')
        print('f:as o:h p:3 t:225   -> ottengo entalpia dell\'acqua surriscaldata a 3MPa e 225°C')
        print('-' * os.get_terminal_size().columns)
    else:
        print('ERROR!')