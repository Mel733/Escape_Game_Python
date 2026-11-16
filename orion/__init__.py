
class Oxygene:  # gère le niveau d'oxygène du joueur
    def __init__(self,niveau : int, maximum : int):
        if maximum >80:  # le maximum ne peut pas dépasser 80
            raise ValueError ("Le maximum est de 80")  # raise = on lance une erreur
        if niveau <0 :  # le niveau ne peut pas être négatif
            raise ValueError("Le niveau ne peut pas etre négatif")
        self._niveau = niveau  
        self._maximum = maximum  # _ = attribut protégé

    @property  # property = on lit sans parenthèses, sans pouvoir modifier
    def niveau(self):
       return self._niveau

    @property
    def maximum(self):
        return self._maximum


    def retirer(self, cout):  # baisse l'oxygène
        if cout <0:  # un coût ne peut pas être négatif
          raise ValueError("Les cout d'oxygene ne peuvent pas être inférieur a 0")
        self._niveau = max (0, self._niveau - cout)  # on retire le coût, jamais sous 0

    def recharger(self, quantite):  
        self._niveau = min (self._maximum, self._niveau + quantite) #ajoute de l'oxygène sans jamais dépasser 80



class Objets:  # classe mère de tous les objets
    def __init__(self, nom:str):
        self.nom = nom  # public : sert juste à identifier l'objet

    def utiliser(self, joueur, salle)-> bool:  # -> bool : renvoie True ou False
        raise NotImplementedError("Rien ne se passe")  # chaque enfant la redéfinit


class Bombonne(Objets):  # hérite de Objets
    def __init__(self):
        super().__init__("Bombonne")  # appelle le constructeur de la mère
        self._utilisee = False  # pas encore utilisée

    def utiliser(self, joueur, salle):
        if self._utilisee :  # déjà utilisée
            return False  # rien ne se passe
        
        joueur.recharger_oxygene(30)  # +30 d'oxygène
        self._utilisee = True  # une seule utilisation
        joueur.retirer_objet(self)  # elle disparaît de l'inventaire
        return True  # ça a marché

class Badge(Objets):
     def __init__(self):
        super().__init__("Badge")


     def utiliser(self, joueur, salle) -> bool:
         if not salle.nom =="Laboratoire":  # seulement dans le labo
             return False
         for passage in salle.passages:  # on regarde chaque passage du labo
            if passage.autre_salle(salle).nom == "Machines":  # celui qui mène aux machines
                 return passage.essayer_deverouiller(joueur)  # le passage vérifie l'énigme (le badge)
         return False  # aucun passage trouvé
             
  

class Cable(Objets):
    def __init__(self):
        super().__init__("Câble")

    def utiliser(self, joueur, salle) -> bool:
        if  salle.nom !="Machines":  # seulement dans les machines
            return False
        salle.installer(self)  # installe le câble dans les machines
        joueur.retirer_objet(self)  # il disparaît de l'inventaire
        return True
       

class Fusible(Objets):  # pareil que Cable
    def __init__(self):
        super().__init__("Fusible")

    def utiliser(self, joueur, salle) -> bool:
        if salle.nom !="Machines":
            return False
        salle.installer(self)
        joueur.retirer_objet(self)
        return True
        

    


class Enigme:  # classe mère des énigmes
    def __init__(self):
        self.resolue = False  # pas encore résolue

    def verifier(self, joueur, saisie=None) -> bool:  # chaque enfant la redéfinit
        raise NotImplementedError("Rien ne se passe")

class EnigmeObjet(Enigme):  # énigme : le joueur a-t-il l'objet ?
    def __init__(self, objet_requis:str):
        super().__init__()  # crée resolue (de la mère)
        self._objet_requis = objet_requis  # nom de l'objet demandé

    @property
    def objet_requis(self):
        return self._objet_requis
    
    def verifier(self, joueur, saisie=None) -> bool:
        if joueur.possede(self._objet_requis):  # le joueur a l'objet
            self.resolue = True
            return True
        return False

class EnigmeCode(Enigme):  # énigme : le code est-il bon ?
    def __init__(self, code: str):
        super().__init__()
        self._code = code  # protégé, personne ne peut le lire de l'extérieur

    
    def verifier(self, joueur, saisie=None) -> bool:
        if saisie is None:  # rien de saisi
                return False
        
        saisie_propre = saisie.strip()  # on enlève les espaces
        
        if saisie_propre.isdigit() == False:  # le code doit être en chiffres
           return False

        if saisie_propre == self._code:  # le code est bon
            self.resolue = True
            return True
        return False



