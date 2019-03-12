Forklaring på highlighter:


Hver linje starter med default fargekode (gjøres i filen)

TODO forklart kopmlisert regex

Den endelige regexen
regex = 
f"        ({fargekode})?            (?!.*(?:{fargekode}).*{regex})      (.*){regex}"
 -valgfri foregående fargekode-  -ikke fargekoder mellom dette og match  -matchen-


Denne regexen kommer til slutt i den endelige regexen. Ingenting må matches foran denne i den endelige
regexen.  Derfor kan den første gruppen matche starten av linjen (pluss default fargekode som alltid
er der). Men man må matche en foregående fargekode med ENTEN gr.1 eller gr.6.
For eksempel, her er import statements regexen:
"     (^\033.+m)            ((?:import|from ).+)       ()": import
 --beginning of line--   --- imports til slutten--

regex:       (gruppe som ikke skal farges)(gruppe som skal farges)(gruppe som skal ha forrige farge)
mather på:      ------gr.6------                 ---gr.7-----            -----gr.8----- 

[FARGEKODE] [noe som ikke skal farges] FARGEKODE noe som ikke skal farges NOE SOM SKAL FARGES
                                       --gr.1--   -------gr.5-----------   -----gr.8------     
         
byttes ut med:  \1 \5 \6 <ny farge> \7 \1 \8

Der gr.1 er den gamle fargekoden, slik at den forrige fargen kommer etter den nye.



Jeg rakk ikke 5.6


