"""MISSION ORION-7 - point d'entrée à compléter par l'étudiant.

Consigne : concevez votre architecture POO avant d'écrire la logique du jeu.
Vous êtes libre des classes, propriétés et méthodes, à condition de satisfaire
le cahier des charges et de justifier vos décisions dans REPONSES_POO_15_QUESTIONS.txt.
"""
from orion import GameManager

def main():
    game_manager = GameManager()
    print("MISSION ORION-7 : Vous êtes coincé au sein de l'Orion 7\nVotre but : Sortir d'ici vivant ")
    while game_manager.est_terminee():
        print("Bienvenue cher joueur\nVoici tes actions :\n1.Te déplacer (6)\n2.Observer la salle(1)\n3.Lire le journal(1)\n4.Ramasser un objet(2)\n5.Utiliser un objet(2)\n6.Tenter un code(3)\n7.Evacuer(3)\n8.Attendre(5)\n9.Aide\n10.Etat\n11.Inventaire")
        try :
            choix = int(input("Que veux tu faire ? "))
            if choix <=0 or choix > 11:
                return "Choix inconnu"
            elif choix == 1 :
                game_manager.deplacer()
            elif choix == 2:
                game_manager.observer()
            elif choix == 3:
                game_manager.lire_journal()
            elif choix == 4:
                game_manager.ramasser()
            elif choix == 5:
                game_manager.utiliser()
            elif choix == 6 :
                numero = input("Quelle code ? ")
                game_manager.tenter_code(numero)
            elif choix == 7:
                game_manager.evacuer()
            elif choix == 8:
                game_manager.attendre()
            elif choix == 9:
                game_manager.aide()
            elif choix== 10:
                game_manager.etat()
            elif choix == 11 :
                game_manager.voir_inventaire()
        except ValueError:
            print("Choix invalide, veuillez rentrer un nombre")




if __name__ == "__main__":
    main()