class Salle:
    def __init__(self,nom : str):
        self._passages : list[Passage] =[]  # passages de la salle
        self._objets : list[Objets] = []  # objets dans la salle
        self.nom = nom

    @property 
    def objets(self):  # lecture seule de la liste
        return self._objets

    @property
    def passages(self):
        return self._passages


    def ajouter_objet(self, objet):  # ajoute un objet dans la salle
        self._objets.append(objet)

    def retirer_objet(self, objet):  # enlève un objet de la salle
       self._objets.remove(objet)

    def trouver_objet(self, nom: str):  # cherche un objet avec son nom
        nom = nom.lower().strip()  # sans majuscules ni espaces
        for objet in self._objets:
            if nom == objet.nom.lower().strip():
                return objet  # trouvé
        return None  # pas trouvé

    def decrire(self):
        noms = []  # liste des noms des objets
        for objet in self._objets:
            noms.append(objet.nom)
        liste_objet = ", ".join(noms)  # join colle les noms avec une virgule
        if not noms:  # salle vide
            return f"Bienvenue dans {self.nom}, ici il y a aucun objet"
        return f"Bienvenue dans {self.nom}, ici il y a {liste_objet}"

    def ajouter_passage(self, passage):
        self._passages.append(passage) 

    def passage_vers(self,salle):  # trouve le passage qui mène à une salle
        for passage in self._passages:
            if passage.autre_salle(self) == salle:  # la salle d'en face est la bonne
              return passage
        return None

class Machines(Salle):  # hérite de Salle
    def __init__(self,enigme:EnigmeCode):
        super().__init__("Machines")
        self._cable_installe = False  # rien d'installé au départ
        self._fusible_installe = False
        self._reacteur_actif = False
        self._enigme = enigme  # l'énigme du code

    
    @property  # lecture seule, pareil pour les 3 suivantes
    def cable_installe(self):
        return self._cable_installe

    @property
    def fusible_installe(self):
        return self._fusible_installe

    @property
    def reacteur_actif(self):
        return self._reacteur_actif

    def installer(self,objet):  # installe le câble ou le fusible
        if objet.nom =="Câble":
            self._cable_installe = True
            return True
        elif objet.nom =="Fusible":
            self._fusible_installe = True
            return True
        return False  # autre objet : refusé

    def tenter_code(self,saisie,joueur):
        if not self._cable_installe or not self._fusible_installe:  # il faut les deux
            return False
        if self._enigme.verifier(joueur, saisie):  # code bon
            self._reacteur_actif = True  # le réacteur démarre
            for passage in self._passages:
               if passage.autre_salle(self).nom == "Commande":  # passage vers la Commande
                  passage.deverouiller()  # on l'ouvre
            return True
        return False  # code faux
            
class Laboratoire(Salle):  # hérite de Salle
    def __init__(self, code: str):
        super().__init__("Laboratoire")
        self._code= code  # le code est écrit dans le journal

    def lire_journal(self):
        return self._code  # donne le code

class Joueur:
    def __init__(self, oxygene: Oxygene, salle_actuelle : Salle):
        self._oxygene = oxygene  # objet Oxygene
        self._inventaire: list[Objets] = []  # vide au départ
        self._salle_actuelle = salle_actuelle  # salle où il est

    @property
    def oxygene(self):
        return self._oxygene

    @property
    def inventaire(self):
        return self._inventaire

    @property
    def salle_actuelle(self):
        return self._salle_actuelle



    def est_vivant(self):
        return self._oxygene.niveau>0  # vivant = il reste de l'oxygène

    def retirer_oxygene(self, cout):  # il délègue à Oxygene
        self._oxygene.retirer(cout)
    
    def recharger_oxygene(self, quantite):
        self._oxygene.recharger(quantite)  
    
    def voir_inventaire(self):
       nom_objet = []  # liste des noms
       if not self._inventaire:  # inventaire vide
           return "Inventaire vide"
       for objet in self._inventaire:
             nom_objet.append(objet.nom)
       texte = ", ".join(nom_objet)
       return f"Inventaire : {texte}"

    
    def ajouter_objet(self, objet):  # même idée que dans Salle
        self._inventaire.append(objet)


    def retirer_objet(self, objet):
        self._inventaire.remove(objet)


    def trouver_objet(self, nom: str):  # pareil que dans Salle, mais dans l'inventaire
            nom = nom.lower().strip()
            for objet in self._inventaire:
                if nom == objet.nom.lower().strip():
                    return objet
            return None


    def possede(self, nom):  # le joueur a-t-il cet objet ?
      if self.trouver_objet(nom) is not None:  # trouvé = il l'a
          return True
      return False

    def changer_salle(self, nouvelle_salle:Salle):  # change juste la position
        self._salle_actuelle = nouvelle_salle

    

