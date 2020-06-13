# Tabelle-Fisica-Tecnica
Calcolo automatico di alcune grandezze termodinamiche utilizzando tabelle empiriche

**Interpolazione lineare automatica**

Per eseguire il programma aprire il file ```TablesData.exe```

~~Le istruzioni sono coì formattate:~~Ora è disponibile una GUI molto semplice

![GUI](https://github.com/Kishin98/Tabelle-Fisica-Tecnica/blob/master/images/GUITabelleFisicaTecnica.PNG)

Valori accettabili:

```<fluido>``` : ```a``` -> acqua satura; ```as``` -> acqua surriscaldata; ```r ```-> R134a saturo; ```rs``` -> R14a surriscaldato

```<incognita da trovare>``` :

```h``` -> entalpia(bifase o surriscaldato); ```hl``` -> entalpia licquido saturo; ```hv``` -> entalpia vapore saturo

```s``` -> entropia(bifase o surriscaldato); ```sl``` -> entropia liquido saturo; ```sv``` -> entropia vapore saturo

```v``` -> volume specifico(bifase o surriscaldato); ```vl``` -> volume specifico liquido saturo; ```vv``` -> volume specifico vapore saturo

```x``` -> titolo di vapore; ```ts``` -> temperatura di saturazione; ```ps``` -> pressione di saturazione

Nei campi ```<Dato1>``` e ```<Dato2>``` bisogna inserire la lettera della grandezza seguito dal valore numerico

```<Dato1>```: ```p``` -> pressione **[MPa]**; ```t``` -> premperatura **[°C]**; **NB: con ```as``` e ```rs``` si potrà fornire solo la pressione come primo dato di ingresso!**

```<Dato2>```: ```p``` -> pressione **[MPa]**; ```t``` -> premperatura **[°C]**; ```h``` -> entalpia **[kj/kg]**; ```s``` -> entropia **[kj/kg\*k]**  

```v``` -> volume specifico **[m^3/kg]**; ```x``` -> titolo; **NB: con ```as``` e ```rs``` è NON è possibile fornire la pressione e il titolo come secondo dato!** 

**NB:Se è necessario un solo dato per trovare la grandezza desiderata lasciare ```<Dato2>``` vuoto**

I risultati saranno stampati sul termilale abbinato

![TERMINALE](https://github.com/Kishin98/Tabelle-Fisica-Tecnica/blob/master/images/CLITabelleFisicaTecnica.PNG)

# Esempi:

```<Fluido>:a <Incognita>:hl <Dato1>:t20```    -> ottengo entalpia di liquido saturo dell'acqua a 20°C
```<Fluido>:r <Incognita>:h <Dato1>:p2 <Dato2>:x0.87```   -> ottengo entalpia di R134a con titolo di vapore = 0.87 a 2MPa
```<Fluido>:as <Incognita>:h <Dato1>:p3 <Dato2>:t225```   -> ottengo entalpia dell'acqua surriscaldata a 3MPa e 225°C
```<Fluido>:a <Incognita>:h <Dato1>:p3 <Dato2>:s2.9635```   -> ottengo entalpia dell'acqua surriscaldata a 3MPa fornendo l'entropia
