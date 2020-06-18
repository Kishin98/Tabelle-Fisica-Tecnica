import tkinter as tk
import pandas as pd
import os, re

commandPattern1 = re.compile(r'''(^f:(a|r)
                                \so:(hl|hv|sl|sv|vl|vv|ps|ts|ul|uv)
                                \s(p|t):(-?(\d+(\.|\,))?\d+)$
                                )''', re.VERBOSE)
commandPattern2 = re.compile(r'''(^f:(a|r) #bifase fornendo titolo o titolo fornendo v/h/s
                                \so:(h|s|v|x|u)
                                \s(p|t):(-?(\d+(\.|\,))?\d+)
                                \s(h|s|x|v|u):(-?(\d+(\.|\,))?\d+)
                                )''', re.VERBOSE)
commandPattern3 = re.compile(r'''(^f:(as|rs)
                                \so:(h|s|v|t|u)
                                \sp:(-?(\d+(\.|\,))?\d+)
                                \s(t|h|s|v|u):(-?(\d+(\.|\,))?\d+)
                                )''', re.VERBOSE)

firstDataPattern = re.compile(r'(p|t):(-?(\d+(\.|\,))?\d+)')

satWaterPressures = ['0.010', '0.050','0.100','0.200','0.300','0.400','0.500','0.600','0.800','1.000',
                    '1.200','1.400','1.600','1.800','2.000','2.500','3.000','3.500','4.000','4.500','5.000',
                    '6.000','7.000','8.000','9.000','10.00','12.50','15.00','17.50','20.00','25.00','30.00','40.00']

satRefPressures = ['0.030','0.040', '0.050','0.060','0.080','0.100','0.150','0.200','0.300','0.350','0.400',
                    '0.500','0.600','0.800','1.000','1.500','2.000','2.500']

def unit(par):
    if par == 'h' or par == 'hl'or par == 'hv' :
        return '[kj/kg]'
    if par == 's'or par == 'sl'or par == 'sv' :
        return '[kj/kg*k]'
    if par == 'p' or par == 'ps' :
        return '[MPa]'
    if par == 't' or par == 'ts' :
        return '[°C]'
    if par == 'v'or par == 'vl'or par == 'vv' :
        return '[m^3/kg]'
    if par == 'u'or par == 'ul'or par == 'uv' :
        return '[kj/kg]'
    if par == 'x' :
        return ''
    return ''

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
    if(operation == 'u'):
        return ['ul', 'uvl']

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
    print(operation + " = " + str(result) + unit(operation) + '\n')
    print('-' * os.get_terminal_size().columns)
    if(result < 0): #could happen from bad input
        print('WARNING: titolo < 0')
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
    print(operation + " = " + str(result) + unit(operation) + '\n')
    print('-' * os.get_terminal_size().columns)
    if(operation == 'v' and result < 0): #could happen from bad input
        print('WARNING: volume specifico < 0')
        print('-' * os.get_terminal_size().columns)
    return result

def interpolation(table, fluid, pressure, operation, typeOfSecondData, secondData):
    smaller = table.loc[table[typeOfSecondData] == table[typeOfSecondData][table[typeOfSecondData] < secondData].max()]
    greater = table.loc[table[typeOfSecondData] == table[typeOfSecondData][table[typeOfSecondData] > secondData].min()]
    if(smaller.empty or greater.empty):
        print(typeOfSecondData + ' potrebbe essere troppo piccola e quindi il fluido è in stato BIFASE!')
        print('-' * os.get_terminal_size().columns)
        print('Ecco la riga corrispondente alla temperatura di saturazione a p =' + pressure +'[MPa]:')
        print(table.head(1))
        print('-' * os.get_terminal_size().columns)
        print('Oppure ' + typeOfSecondData + ' è troppo grande e non rientra in tabella!')
        print('-' * os.get_terminal_size().columns)
        print('Ecco l\'ultima riga a p =' + pressure +'[MPa]:')
        print(table.tail(1))
        return None
    else:
        print('-' * os.get_terminal_size().columns)
        print('Riga valori minori tabella '+ fluid +' (p = '+ pressure + '[MPa]) : ')
        print(smaller)
        print('-' * os.get_terminal_size().columns)
        print('Riga valori maggiori tabella '+ fluid +' (p = '+ pressure + '[MPa]) : ')
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
        + '=\n' + operation + ' = ' +str(result) + unit(operation) + '\n')
        print('-' * os.get_terminal_size().columns)
        return result

