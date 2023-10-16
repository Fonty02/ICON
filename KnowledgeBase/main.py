from pyswip import Prolog

# Inizializza il motore Prolog
prolog = Prolog()

# Carica la base di conoscenza dal file .pl
prolog.consult("base_conoscenza.pl")



def verifica_conseguenza(proposizione):
    query = f"not {proposizione}."
    if not prolog.query(f"not {query}."):
        return "false"
    else:
        return "true"

# Esempi di verifiche
proposizione1 = "ok_l1"
proposizione2 = "down_s2"

risultato1 = verifica_conseguenza(proposizione1)
risultato2 = verifica_conseguenza(proposizione2)

print(f"La proposizione '{proposizione1}' è una conseguenza logica: {risultato1}")
print(f"La proposizione '{proposizione2}' è una conseguenza logica: {risultato2}")