class Passage:  # relie deux salles, un seul objet pour les deux sens
    def __init__(self,salle_a:Salle, salle_b:Salle, verouiller: bool, enigme = None):
        self.salle_a = salle_a
        self.salle_b =salle_b
        self._verouiller = verouiller  # True = verrouillé
        self._enigme = enigme  # énigme pour l'ouvrir (ou None)
        
    @property
    def verouiller(self):
        return self._verouiller


    def essayer_deverouiller(self, joueur):
        if self._enigme is None:  # pas d'énigme : on ne peut pas l'ouvrir comme ça
            return False
        if self._enigme.verifier(joueur):  # polymorphisme : même appel pour tous les types d'énigmes
            self.deverouiller()
            return True
        return False


    def est_ouvert(self):
        return not self._verouiller  # ouvert = pas verrouillé


    def deverouiller(self):
        self._verouiller = False  # reste ouvert pour toujours

    def autre_salle(self,salle):  # donne la salle d'en face
        if salle == self.salle_a:
            return self.salle_b
        elif salle == self.salle_b:
            return self.salle_a
        else:
            return None  # la salle n'est pas dans ce passage


class GameManager:  # pilote la partie
    def __init__(self):
        self.preparer_partie()  # crée tout le monde du jeu
        self._joueur = self.joueur  # même joueur que dans preparer_partie

    def preparer_partie(self):
       code ="8259"  # code du réacteur (en texte pour garder les zéros)
       self.sas = Salle("Sas")  # salles simples : instances de Salle
       self.reserve = Salle("Réserve")
       self.labo =  Laboratoire(code)  # le labo donne le code
       self.machine = Machines(EnigmeCode(code))  # les machines testent le même code
       self.commande = Salle("Commande")

       self._salles = {"Sas":self.sas,  # dictionnaire : on retrouve une salle avec son nom
                      "Réserve":self.reserve,
                      "Laboratoire":self.labo,
                      "Machines":self.machine,
                      "Commande":self.commande}
       
       self._couts ={ "déplacer": 6,  # dictionnaire des coûts d'oxygène
                     "observer": 1,
                     "lire journal":1,
                     "ramasser":2,
                     "utiliser" : 2,
                     "tenter code": 3,
                     "évacuer" :3,
                     "attendre":5


       }
       
       self.reserve.ajouter_objet(Badge())  # on met les objets dans leur salle
       self.reserve.ajouter_objet(Cable())
       self.labo.ajouter_objet(Bombonne())
       self.labo.ajouter_objet(Fusible())

       self.joueur = Joueur(Oxygene(48, 80), self.sas)  # il démarre dans le Sas avec 48

       passage_sas_reserve = Passage(self.sas, self.reserve, verouiller=False)  # ouvert
       self.sas.ajouter_passage(passage_sas_reserve)  # ajouté aux deux salles
       self.reserve.ajouter_passage(passage_sas_reserve)

       passage_sas_labo = Passage(self.sas, self.labo,  verouiller=False)
       self.sas.ajouter_passage(passage_sas_labo)
       self.labo.ajouter_passage(passage_sas_labo)

       passage_labo_machines = Passage(self.labo, self.machine, verouiller=True, enigme=EnigmeObjet("Badge"))  # verrouillé, s'ouvre avec le badge
       self.labo.ajouter_passage(passage_labo_machines)
       self.machine.ajouter_passage(passage_labo_machines)

       passage_machine_commande=Passage(self.machine, self.commande, verouiller=True)  # verrouillé, s'ouvre avec le réacteur
       self.machine.ajouter_passage(passage_machine_commande)
       self.commande.ajouter_passage(passage_machine_commande)


       self._etat = "en cours"  # états : en cours, victoire, defaite

    @property
    def a_gagner(self):  # utilisée par main.py
       if self._etat == "victoire":
           return True
       return False


    @property
    def niveau_final_oxygene(self):  # pour le message de victoire
        return self._joueur.oxygene.niveau

    def _payer(self, cout):  # méthode interne : retire le coût, vérifie si le joueur est vivant
        self._joueur.retirer_oxygene(cout)
        if not self._joueur.est_vivant():  # plus d'oxygène
            self._etat = "defaite"
            return False
        return True


        
    def deplacer(self, autre_salle):
        destination = self._salles.get(autre_salle)  # .get renvoie None si le nom n'existe pas
        passage = self.joueur._salle_actuelle.passage_vers(destination)  # mieux : self._joueur.salle_actuelle
       
        if destination is None:  # la salle n'existe pas
            return "Cette salle n'existe pas."
        if passage is None:  # pas de passage : coût 0
            return f"Passage entre {self._joueur.salle_actuelle.nom} vers {destination.nom} n'existe pas"
        if not passage.est_ouvert():  # verrouillé : coût 0
            return f"Passage entre {self._joueur.salle_actuelle.nom} vers {destination.nom} fermé"
        if not self._payer(self._couts["déplacer"]):  # on paie 6, si mort : défaite
            return "tu est mort"
        self.joueur.changer_salle(destination)  # le joueur change de salle
        return f"Tu es maintenant dans {destination.nom}"


    def observer(self):
        self._payer(self._couts["observer"])  # coût 1
        return self._joueur.salle_actuelle.decrire()  

    def lire_journal(self):
        salle = self._joueur.salle_actuelle
        if salle.nom != "Laboratoire":  # seulement au labo : coût 0
            return "Pas possible"
        self._payer(self._couts["lire journal"])  # coût 1
        return self.labo.lire_journal()
        
        

    def ramasser(self, nom_objet):
        objet = self._joueur.salle_actuelle.trouver_objet(nom_objet)  # on cherche dans la salle
        if objet is None:  # objet absent : coût 0
            return f"Objet absent : {nom_objet}"
        if objet in self._joueur._inventaire: 
            return f"Objet déjà présent dans l'inventaire"
        if not self._payer(self._couts["ramasser"]):  # coût 2
            return"Plus d'oxygene"
        self._joueur.salle_actuelle.retirer_objet(objet)  # il sort de la salle
        self._joueur.ajouter_objet(objet) 
        return f"Tu a ramasser {objet.nom}"



    def tenter_code(self, saisie):
        salle = self._joueur.salle_actuelle
        if salle.nom != "Machines":  # seulement aux machines : coût 0
            return "Impossible, action possible seulement dans Machines"
        if not salle.cable_installe or not salle.fusible_installe:  # pièces manquantes : coût 0
            return "Objet manquant"
        if not self._payer(self._couts["tenter code"]):  # coût 3, même si le code est faux
            return "Plus d'oxygene"
        if salle.tenter_code(saisie, self._joueur):  # la salle teste le code
            return "Code correct, le réacteur démarre, la porte vers la salle de commande s'ouvre"
        return "Code faux"

    def evacuer(self):
        machine = self._salles["Machines"]  # le réacteur est dans les machines
        salle = self._joueur.salle_actuelle
        if salle.nom != "Commande":  # seulement dans la Commande : coût 0
            return "Action possible seulement dans Commandes"
        if not machine.reacteur_actif:  # réacteur éteint : coût 0
            return "Le réacteur n'est pas actif, aucun oxygene ne sera débité"
        if not self._payer(self._couts["évacuer"]):  # coût 3
            return "Vous êtes morts" 
        self._etat = "victoire"  # il a payé et il est vivant : victoire
        return "Vous êtes sortie"


    def utiliser(self, nom_objet):
        if self.est_terminee():  # partie finie
            return "Plus d'oxygene"

        objet = self._joueur.trouver_objet(nom_objet)  # on cherche dans l'inventaire
        if objet is None :  # il n'a pas l'objet : coût 0
            return "Refusé, aucun oxygene a été débité"

        salle = self._joueur.salle_actuelle
        if not self._payer(self._couts["utiliser"]):  # coût 2, payé avant de savoir si ça marche
            return "Tu a perdu, plus d'oxygene"

        resultat = objet.utiliser(self._joueur, salle)  # polymorphisme : chaque objet fait son effet
        if resultat is True:
            return f"Tu a utilisé : {objet.nom}"
        return f"Impossible d'utiliser : {objet.nom}"

        





    def attendre(self):
        self._payer(self._couts["attendre"])  # coût 5, rien d'autre
        return "Tu attend, rien ne se passe"

    # texte d'aide, avec la carte des chemins
    def aide(self):
        return "Aide : Le but de cet escape game est de s'enfuire de la base, faite attention a vos action car une fois l'oxygene a 0 c'est perdu.\nVoici une cartes des chemins:\nSas -> Réserve et Sas -> Laboratoire\nLaboratoire -> Machines : a condition d'avoir le badge\nMachine -> Commande : a condition d'avoir le cable, le fusible et le code" 
        
       

    def etat(self):  # état du joueur (gratuit)
        return f"Voici votre état : Salle: {self._joueur.salle_actuelle.nom} | Oxygène :{self._joueur.oxygene.niveau}"

    def voir_inventaire(self):  # il délègue au joueur
      return self._joueur.voir_inventaire()


    
    def est_terminee(self):  # utilisée par main.py pour arrêter la boucle
        if self._etat != "en cours":
            return True 
        # sinon il ne renvoie rien (mieux : return False)
        

    
        