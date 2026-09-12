import random
import tkinter as tk
from tkinter import ttk

# ====== Configuration / Déclaration des variables ======
# Dés: 4 valeurs possibles -> Fumble (crâne), Critique (étoile), 1, 2
# 5 couleurs classées par ordre croissant: R Rouge, O Orange, N Noir, V Vert, B Bleu
DES_PROBAS = {
    'R': {'values': ['\u26e4', '\u2620', 0, 1, 2], 'weights': [1, 3, 8, 2, 2]},
    'O': {'values': ['\u26e4', '\u2620', 0, 1, 2], 'weights': [1, 2, 6, 5, 2]},
    'N': {'values': ['\u26e4', '\u2620', 0, 1, 2], 'weights': [1, 1, 6, 5, 3]},
    'V': {'values': ['\u26e4', '\u2620', 0, 1, 2], 'weights': [2, 1, 4, 5, 4]},
    'B': {'values': ['\u26e4', '\u2620', 0, 1, 2], 'weights': [3, 1, 3, 4, 5]}
}

# Textes des cas critiques
CAS1 = ''
CAS2 = 'D\u00e9sarm\u00e9, -1 \u202c si dragone, Si 2* dragone casse ou -2 \u202c'
CAS3 = 'Arme bris\u00e9e'
CAS4 = 'Chute -1\U0001f3b2, & -1 \u202c pour se relever, -1\U0001f3b2 -1 \u202c sup pour 2M'
CAS5 = 'Se blesse \u26844, C 1M 1*\u0110, 2M D 2*\u0110'
CAS6 = 'Perte de doigt, -1\U0001f3b2 Permanent'
CAS6D = 'Le projectile rebondit Blessure T2 \u26844, H\u00e9moragie = \u03a3\u2620 ou \u03a3\u26e4'
CAS7 = "S'assomme = fin du combat pour vous"

EFFETS = {
    'C': {2: CAS2, 3: CAS3, 4: CAS4, 5: CAS5, 6: CAS6, 7: CAS7},
    'M': {2: CAS2, 3: CAS3, 4: CAS4, 5: CAS5, 6: CAS6, 7: CAS7},
    'D': {2: CAS2, 3: CAS3, 4: CAS4, 5: CAS5}
}

COULEURS = [
    ('R', 'Rouge', '#c0392b'),
    ('O', 'Orange', '#e67e22'),
    ('N', 'Noir', '#2c3e50'),
    ('V', 'Vert', '#27ae60'),
    ('B', 'Bleu', '#2980b9'),
]


def lancer_de(des, nombre=1):
    des = des.upper()
    valeurs = DES_PROBAS[des]['values']
    poids = DES_PROBAS[des]['weights']
    return random.choices(valeurs, weights=poids, k=nombre)


def calculer_somme_et_effet(resultats, type_arme):
    nb_etoiles = resultats.count('\u26e4')
    nb_tetes_de_mort = resultats.count('\u2620')

    if nb_etoiles > nb_tetes_de_mort:
        valeur_symboles = 4
        nb_symboles_restants = nb_etoiles - nb_tetes_de_mort
        symboles_restants = ['\u26e4'] * nb_symboles_restants
        if nb_symboles_restants == 1:
            effet = "Vous avez gagn\u00e9 4 touches !"
            partie = "Attaquant"
        else:
            effet = EFFETS[type_arme].get(nb_symboles_restants, "")
            partie = "D\u00e9fenseur"
    elif nb_tetes_de_mort > nb_etoiles:
        valeur_symboles = -2
        nb_symboles_restants = nb_tetes_de_mort - nb_etoiles
        symboles_restants = ['\u2620'] * nb_symboles_restants
        if nb_symboles_restants == 1:
            effet = "Vous avez perdu 2 touches et votre adversaire en a gagn\u00e9 1"
            partie = "Attaquant"
        else:
            effet = EFFETS[type_arme].get(nb_symboles_restants, "")
            partie = "Attaquant"
    else:
        valeur_symboles = 0
        symboles_restants = []
        nb_symboles_restants = 0
        effet = ""
        partie = ""

    somme_numerique = sum(r for r in resultats if isinstance(r, int))
    total = somme_numerique + valeur_symboles

    return total, symboles_restants, effet, partie


