
class Oxygene:
    def __init__(self,niveau : int, maximum : int):
        if maximum >80:
            raise ValueError ("Le maximum est de 80")
        if niveau <0 :
            raise ValueError("Le niveau ne peut pas etre négatif")
        self._niveau = 48
        self._maximum = maximum

    @property
    def niveau(self):
       return self._niveau

    @property
    def maximum(self):
        return self._maximum


    def retirer(self, cout):
        if cout <0:
          raise ValueError("Les cout d'oxygene ne peuvent pas être inférieur a 0")
        self._niveau = max (0, self._niveau - cout)

    def rechager(self, quantite):
        self.quantite = 30
        if self.quantite + self._niveau >80:
            raise ValueError ("La quantité max d'oxygene est de 80")
        self._niveau = max (80, self._niveau + quantite)



class Objets:
    def __init__(self, nom:str):
        self.nom = nom

    def utiliser(self, joueur, salle)-> bool:
        raise NotImplementedError("Rien ne se passe")


class Bombonne(Objets):
    def __init__(self):
        super().__init__("Bombonne")
        self._utilisee = False

    def utiliser(self, joueur, salle):
        if self._utilisee :
            return False
        
        joueur.recharger_oxygene(30)
        self._utilisee = True
        joueur.retirer_objet(self)
        return True

class Badge(Objets):
     def __init__(self):
        super().__init__("Badge")


     def utiliser(self, joueur, salle) -> bool:
         if not salle.nom =="Laboratoire":
             return False
         for passage in salle.passages:
            if passage.autre_salle(salle).nom == "Machines":
                 return passage.essayer_deverouiller(joueur)
         return False
             
  

class Cable(Objets):
    def __init__(self):
        super().__init__("Câble")

    def utiliser(self, joueur, salle) -> bool:
        if  salle.nom !="Machines":
            return False
        salle.installer(self)
        joueur.retirer_objet(self)
        return True
       

class Fusible(Objets):
    def __init__(self):
        super().__init__("Fusible")

    def utiliser(self, joueur, salle) -> bool:
        if salle.nom !="Machines":
            return False
        salle.installer(self)
        joueur.retirer_objet(self)
        return True
        

    


class Enigme:
    def __init__(self):
        self.resolue = False

    def verifier(self, joueur, saisie=None) -> bool:
        raise NotImplementedError("Rien ne se passe")

class EnigmeObjet(Enigme):
    def __init__(self, objet_requis:str):
        super().__init__()
        self._objet_requis = objet_requis

    @property
    def objet_requis(self):
        return self._objet_requis
    
    def verifier(self, joueur, saisie=None) -> bool:
        if joueur.possede(self._objet_requis):
            self.resolue = True
            return True
        return False

class EnigmeCode(Enigme):
    def __init__(self, code: str):
        super().__init__()
        self._code = code

    
    def verifier(self, joueur, saisie=None) -> bool:
        if saisie is None:
                return False
        
        saisie_propre = saisie.strip()
        
        if saisie_propre.isdigit() == False:
           return False

        if saisie_propre == self._code:
            self.resolue = True
            return True
        return False



class Salle:
    def __init__(self,nom : str):
        self._passages : list[Passage] =[]
        self._objets : list[Objets] = []
        self.nom = nom

    @property 
    def objets(self):
        return self._objets

    @property
    def passages(self):
        return self._passages


    def ajouter_objet(self, objet):
        self._objets.append(objet)

    def retirer_objet(self, objet):
       self._objets.remove(objet)

    def trouver_objet(self, nom: str):
        nom = nom.lower().strip()
        for objet in self._objets:
            if nom == objet.nom.lower().strip():
                return objet
        return None

    def decrire(self):
        noms = []
        for objet in self._objets:
            noms.append(objet.nom)
        liste_objet = ", ".join(noms)
        if not noms:
            return f"Bienvenue dans {self.nom}, ici il y a aucun objet"
        return f"Bienvenue dans {self.nom}, ici il y a {liste_objet}"

    def ajouter_passage(self, passage):
        self.passages.append(passage)

    def passage_vers(self,salle):
        for passage in self._passages:
            if passage.autre_salle(self) == salle:
              return passage
        return None

