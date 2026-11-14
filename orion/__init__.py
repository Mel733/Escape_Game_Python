"""Espace prévu pour organiser vos classes et modules Python."""
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
        else :
           joueur.recharger(30)
           self._utilisee = True
           return True

class Badge(Objets):
     def __init__(self):
        super().__init__("Badge")


     def utiliser(self, joueur, salle) -> bool:
         if not salle.nom !="Laboratoire":
             return False
         for passage in salle.passages:
          if passage.autre_salle(salle).nom == "Machines":
                 passage.deverrouiller()
                 return True
          return False
             
  

class Cable(Objets):
    def __init__(self):
        super().__init__("Cable")

    def utiliser(self, joueur, salle) -> bool:
        if  salle.nom !="Machines":
            return False
        #sinon installer dans les machines
        #l'objet disparait de l'inventaire apres
        #return true

class Fusible(Objets):
    def __init__(self):
        super().__init__("Fusible")

    def utiliser(self, joueur, salle) -> bool:
        if salle.nom !="Machines":
            return False
        #sinon installer dans les machines
        #l'objet disparait de l'inventaire apres
        #return true

    
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
        self._objet.append(objet)

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
        if objet.nom =="Cable":
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
                passage.deverrouiller()
             return True
        return False
            
class Laboratoire(Salle):
    def __init__(self, code: str):
        super().__init__("Laboratoire")
        self._code=code

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
        return self._oxygene>0


    def voir_inventaire(self):
       if not self._inventaire:
           return "Inventaire vide"
       return f"Inventaire : {self._inventaire}"

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
    def __init__(self,salle_a:Salle, salle_b:Salle, verouiller: bool, condition:bool):
        self.salle_a = salle_a
        self.salle_b =salle_b
        self._verouiller = verouiller
        self.condition = condition

    @property
    def verouiller(self):
        return self._verouiller

    def est_ouvert(self):
        if not self._verouiller == False:
            return True
        return False


    def deverouiller(self):
        self._verouiller = True

    def autre_salle(self,salle):
        if salle == self.salle_a:
            return self.salle_b
        elif salle == self.salle_b:
            return self.salle_a
        else:
            return None



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

        



       