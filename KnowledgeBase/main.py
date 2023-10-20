from pyswip import Prolog
from KB import *

kb = KB()
with open("base_conoscenza.pl", "r") as file:
    for riga in file:
        cl=riga.split(" :- ")
        body=[]
        if len(cl)>1:
            for atomo in cl[1].split(" , ") : body.append(atomo)
            body[-1]=body[-1].replace(".\n","")
            body[-1]=body[-1].replace(".","")
        else:
            cl[0]=cl[0].replace(".\n","")
        kb.addClausola(clausola(cl[0],body))
kb.addAssumable("ok_l1")
kb.addAssumable("ok_l2")
kb.addAssumable("ok_s1")
kb.addAssumable("ok_s2")
kb.addAssumable("ok_s3")
kb.addAssumable("ok_cb1")
kb.addAssumable("ok_cb2")
kb.addAssumable("live_outside")
print(kb.conflicts())

