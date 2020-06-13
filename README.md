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

```<primo dato>```: ```p``` -> pressione **[MPa]**; ```t``` -> premperatura **[°C]**; **NB: con ```as``` e ```rs``` si potrà fornire solo la pressione come primo dato di ingresso!**

```<secondo dato>```: ```p``` -> pressione **[MPa]**; ```t``` -> premperatura **[°C]**; ```h``` -> entalpia **[kj/kg]**; ```s``` -> entropia **[kj/kg\*k]**

```v``` -> volume specifico **[m^3/kg]**; ```x``` -> titolo; **NB: con ```as``` e ```rs``` è NON è possibile fornire la pressione e il titolo come secondo dato!**

# Esempi:

```f:a o:hl t:20```    -> ottengo entalpia di liquido saturo dell'acqua a 20°C

```f:r o:h p:2 x:0.87```   -> ottengo entalpia di R134a con titolo di vapore = 0.87 a 2MPa

```f:as o:h p:3 t:225```   -> ottengo entalpia dell'acqua surriscaldata a 3MPa e 225°C

```f:a o:x p:3 s:3.254```  -> ottengo titolo di vapore dell'acqua satura a 3MPa fornendo l'entropia
