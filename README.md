# Tabelle-Fisica-Tecnica
Calcolo automatico di valori esatti di alcune grandezze termodinamiche utilizzando tabelle empiriche

Tutti i procedimenti effettuati per calcolare i risultati vengono mostrati

**Interpolazione lineare automatica**

Per eseguire il programma aprire il file ```TablesData.exe```

~~Le istruzioni sono così formattate:~~ Ora è disponibile una GUI molto semplice

![GUI](https://github.com/Kishin98/Tabelle-Fisica-Tecnica/blob/master/image/GUITabelleFisicaTecnica.PNG)

Valori accettabili:

```<fluido>``` : ```a``` -> acqua satura; ```as``` -> acqua surriscaldata; ```r ```-> R134a saturo; ```rs``` -> R14a surriscaldato

```<incognita da trovare>``` :

```h``` -> entalpia; ```hl``` -> entalpia liquido saturo; ```hv``` -> entalpia vapore saturo

```s``` -> entropia; ```sl``` -> entropia liquido saturo; ```sv``` -> entropia vapore saturo

```v``` -> volume specifico; ```vl``` -> volume specifico liquido saturo; ```vv``` -> volume specifico vapore saturo

```x``` -> titolo di vapore; ```ts``` -> temperatura di saturazione; ```ps``` -> pressione di saturazione

Nei campi ```<Dato1>``` e ```<Dato2>``` bisogna inserire la lettera della grandezza seguito dal valore numerico (i numeri decimali possono essere indicati sia con la ```,``` che con il ```.```)
Esempio: ```p2``` -> pressione = 2MPa

```<Dato1>```: ```p``` -> pressione **[MPa]**; ```t``` -> premperatura **[°C]**; **NB: con ```as``` e ```rs``` si potrà fornire solo la pressione come primo dato di ingresso!**

```<Dato2>```: ```p``` -> pressione **[MPa]**; ```t``` -> premperatura **[°C]**; ```h``` -> entalpia **[kj/kg]**; ```s``` -> entropia **[kj/kg\*k]**  

```v``` -> volume specifico **[m^3/kg]**; ```x``` -> titolo; **NB: con ```as``` e ```rs``` è NON è possibile fornire la pressione e il titolo come secondo dato!** 

**NB:Se è necessario un solo dato per trovare la grandezza desiderata lasciare ```<Dato2>``` vuoto**

I risultati saranno stampati sul termilale abbinato

![TERMINALE](https://github.com/Kishin98/Tabelle-Fisica-Tecnica/blob/master/image/CLITabelleFisicaTecnica.PNG)

# Esempi:

1. Ottengo l'entalpia di liquido saturo dell'acqua fornendo la pressione:

![TERMINALE](https://github.com/Kishin98/Tabelle-Fisica-Tecnica/blob/master/image/esempiohl.png)


2. Ottengo l'entalpia del R134a fornendo la pressione e il titolo:

![TERMINALE](https://github.com/Kishin98/Tabelle-Fisica-Tecnica/blob/master/image/esempioTitolo.png)


3. Ottengo l'entalpia dell'acqua fornendo l'entropia, il titolo viene calcolato autimaticamente:

![TERMINALE](https://github.com/Kishin98/Tabelle-Fisica-Tecnica/blob/master/image/esempioTitoloAuto.png)


4. Sapendo di essere nelle condizioni si acqua surriscaldata, ottengo l'entalpia fornendo la pressione e la temperatura:
![TERMINALE](https://github.com/Kishin98/Tabelle-Fisica-Tecnica/blob/master/image/esempioAcquaSurr.png)


5. Interpolazione automatica fornendo una temperatura intermedia non direttamente riportata in tabella:
![TERMINALE](https://github.com/Kishin98/Tabelle-Fisica-Tecnica/blob/master/image/esempioInterpolazioneTemp.png)


6. Interpolazione automatica fornendo una pressione intermedia non direttamente riportata in tabella:
![TERMINALE](https://github.com/Kishin98/Tabelle-Fisica-Tecnica/blob/master/image/esempioInterpolazionePres.png)


7. Interpolazione "doppia" fornendo pressioe e temperatura intermedie non presenti nelle tabelle:
![TERMINALE](https://github.com/Kishin98/Tabelle-Fisica-Tecnica/blob/master/image/EsempioDoppiaInterpolazione.png)


8. Inserimento di valori negativi:
![TERMINALE](https://github.com/Kishin98/Tabelle-Fisica-Tecnica/blob/master/image/esempioNegativo.png)


9. Nel caso di risultati improbabili viene lanciato un warning:
![TERMINALE](https://github.com/Kishin98/Tabelle-Fisica-Tecnica/blob/master/image/esempioWarningNegativo.png)