class Machines(Salle):
    def __init__(self,enigme:EnigmeCode):
        super().__init__("Machines")
        self._cable_installe = False
        self._fusible_installe = False
        self._reacteur_actif = False
        self._enigme = enigme

    
    @property
    def cable_installe(self):
        return self._cable_installe

    @property
    def fusible_installe(self):
        return self._fusible_installe

    @property
    def reacteur_actif(self):
        return self._reacteur_actif

    def installer(self,objet):
        if objet.nom =="Câble":
            self._cable_installe = True
            return True
        elif objet.nom =="Fusible":
            self._fusible_installe = True
            return True
        return False

    def tenter_code(self,saisie,joueur):
        if not self._cable_installe or not self._fusible_installe:
            return False
        if self._enigme.verifier(joueur, saisie):
            self._reacteur_actif = True
            for passage in self._passages:
               if passage.autre_salle(self).nom == "Commande":
                  passage.deverouiller()
            return True
        return False
            
class Laboratoire(Salle):
    def __init__(self, code: str):
        super().__init__("Laboratoire")
        self._code= code

    def lire_journal(self):
        return self._code

class Joueur:
    def __init__(self, oxygene: Oxygene, salle_actuelle : Salle):
        self._oxygene = oxygene
        self._inventaire: list[Objets] = []
        self._salle_actuelle = salle_actuelle

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
        return self._oxygene.niveau>0

    def retirer_oxygene(self, cout):
        self._oxygene.retirer(cout)
    
    def recharger_oxygene(self, quantite):
        self._oxygene.rechager(quantite)
    
    def voir_inventaire(self):
       nom_objet = []
       if not self._inventaire:
           return "Inventaire vide"
       for objet in self._inventaire:
             nom_objet.append(objet.nom)
       texte = ", ".join(nom_objet)
       return f"Inventaire : {texte}"

    
    def ajouter_objet(self, objet):
        self._inventaire.append(objet)


    def retirer_objet(self, objet):
        self._inventaire.remove(objet)


    def trouver_objet(self, nom: str):
            nom = nom.lower().strip()
            for objet in self._inventaire:
                if nom == objet.nom.lower().strip():
                    return objet
            return None


    def possede(self, nom):
      if self.trouver_objet(nom) is not None:
          return True
      return False

    def changer_salle(self, nouvelle_salle:Salle):
        self._salle_actuelle = nouvelle_salle

    

class Passage:
    def __init__(self,salle_a:Salle, salle_b:Salle, verouiller: bool, enigme = None):
        self.salle_a = salle_a
        self.salle_b =salle_b
        self._verouiller = verouiller
        self._enigme = enigme
        
    @property
    def verouiller(self):
        return self._verouiller


    def essayer_deverouiller(self, joueur):
        if self._enigme is None:
            return False
        if self._enigme.verifier(joueur):
            self.deverouiller()
            return True
        return False


    def est_ouvert(self):
        return not self._verouiller


    def deverouiller(self):
        self._verouiller = False

    def autre_salle(self,salle):
        if salle == self.salle_a:
            return self.salle_b
        elif salle == self.salle_b:
            return self.salle_a
        else:
            return None