def help():
    print('-' * os.get_terminal_size().columns)
    print('Valori accettabili:')
    print('<Fluido> : a -> acqua satura; as -> acqua surriscaldata; r -> R134a saturo; rs -> R14a surriscaldato')
    print('<Incognita> :\n'+
    'h -> entalpia; hl -> entalpia licquido saturo; hv -> entalpia vapore saturo\n' +
    's -> entropia; sl -> entropia liquido saturo; sv -> entropia vapore saturo\n' + 
    'v -> volume specifico; vl -> volume specifico liquido saturo; vv -> volume specifico vapore saturo\n' + 
    'u -> energia interna; ul -> energia interna liquido saturo; uv -> energina interna vapore saturo\n' +
    'x -> titolo di vapore; ts -> temperatura di saturazione; ps -> pressione di saturazione')
    print('Per <Dato1> e <Dato2> inserire la lettera corrispondente alla grandezza seguito dal valore numerico\n')
    print('<Dato1>: \n' + 
    'p -> pressione [MPa]; t -> premperatura [°C]; NB: con as e rs si potrà fornire solo la pressione come primo dato di ingresso!')
    print('<Dato2>: \n'+
    'p -> pressione [MPa]; t -> premperatura [°C]; h -> entalpia [kj/kg]; s -> entropia [kj/kg*k]\n' + 
    'u -> energina interna [kj/kg]; v -> volume specifico [m^3/kg]; x -> titolo;\n' + 
    'NB: con as e rs è NON è possibile fornire la pressione e il titolo come secondo dato!')
    print('-' * os.get_terminal_size().columns)
    print('Esempi:')
    print('<Fluido>:a <Incognita>:hl <Dato1>:t20    -> ottengo entalpia di liquido saturo dell\'acqua a 20[°C]')
    print('<Fluido>:r <Incognita>:h <Dato1>:p2 <Dato2>:x0.87   -> ottengo entalpia di R134a con titolo di vapore = 0.87 a 2[MPa]')
    print('<Fluido>:as <Incognita>:h <Dato1>:p3 <Dato2>:t225   -> ottengo entalpia dell\'acqua surriscaldata a 3[MPa] e 225[°C]')
    print('<Fluido>:a <Incognita>:h <Dato1>:p3 <Dato2>:s2.9635   -> ottengo entalpia dell\'acqua surriscaldata a 3[MPa] fornendo l\'entropia')
    print('-' * os.get_terminal_size().columns)

def convCommaToDot(string):
    if(',' in string):
        return string.replace(',', '.')
    return string

fields = 'Fluido', 'Incognita', 'Dato1', 'Dato2'

