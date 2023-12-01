import re

from pyswip import Prolog

prolog = Prolog()
prolog.consult("kb.pl")


def query_generic(query):
    result = list(prolog.query(query))
    for entry in result:
        print(entry)


def query_canzoni_di_artista():
    artist = input("Inserisci il nome dell'artista: ")
    artist=re.sub(r'\W+', '_', artist)
    query_generic(f"canzoni_di_un_artista('{artist}', X)")


def query_canzoni_danzabili_di_artista():
    artist = input("Inserisci il nome dell'artista: ")
    artist = re.sub(r'\W+', '_', artist)
    query_generic(f"titoli_danzabili_di_artista('{artist}', X)")


def query_canzoni_danzabili_con_molte_parole():
    query_generic("titoli_danzabili_con_molte_parole(X)")


def query_canzoni_danzabili_veloci():
    query_generic("titoli_danzabili_veloci(X)")


def query_canzoni_danzabili_lente():
    query_generic("titoli_danzabili_lente(X)")


def query_alta_danzabilita():
    query_generic("titoli_alta_danzabilita(X)")


def query_alto_livello_energia():
    query_generic("titoli_alta_energia(X)")


def query_molto_strumentale():
    query_generic("titoli_molto_strumentale(X)")


def query_chiave_maggiore():
    query_generic("titoli_chiave_maggiore(X)")


def query_registrazione_live():
    query_generic("titoli_registrazione_live(X)")


def query_loudness_alto():
    query_generic("titoli_loudness_alto(X)")


def query_molto_parlante():
    query_generic("titoli_molto_parlante(X)")


def query_tempo_vivace():
    query_generic("titoli_tempo_vivace(X)")


def query_valenza_positiva():
    query_generic("titoli_valenza_positiva(X)")


def query_alta_acusticità():
    query_generic("titoli_alta_acusticità(X)")


def query_bassa_danzabilita():
    query_generic("titoli_bassa_danzabilita(X)")


def query_bassa_energia():
    query_generic("titoli_bassa_energia(X)")


def query_poco_strumentale():
    query_generic("titoli_poco_strumentale(X)")


def query_chiave_minore():
    query_generic("titoli_chiave_minore(X)")


def query_registrazione_non_live():
    query_generic("titoli_registrazione_non_live(X)")


def query_loudness_basso():
    query_generic("titoli_loudness_basso(X)")


def query_molto_poco_parlante():
    query_generic("titoli_molto_poco_parlante(X)")


def query_tempo_lento():
    query_generic("titoli_tempo_lento(X)")


def query_valenza_negativa():
    query_generic("titoli_valenza_negativa(X)")


def query_bassa_acusticità():
    query_generic("titoli_bassa_acusticità(X)")


while True:
    print("\nScegli un'opzione:")
    print("1. Canzoni di un artista")
    print("2. Canzoni danzabili di un artista")
    print("3. Canzoni danzabili con molte parole")
    print("4. Canzoni danzabili veloci")
    print("5. Canzoni danzabili lente")
    print("6. Canzoni con alta danzabilità")
    print("7. Canzoni con alto livello di energia")
    print("8. Canzoni molto strumentali")
    print("9. Canzoni in chiave maggiore")
    print("10. Canzoni con alta probabilità di registrazione live")
    print("11. Canzoni con loudness elevato")
    print("12. Canzoni con elevata presenza di parole parlate")
    print("13. Canzoni con tempo vivace")
    print("14. Canzoni con valenza positiva")
    print("15. Canzoni con alta probabilità di essere acustiche")
    print("16. Canzoni con bassa danzabilità")
    print("17. Canzoni con basso livello di energia")
    print("18. Canzoni poco strumentali")
    print("19. Canzoni in chiave minore")
    print("20. Canzoni con bassa probabilità di registrazione live")
    print("21. Canzoni con loudness basso")
    print("22. Canzoni con bassa presenza di parole parlate")
    print("23. Canzoni con tempo lento")
    print("24. Canzoni con valenza negativa")
    print("25. Canzoni con bassa probabilità di essere acustiche")
    print("0. Esci")

    choice = input("Scelta: ")

    if choice == "1":
        query_canzoni_di_artista()
    elif choice == "2":
        query_canzoni_danzabili_di_artista()
    elif choice == "3":
        query_canzoni_danzabili_con_molte_parole()
    elif choice == "4":
        query_canzoni_danzabili_veloci()
    elif choice == "5":
        query_canzoni_danzabili_lente()
    elif choice == "6":
        query_alta_danzabilita()
    elif choice == "7":
        query_alto_livello_energia()
    elif choice == "8":
        query_molto_strumentale()
    elif choice == "9":
        query_chiave_maggiore()
    elif choice == "10":
        query_registrazione_live()
    elif choice == "11":
        query_loudness_alto()
    elif choice == "12":
        query_molto_parlante()
    elif choice == "13":
        query_tempo_vivace()
    elif choice == "14":
        query_valenza_positiva()
    elif choice == "15":
        query_alta_acusticità()
    elif choice == "16":
        query_bassa_danzabilita()
    elif choice == "17":
        query_bassa_energia()
    elif choice == "18":
        query_poco_strumentale()
    elif choice == "19":
        query_chiave_minore()
    elif choice == "20":
        query_registrazione_non_live()
    elif choice == "21":
        query_loudness_basso()
    elif choice == "22":
        query_molto_poco_parlante()
    elif choice == "23":
        query_tempo_lento()
    elif choice == "24":
        query_valenza_negativa()
    elif choice == "25":
        query_bassa_acusticità()
    elif choice == "0":
        break
    else:
        print("Scelta non valida. Riprova.")
