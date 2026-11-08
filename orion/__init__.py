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
         if not salle.nom =="Laboratoire":
             return False
          # 2. sinon : retrouver le passage vers les machines
        #    et le déverrouiller
        # 3. return True (le badge reste dans l'inventaire)

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
        self._passage = list[Passages] = []
        self._objet = list[Objets] = []

    def trouver_objet(self, nom):
        













# class Joueur:
#     def __init__(self, oxygene: Oxygene, salle_actuelle : Salle):
#         self._oxygene = oxygene
#         self._inventaire: list[Objet] = []
#         self._salle_actuelle = salle_actuelle