def fetch(entries):
    if(len(entries[3][1].get()) == 0):
        command = 'f:' + entries[0][1].get() + ' o:' + entries[1][1].get() + ' ' + entries[2][1].get()[0] + ':' + convCommaToDot(entries[2][1].get()[1:len(entries[2][1].get())])
        print(command)
        for entry in entries:
            field = entry[0]
            text  = entry[1].get()
            print('%s: "%s"' % (field, text)) 
    else:
        command = 'f:' + entries[0][1].get() + ' o:' + entries[1][1].get() + ' ' + entries[2][1].get()[0] + ':' + convCommaToDot(entries[2][1].get()[1:len(entries[2][1].get())]) + ' ' + entries[3][1].get()[0] + ':' + convCommaToDot(entries[3][1].get()[1:len(entries[3][1].get())])
        print(command)
        for entry in entries:
            field = entry[0]
            text  = entry[1].get()
            print('%s: "%s"' % (field, text)) 
    print('-' * os.get_terminal_size().columns)


    if(commandPattern1.match(command)): #a, r with 1 data

        fluid = getFluid(command)# a|r

        operation = getOperation(command) #hl|hv|sl|sv|vl|vv|ps|ts

        typeOfFirstData = getTypeOfFirstData(command) # p|t 
        firstData = float(getFirstData(command)) #value of p|t

        table = pd.read_excel(fluid + typeOfFirstData + '.xlsx')
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
            print(operation + ": " + str(result) + unit(operation) + '\n')
            print('-' * os.get_terminal_size().columns)


    elif(commandPattern2.match(command)): # a, r with 2 data
        fluid = getFluid(command) #a|r

        operation = getOperation(command) # h|s|v|x to e found

        typeOfFirstData = getTypeOfFirstData(command) # p|t
        firstData = float(getFirstData(command)) #value of p|t

        typeOfSecondData = getTypeOfSecondData(command) # h|s|v|x
        secondData = float(getSecondData(command)) #value of h|s|v|x

        table = pd.read_excel(fluid + typeOfFirstData + '.xlsx')
        row = table.loc[table[typeOfFirstData] == firstData]
        if(row.empty):
            print('-' * os.get_terminal_size().columns)
            print('La ' + typeOfFirstData + ' inserita non c\'è nelle tabelle!')
            print('-' * os.get_terminal_size().columns)
        else:
            if((operation == 'h' or operation == 's' or operation == 'v' or operation == 'u') and typeOfSecondData == 'x'):

                result = findVHS(secondData, row, fluid, typeOfFirstData, operation)

            elif(operation == 'x' and (typeOfSecondData == 'h' or typeOfSecondData == 's' or typeOfSecondData == 'v' or typeOfSecondData == 'u')):

                result = findTitolo(typeOfSecondData, secondData, row, fluid, typeOfFirstData, operation)

            elif((operation == 'h' and (typeOfSecondData == 'v' or typeOfSecondData == 's' or typeOfSecondData == 'u')) or
            (operation == 's' and (typeOfSecondData == 'v' or typeOfSecondData == 'h' or typeOfSecondData == 'u')) or
            (operation == 'v' and (typeOfSecondData == 'h' or typeOfSecondData == 's' or typeOfSecondData == 'u')) or
            (operation == 'u' and (typeOfSecondData == 'v' or typeOfSecondData == 's' or typeOfSecondData == 'h'))):

                print('Calcolo il titolo con '+ typeOfSecondData +' :')
                titolo = findTitolo(typeOfSecondData, secondData, row, fluid, typeOfFirstData, 'x')
                print('Calcolo ' + operation + ' con il titolo calcolato precedentemente: ')
                result = findVHS(titolo, row, fluid, typeOfFirstData, operation)

            else:
                print('ERROR!')


    elif(commandPattern3.match(command)): # as, rs with 2 data
        fluid = getFluid(command) #as|rs

        operation = getOperation(command) # h|s|v|t to be found

        pressure = getFirstData(command) #p

        typeOfSecondData = getTypeOfSecondData(command) # h|s|v|t
        secondData = float(getSecondData(command)) # value of h|s|v|t

        if(len(pressure) > 5 or (len(pressure) >= 4 and not '.' in pressure)):
            print('ERROR! La pressione inserita è troppo piccola o troppo grande! Il range delle pressioni per ' + fluid + ' è:')
            print('Ecco il range delle pressioni disponibili: ')
            if(fluid == 'as'):
                for i in satWaterPressures:
                    print(i + '[MPa]')
            if(fluid == 'rs'):
                for i in satRefPressures:
                    print(i + '[MPa]')
        else:
            if (fluid == 'as' and getPressureFormat(pressure) in satWaterPressures) or (fluid == 'rs' and getPressureFormat(pressure) in satRefPressures):
                table = pd.read_excel(fluid + getPressureFormat(pressure) + '.xlsx')
                row = table.loc[table[typeOfSecondData] == secondData]
                if(row.empty):

                    result = interpolation(table, fluid, pressure, operation, typeOfSecondData, secondData)

                else:
                    result = float(row[operation])
                    print('-' * os.get_terminal_size().columns)
                    print('Riga tabella '+ fluid +' (p = '+ pressure + '[MPa]) : ')
                    print(row)
                    print('-' * os.get_terminal_size().columns)
                    print(operation + ": " + str(result) + unit(operation) + '\n')
                    print('-' * os.get_terminal_size().columns)
            elif (fluid == 'as' and (float(pressure) < float(satWaterPressures[0]) or float(pressure) > float(satWaterPressures[32]))) or (fluid == 'rs' and (float(pressure) < float(satRefPressures[0]) or float(pressure) > float(satRefPressures[17]))):
                print('ERROR! La pressione inserita è troppo piccola o troppo grande! Il range delle pressioni per ' + fluid + ' è:')
                if(fluid == 'as'):
                    print(satWaterPressures[0] + '[MPa] - ' + satWaterPressures[32] + '[MPa]')
                if(fluid == 'rs'):
                    print(satRefPressures[0] + '[MPa] - ' + satRefPressures[17] + '[MPa]')
            else:
                if(fluid == 'as'): # if i'm here pressure is within the range
                    for i in reversed(satWaterPressures):
                        if float(i) < float(pressure):
                            smallerPressure = i
                            break
                    for i in satWaterPressures:
                        if float(i) > float(pressure):
                            greaterPressure = i
                            break
                if(fluid == 'rs'):
                    for i in reversed(satRefPressures):
                        if float(i) < float(pressure):
                            smallerPressure = i
                            break
                    for i in satRefPressures:
                        if float(i) > float(pressure):
                            greaterPressure = i
                            break
                smallerTable = pd.read_excel(fluid + smallerPressure + '.xlsx')
                greaterTable = pd.read_excel(fluid + greaterPressure + '.xlsx')
                smaller = smallerTable.loc[smallerTable[typeOfSecondData] == secondData]
                greater = greaterTable.loc[greaterTable[typeOfSecondData] == secondData]
                if(smaller.empty or greater.empty):
                    print('Interpolazione tabella '+ fluid +' a p = '+ smallerPressure + '[MPa] per '+ typeOfSecondData +' = ' + str(secondData) + unit(typeOfSecondData))
                    op1 = interpolation(smallerTable, fluid, smallerPressure, operation, typeOfSecondData, secondData)
                    print('Interpolazione tabella '+ fluid +' a p = '+ greaterPressure + '[MPa] per '+ typeOfSecondData +' = ' + str(secondData) + unit(typeOfSecondData))
                    op2 = interpolation(greaterTable, fluid, greaterPressure, operation, typeOfSecondData, secondData)
                    smallerOperation = min(op1, op2)
                    greaterOperation = max(op1, op2)
                    if not(smallerOperation is None or greaterOperation is None):
                        smallerSecondData = float(smallerPressure)
                        greaterSecondData = float(greaterPressure)
                        result = smallerOperation + ((float(pressure) - smallerSecondData)/(greaterSecondData - smallerSecondData)) * (greaterOperation - smallerOperation)
                        print('Interpolazione con '+ operation +'min = '+ str(smallerOperation) + unit(operation) +' e ' + operation + 'max = '+ str(greaterOperation) + unit(operation))
                        print('-' * os.get_terminal_size().columns)
                        print(operation + ' = ' + operation + 'min '+ '+ ((p - pmin' + ')/(pmax ' + ' - pmin' + ')) * (' + operation + 'max ' + ' - ' + operation + 'min' + ')' 
                        + ' = \n' + operation + ' = '  + str(smallerOperation)+ ' + ((' + pressure + ' - ' + str(smallerSecondData) + ')/(' + str(greaterSecondData) + ' - ' + str(smallerSecondData) + ')) * (' + str(greaterOperation) + ' - ' + str(smallerOperation) + ')'
                        + '=\n' + operation + ' = ' +str(result) + unit(operation) + '\n')
                        print('-' * os.get_terminal_size().columns)
                else:
                    print('-' * os.get_terminal_size().columns)
                    print('Riga valori minori tabella '+ fluid +' (p = '+ smallerPressure + '[MPa]) : ')
                    print(smaller)
                    print('-' * os.get_terminal_size().columns)
                    print('Riga valori maggiori tabella '+ fluid +' (p = '+ greaterPressure + '[MPa]) : ')
                    print(greater)
                    print('-' * os.get_terminal_size().columns)
                    smallerOperation = float(smaller[operation])
                    greaterOperation = float(greater[operation])
                    smallerSecondData = float(smallerPressure)
                    greaterSecondData = float(greaterPressure)
                    result = smallerOperation + ((float(pressure) - smallerSecondData)/(greaterSecondData - smallerSecondData)) * (greaterOperation - smallerOperation)
                    print('-' * os.get_terminal_size().columns)
                    print(operation + ' = ' + operation + 'min '+ '+ ((p - pmin' + ')/(pmax ' + ' - pmin' + ')) * (' + operation + 'max ' + ' - ' + operation + 'min' + ')' 
                    + ' = \n' + operation + ' = '  + str(smallerOperation)+ ' + ((' + pressure + ' - ' + str(smallerSecondData) + ')/(' + str(greaterSecondData) + ' - ' + str(smallerSecondData) + ')) * (' + str(greaterOperation) + ' - ' + str(smallerOperation) + ')'
                    + '=\n' + operation + ' = ' +str(result) + unit(operation) + '\n')
                    print('-' * os.get_terminal_size().columns)
    else:
        print('ERROR!')

def makeform(root, fields):
    entries = []
    for field in fields:
        row = tk.Frame(root)
        lab = tk.Label(row, width=15, text=field, anchor='w')
        ent = tk.Entry(row)
        row.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
        lab.pack(side=tk.LEFT)
        ent.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.X)
        entries.append((field, ent))
    return entries

if __name__ == '__main__':
    root = tk.Tk('ciao')
    ents = makeform(root, fields)
    root.bind('<Return>', (lambda event, e=ents: fetch(e)))   
    b1 = tk.Button(root, text='Show',
                  command=(lambda e=ents: fetch(e)))
    b1.pack(side=tk.LEFT, padx=5, pady=5)
    b2 = tk.Button(root, text='Help', command=(lambda : help()))
    b2.pack(side=tk.LEFT, padx=5, pady=5)
    b3 = tk.Button(root, text='Quit', command=root.quit)
    b3.pack(side=tk.LEFT, padx=5, pady=5)
    
    root.mainloop()