class HarzaDiceApp:
    def __init__(self, fenetre):
        self.fenetre = fenetre
        self.fenetre.title("HarzaDice")
        self.compteur_des = {code: 0 for code, _, _ in COULEURS}
        self.type_arme = tk.StringVar(value='M')

        self._construire_interface()

    def _construire_interface(self):
        barre_haut = ttk.Frame(self.fenetre)
        barre_haut.pack(padx=10, pady=10, fill='x')

        ttk.Label(barre_haut, text="Type d'arme :").pack(side='left')
        for code, label in (('C', 'Courte'), ('M', 'Moyenne'), ('D', 'Distante')):
            ttk.Radiobutton(
                barre_haut, text=label, value=code, variable=self.type_arme
            ).pack(side='left', padx=5)

        zone_boutons = ttk.Frame(self.fenetre)
        zone_boutons.pack(padx=10, pady=5)
        self.labels_compteur = {}
        for i, (code, label, couleur) in enumerate(COULEURS):
            cadre = ttk.Frame(zone_boutons, padding=5)
            cadre.grid(row=0, column=i, padx=5)
            bouton = tk.Button(
                cadre, text=label, bg=couleur, fg='white',
                width=10, height=2,
                command=lambda c=code: self.incrementer(c)
            )
            bouton.pack()
            lbl = ttk.Label(cadre, text='0', font=('Arial', 14, 'bold'))
            lbl.pack()
            self.labels_compteur[code] = lbl

        zone_actions = ttk.Frame(self.fenetre)
        zone_actions.pack(padx=10, pady=10)
        ttk.Button(zone_actions, text="LANCER !", command=self.lancer).pack(side='left', padx=5)
        ttk.Button(zone_actions, text="Oublie...", command=self.oublier).pack(side='left', padx=5)

        self.zone_resultat = tk.Text(self.fenetre, width=70, height=12, wrap='word')
        self.zone_resultat.pack(padx=10, pady=10)

    def incrementer(self, code):
        self.compteur_des[code] += 1
        self.labels_compteur[code].config(text=str(self.compteur_des[code]))

    def lancer(self):
        if not any(self.compteur_des.values()):
            self.zone_resultat.delete('1.0', 'end')
            self.zone_resultat.insert('end', "S\u00e9lectionnez au moins un d\u00e9.\n")
            return

        type_arme = self.type_arme.get().upper()
        if type_arme not in ('C', 'M', 'D'):
            type_arme = 'M'

        resultats = []
        for code, _, _ in COULEURS:
            n = self.compteur_des[code]
            if n > 0:
                resultats.extend(lancer_de(code, n))

        total, symboles_restants, effet, partie = calculer_somme_et_effet(resultats, type_arme)
        symboles_str = ''.join(str(s) for s in symboles_restants)

        self.zone_resultat.delete('1.0', 'end')
        if symboles_restants:
            self.zone_resultat.insert('end', f"Total = {total} & {symboles_str}     :     {resultats}\n")
        else:
            self.zone_resultat.insert('end', f"Total = {total}     :     {resultats}\n")
        if partie:
            self.zone_resultat.insert('end', f"{partie} : {effet}\n")

    def oublier(self):
        for code in self.compteur_des:
            self.compteur_des[code] = 0
            self.labels_compteur[code].config(text='0')
        self.zone_resultat.delete('1.0', 'end')


def main():
    racine = tk.Tk()
    HarzaDiceApp(racine)
    racine.mainloop()


if __name__ == '__main__':
    main()