class GameManager:
    def __init__(self):
        self.preparer_partie()
        self._joueur = self.joueur

    def preparer_partie(self):
       code ="8259"
       self.sas = Salle("Sas")
       self.reserve = Salle("Réserve")
       self.labo =  Laboratoire(code)
       self.machine = Machines(EnigmeCode(code))
       self.commande = Salle("Commande")

       self._salles = {"Sas":self.sas, 
                      "Réserve":self.reserve,
                      "Laboratoire":self.labo,
                      "Machines":self.machine,
                      "Commande":self.commande}
       
       self._couts ={ "déplacer": 6,
                     "observer": 1,
                     "lire journal":1,
                     "ramasser":2,
                     "utiliser" : 2,
                     "tenter code": 3,
                     "évacuer" :3,
                     "attendre":5


       }
       
       self.reserve.ajouter_objet(Badge())
       self.reserve.ajouter_objet(Cable())
       self.labo.ajouter_objet(Bombonne())
       self.labo.ajouter_objet(Fusible())

       self.joueur = Joueur(Oxygene(48, 80), self.sas)

       passage_sas_reserve = Passage(self.sas, self.reserve, verouiller=False)
       self.sas.ajouter_passage(passage_sas_reserve)
       self.reserve.ajouter_passage(passage_sas_reserve)

       passage_sas_labo = Passage(self.sas, self.labo,  verouiller=False)
       self.sas.ajouter_passage(passage_sas_labo)
       self.labo.ajouter_passage(passage_sas_labo)

       passage_labo_machines = Passage(self.labo, self.machine, verouiller=True, enigme=EnigmeObjet("Badge"))
       self.labo.ajouter_passage(passage_labo_machines)
       self.machine.ajouter_passage(passage_labo_machines)

       passage_machine_commande=Passage(self.machine, self.commande, verouiller=True)
       self.machine.ajouter_passage(passage_machine_commande)
       self.commande.ajouter_passage(passage_machine_commande)

       self._joueur = Joueur(Oxygene(48, 80), Salle(self.sas))

       self._etat = "en cours"

    @property
    def etat(self):
      return self._etat

    @property
    def a_gagner(self):
       if self._etat == "victoire":
           return True
       return False


    @property
    def niveau_final_oxygene(self):
        return self._joueur.oxygene.niveau

    def _payer(self, cout):
        self._joueur.retirer_oxygene(cout)
        if not self._joueur.est_vivant():
            self._etat = "defaite"
            return False
        return True


        
    def deplacer(self, autre_salle):
        destination = self._salles.get(autre_salle)
        passage = self.joueur._salle_actuelle.passage_vers(destination)
       
        if destination is None:
            return "Cette salle n'existe pas."
        if passage is None:
            return f"Passage entre {self._joueur.salle_actuelle.nom} vers {destination.nom} n'existe pas"
        if not passage.est_ouvert():
            return f"Passage entre {self._joueur.salle_actuelle.nom} vers {destination.nom} fermé"
        if not self._payer(self._couts["déplacer"]):
            return "tu est mort"
        self.joueur.changer_salle(destination)
        return f"Tu es maintenant dans {destination.nom}"


    def observer(self):
        self._payer(self._couts["observer"])
        return self._joueur._salle_actuelle.decrire()

    def lire_journal(self):
        salle = self._joueur.salle_actuelle
        if salle.nom != "Laboratoire":
            return "Pas possible"
        self._payer(self._couts["lire journal"])
        return self.labo.lire_journal()
        
        

    def ramasser(self, nom_objet):
        objet = self._joueur.salle_actuelle.trouver_objet(nom_objet)
        if objet is None:
            return f"Objet absent : {nom_objet}"
        if objet in self._joueur._inventaire:
            return f"Objet déjà présent dans l'inventaire"
        if not self._payer(self._couts["ramasser"]):
            return"Plus d'oxygene"
        self._joueur.salle_actuelle.retirer_objet(objet)
        self._joueur._inventaire.append(objet)
        return f"Tu a ramasser {objet.nom}"



    def tenter_code(self, saisie):
        salle = self._joueur.salle_actuelle
        if salle.nom != "Machines":
            return "Impossible, action possible seulement dans Machines"
        if not salle.cable_installe or not salle.fusible_installe:
            return "Objet manquant"
        if not self._payer(self._couts["tenter code"]):
            return "Plus d'oxygene"
        if salle.tenter_code(saisie, self._joueur):
            self._payer(self._couts["tenter code"])
            return "Code correct, le réacteur démarre, la porte vers la salle de commande s'ouvre"
        return "Code faux"

    def evacuer(self):
        machine = self._salles["Machines"]
        salle = self._joueur.salle_actuelle
        if salle.nom != "Commande":
            return "Action possible seulement dans Commandes"
        if not machine.reacteur_actif:
            return "Le réacteur n'est pas actif, aucun oxygene ne sera débité"
        if not self._payer(self._couts["évacuer"]):
            return "Vous êtes morts" 
        self._etat = "victoire"
        return "Vous êtes sortie"


    def utiliser(self, nom_objet):
        if self.est_terminee():
            return "Plus d'oxygene"

        objet = self._joueur.trouver_objet(nom_objet)
        if objet is None :
            return "Refusé, aucun oxygene a été débité"

        salle = self._joueur.salle_actuelle
        if not self._payer(self._couts["utiliser"]):
            return "Tu a perdu, plus d'oxygene"

        resultat = objet.utiliser(self._joueur, salle)
        if resultat is True:
            return f"Tu a utilisé : {objet.nom}"
        return f"Impossible d'utiliser : {objet.nom}"

        





    def attendre(self):
        self._payer(self._couts["attendre"])
        return "Tu attend, rien ne se passe"

    def aide(self):
        return "Aide : Le but de cet escape game est de s'enfuire de la base, faite attention a vos action car une fois l'oxygene a 0 c'est perdu.\nVoici une cartes des chemins:\nSas -> Réserve et Sas -> Laboratoire\nLaboratoire -> Machines : a condition d'avoir le badge\nMachine -> Commande : a condition d'avoir le cable, le fusible et le code" \
        
       

    def etat(self):
        return f"Voici votre état : Salle: {self._joueur.salle_actuelle.nom} | Oxygène :{self._joueur.oxygene.niveau}"

    def voir_inventaire(self):
      return self._joueur.voir_inventaire()


    
    def est_terminee(self):
        if self._etat != "en cours":
            return True 

        

    
        