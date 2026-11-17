"""MISSION ORION-7 - point d'entrée à compléter par l'étudiant.

Consigne : concevez votre architecture POO avant d'écrire la logique du jeu.
Vous êtes libre des classes, propriétés et méthodes, à condition de satisfaire
le cahier des charges et de justifier vos décisions dans REPONSES_POO_15_QUESTIONS.txt.
"""
from orion import GameManager

def main():
    game_manager = GameManager()
    print("MISSION ORION-7 : Vous êtes coincé au sein de l'Orion 7\nVotre but : Sortir d'ici vivant\nVous apparaissez dans le Sas")
    print()
    while not game_manager.est_terminee():
        print("Voici tes actions :\n1.Te déplacer (-6 d'oxygène)\n2.Observer la salle (-1 d'oxygène)\n3.Lire le journal (-1 d'oxygène)\n4.Ramasser un objet (-2 d'oxygène)\n5.Utiliser un objet (-2 d'oxygène)\n6.Tenter un code (-3 d'oxygène)\n7.Évacuer (-3 d'oxygène)\n8.Attendre (-5 d'oxygène)\n9.Aide\n10.État\n11.Inventaire")
        print()
        try :
            choix = int(input("Que veux-tu faire ? "))
            print()
            if choix <=0 or choix > 11:
                print("Choix inconnu")
            elif choix == 1 :
                lieux = input("Où veux-tu te déplacer ? ")
                lieux_clean = lieux.strip().capitalize()
                print(game_manager.deplacer(lieux_clean))
            elif choix == 2:
                print(game_manager.observer())
            elif choix == 3:
                print(game_manager.lire_journal())
            elif choix == 4:
                ramasse_objet =input("Quel objet veux-tu ramasser ? ")
                ramasse_objet_clean = ramasse_objet.strip().capitalize()
                print(game_manager.ramasser(ramasse_objet_clean))
            elif choix == 5:
                use_objet = input("Quel objet veux-tu utiliser ? ")
                use_objet_clean = use_objet.strip().capitalize()
                print(game_manager.utiliser(use_objet_clean))
            elif choix == 6 :
                numero = input("Quel code ? ")
                print(game_manager.tenter_code(numero))
            elif choix == 7:
                print(game_manager.evacuer())
            elif choix == 8:
                print(game_manager.attendre())
            elif choix == 9:
                print(game_manager.aide())
            elif choix== 10:
                print(game_manager.etat())
            elif choix == 11 :
                print(game_manager.voir_inventaire())
        except ValueError as erreur:
            print(erreur)

    if game_manager.a_gagner:
        print (f"Félicitations, vous avez réussi à sortir avec {game_manager.niveau_final_oxygene} % d'oxygène")
    else:
        print("Vous êtes mort, vous avez échoué")

if __name__ == "__main__":
    main()
