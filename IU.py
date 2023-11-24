#!/usr/bin/env python3
from tkinter import Menu  # Importez Menu depuis tkinter
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import Text
import json
import tkinter.simpledialog as sd
import os

index_compagnie = 0
index_modele = 0

class InterfaceUtilisateur:
    def __init__(self, fenetre):
        self.fenetre = fenetre
        self.fenetre.title("Fenêtre Principale (DLC)")
        self.fenetre.geometry('1920x1080')
        self.fenetre.config(bg="#111d41")
        self.fenetre.resizable(width=False, height=False)
        # Créer des étiquettes et des champs de saisie pour les données
        self.label_compagnie = tk.Label(fenetre, text="Compagnie:")
        self.entry_compagnie = tk.Entry(fenetre)
        self.label_modele = tk.Label(fenetre, text="Modèle:")
        self.entry_modele = tk.Entry(fenetre)
        self.label_info = tk.Label(fenetre, text="Informations:")
        self.entry_info = tk.Entry(fenetre)

#################################################################################

        #vérifie si le fichier existe
        self.fichier_produits_existe = os.path.exists("produits.json")
        self.fichier_compagnies_existe = os.path.exists("compagnies.json")

#################################################################################
         
        self.labelProduit = tk.Label(fenetre, 
                                   text="Choisir un produit", 
                                   bg="#111d41", 
                                   fg="#E9B824", 
                                   font=("Helvetica", 22))
        self.labelProduit.place(x=70, y=40)
        # Créez un style personnalisé
        style = ttk.Style()
        style.configure("MonStyle.TCombobox", 
                        fieldbackground="#2E4374", 
                        arrowsize=20, 
                        borderwidth=6, 
                        foreground="#E9B824")        
        self.liste_combo_produits = ttk.Combobox(self.fenetre, width=30, style="MonStyle.TCombobox")
        self.liste_combo_produits.place(x=70, y=70)
        self.charger_donnees_produits()        

        self.liste_combo_produits.bind("<<ComboboxSelected>>", self.selection_combo_produits)


##################################################################################


        self.labelCompagnie = tk.Label(fenetre, 
                                   text="Compagnie:", 
                                   bg="#111d41", 
                                   fg="#E9B824", 
                                   font=("Helvetica", 22))
        self.labelCompagnie.place(x=70, y=160)
        # Créez une listebox pour afficher les compagnies
        self.compagnies_listbox = tk.Listbox(fenetre, 
                                           bg="#2E4374", 
                                           font=("Helvetica", 22), 
                                           fg="#E9B824")
        self.compagnies_listbox.place(x=70,y=200,width=300,height=700)


##################################################################################


        self.labelModele = tk.Label(fenetre, 
                                   text="Modèle:", 
                                   bg="#111d41", 
                                   fg="#E9B824", 
                                   font=("Helvetica", 22))
        self.labelModele.place(x=440, y=160)
        # Crée une listbox pour afficher les modèles
        self.modeles_listbox = tk.Listbox(fenetre, 
                                           bg="#2E4374", 
                                           font=("Helvetica", 18), 
                                           fg="#E9B824")
        self.modeles_listbox.place(x=440,y=200,width=300,height=700)


####################################################################################

        # Créer des étiquettes et des champs de saisie pour les données
        self.label_compagnie = tk.Label(fenetre, text="Compagnie:",bg="#111d41",font=("Helvetica", 22),fg="#E9B824")
        self.entry_compagnie = tk.Entry(fenetre,font=("Helvetica", 18),bg="#111d41",fg="#E9B824",insertbackground="white")
        self.label_compagnie.place(x=850,y=35)
        self.entry_compagnie.place(x=850,y=70,height=30,width=300)

        self.label_modele = tk.Label(fenetre, text="Modèle:",bg="#111d41",font=("Helvetica", 22),fg="#E9B824")
        self.entry_modele = tk.Entry(fenetre,font=("Helvetica", 18),bg="#111d41",fg="#E9B824",insertbackground="white")
        self.label_modele.place(x=1250,y=35)
        self.entry_modele.place(x=1250,y=70,height=30,width=300)
       
        self.label_info = tk.Label(fenetre, text="Informations:",bg="#111d41",font=("Helvetica", 22),fg="#E9B824")
        self.label_info.place(x=850,y=157)
        
        self.informations_text = tk.Text(fenetre, height=28, width=75,bg="#2E4374",font=("Helvetica", 18),fg="#E9B824",insertbackground="white")
        self.informations_text.place(x=850,y=200)

        # Créer un bouton pour ajouter les données
        self.ajouter_button = tk.Button(fenetre, text="Ajouter", command=self.ajouter_donnees)
        self.ajouter_button.place(x=1200,y=150)

        # Créez un menu contextuel et ajoutez des éléments de menu pour copier, couper et coller
        self.context_menu = Menu(self.informations_text, tearoff=0)
        self.context_menu.add_command(label="Modifier Info", command=lambda: self.show_context_menu("fake_event"))


####################################################################################

        # Liez la fonction afficher_modeles à l'événement de sélection de la listebox
        self.compagnies_listbox.bind("<<ListboxSelect>>", self.afficher_modeles)
        self.modeles_listbox.bind("<<ListboxSelect>>", self.afficher_modeles)       
        self.modeles_listbox.bind("<Delete>", self.supprimer_modele)
        # Liez la fonction show_context_menu à l'événement du bouton droit de la souris
        self.informations_text.bind("<Button-3>", self.show_context_menu)
        self.informations_text.bind("<Control-s>", self.mettre_a_jour_informations)
        fenetre.protocol("WM_DELETE_WINDOW", self.quitter)


#-----------------------------------------------------------------------------------#


    def show_context_menu(self, event):
        if event == "fake_event":
            self.informations_text.configure(state="normal")
            return
        else:
            self.context_menu.post(event.x_root, event.y_root)

    def ajouter_donnees(self):
        produit = self.liste_combo_produits.get()
        compagnie = self.entry_compagnie.get().capitalize()
        modele = self.entry_modele.get()
        if produit == "" or produit == "Ajouter Produit" or produit == "Supprimer Produit":
            messagebox.showerror("Erreur", "Aucun Produit Selectionné!")
            self.liste_combo_produits.focus()
            return
        elif compagnie == "":
            messagebox.showerror("Erreur", "Entrer Une Compagnie!")
            self.entry_compagnie.focus()
            return
        elif modele == "":
            messagebox.showerror("Erreur", "Entrer Un Modèle!")
            self.entry_modele.focus()
            return
        info = self.informations_text.get("1.0", "end")
        confirmation = messagebox.askyesno("Ajouter une compagnie", "Voulez-vous vraiment ajouter une compagnie ?")
        if confirmation:
            # Vérifier si le fichier JSON existe
            if os.path.exists("compagnies.json"):
                # Charger les données existantes depuis le fichier
                with open("compagnies.json", "r") as json_file:
                    data = json.load(json_file)
            else:
                # Si le fichier n'existe pas, créer un dictionnaire vide
                data = {}
            # Vérifier si la compagnie existe déjà, sinon créer une liste vide
            if compagnie not in data:
                data[compagnie] = []
            # Vérifier si le modèle existe déjà pour la compagnie spécifiée
            for entry in data[compagnie]:
                if entry["Modele"] == modele:
                    messagebox.showerror("Erreur", f"Le modèle '{modele}' existe déjà pour la compagnie '{compagnie}'.")
                    return
            # Ajouter les données à la liste
            data[compagnie].append({
                "Produit" : produit,
                "Modele": modele,
                "Info": info
            })
            # Écrire les données dans le fichier JSON
            with open("compagnies.json", "w") as json_file:
                json.dump(data, json_file, indent=2)
            # Effacer les champs de saisie
            self.entry_compagnie.delete(0, tk.END)
            self.entry_modele.delete(0, tk.END)
            self.informations_text.delete("1.0", "end")
            self.fichier_compagnies_existe = os.path.exists("compagnies.json")
            self.afficher_compagnies()

    def afficher_compagnies(self):
        self.compagnies_listbox.delete(0, 'end')
        selection = self.liste_combo_produits.get()
        if self.fichier_compagnies_existe:
            with open("compagnies.json", "r") as json_file:
                compagnies_data = json.load(json_file)
                compagnies_a_afficher = set()  # Créez un ensemble pour suivre les compagnies déjà ajoutées
                for compagnie, produits in compagnies_data.items():
                    for produit in produits:
                        if produit["Produit"] == selection:
                            compagnies_a_afficher.add(compagnie)  # Ajoutez la compagnie à l'ensemble
                # Convertir l'ensemble en liste et trier alphabétiquement
                compagnies_a_afficher = sorted(list(compagnies_a_afficher))
                for compagnie in compagnies_a_afficher:
                    self.compagnies_listbox.insert(tk.END, compagnie)
        # Assurez-vous que la sélection est correctement mise à jour
        self.compagnies_listbox.selection_set(index_compagnie)
        self.compagnies_listbox.selection_anchor(index_compagnie)
        self.compagnies_listbox.update_idletasks()  # Force la mise à jour de l'interface graphique
        self.compagnies_listbox.event_generate("<<ListboxSelect>>")  # Émet un événement de sélection

    def afficher_modeles(self, event):
        global index_compagnie
        selected_indices = self.compagnies_listbox.curselection()
        if selected_indices != ():
            index_compagnie = selected_indices
        if selected_indices:
            self.entry_compagnie.delete(0, tk.END)
            self.entry_modele.delete(0, tk.END)
            self.selected_indices_compagnie = self.compagnies_listbox.curselection()
            selection = self.compagnies_listbox.get(selected_indices[0])
            self.entry_compagnie.insert(tk.END, selection)
            self.modeles_listbox.delete(0, 'end')
            # Effacez le contenu de la zone de texte lorsque vous sélectionnez une compagnie
            self.informations_text.configure(state="normal")
            self.informations_text.delete("1.0", "end")
        if not selected_indices:
            self.entry_modele.delete(0, tk.END)
            self.afficher_informations_modele(self.selected_indices_compagnie)
            return
        if self.fichier_compagnies_existe:
            produit_selection = self.liste_combo_produits.get()
            with open("compagnies.json", "r") as json_file:
                compagnies_data = json.load(json_file)
                if selection in compagnies_data:
                    produits = compagnies_data[selection]
                    for produit in produits:
                        if produit["Produit"] == produit_selection:
                            modele = produit.get("Modele")
                            if modele:
                                self.modeles_listbox.insert(tk.END, modele)
                        
    def afficher_informations_modele(self,selected_indices_compagnie):
        global index_modele
        selected_indices = self.modeles_listbox.curselection()
        if selected_indices != ():
            index_modele = selected_indices
        if not selected_indices:
            selection = self.modeles_listbox.get(index_modele[0])
            self.entry_modele.insert(tk.END, selection)
            selection = self.liste_combo_produits.get()
        selected_modele = self.modeles_listbox.get(selected_indices[0])
        self.entry_modele.insert(tk.END,selected_modele)
        selected_compagnie = self.compagnies_listbox.get(selected_indices_compagnie)
        if self.fichier_compagnies_existe:
            with open("compagnies.json", "r") as json_file:
                compagnies_data = json.load(json_file)
                if selected_compagnie in compagnies_data:
                    produits = compagnies_data[selected_compagnie]
                    for produit in produits:
                        modele = produit.get("Modele")
                        if modele and modele == selected_modele:
                            self.informations_text.configure(state="normal")
                            self.informations_text.delete("1.0", "end")
                            info = produit.get("Info", "Aucune information disponible")
                            self.informations_text.insert("1.0", info)
                            self.informations_text.configure(state="disabled")
                            break  # Arrêtez la recherche une fois que vous avez trouvé le modèle

    def supprimer_modele(self, event):
        # Vérifiez si un modèle est sélectionné
        index_modele = self.modeles_listbox.curselection()
        if not index_modele:
            return
        # Demandez à l'utilisateur de confirmer la suppression
        confirmation = messagebox.askyesno("Supprimer le modèle", "Voulez-vous vraiment supprimer ce modèle ?")
        if confirmation:
            # Supprimez le modèle de la ListBox
            selected_item = self.modeles_listbox.get(index_modele)
            self.entry_compagnie.delete(0, tk.END)
            self.entry_modele.delete(0, tk.END)
            self.modeles_listbox.delete(index_modele)
            self.compagnies_listbox.delete(0,tk.END)
            self.informations_text.configure(state="normal")
            self.informations_text.delete("1.0", "end")
            # Mettez à jour le fichier "compagnies.json" pour refléter la suppression
            self.mettre_a_jour_compagnies_json(selected_item)
            self.afficher_compagnies()

    def mettre_a_jour_informations(self, event):
        # Obtenez le texte actuel de informations_text
        info = self.informations_text.get("1.0", "end")
        # Obtenez la compagnie et le modèle sélectionnés
        selected_modele_index = self.modeles_listbox.curselection()
        selected_compagnie = self.compagnies_listbox.get(self.selected_indices_compagnie[0])
        selected_modele = self.modeles_listbox.get(selected_modele_index[0])
        # Mettez à jour les données dans "compagnies.json"
        with open("compagnies.json", "r") as json_file:
            compagnies_data = json.load(json_file)
            if selected_compagnie in compagnies_data:
                produits = compagnies_data[selected_compagnie]
                for produit in produits:
                    if produit.get("Modele") == selected_modele:
                        produit["Info"] = info
                        break
        # Écrivez les données mises à jour dans le fichier JSON
        with open("compagnies.json", "w") as json_file:
            json.dump(compagnies_data, json_file, indent=2)
        messagebox.showinfo("Sauvegarde", "Les informations ont été sauvegardées avec succès.")
        self.informations_text.configure(state="disabled")

    def mettre_a_jour_compagnies_json(self, modele_a_supprimer):
        with open("compagnies.json", "r") as json_file:
            compagnies_data = json.load(json_file)
        # Parcourez la structure de données pour trouver et supprimer le modèle
        for compagnie, modeles in compagnies_data.items():
            for modele in modeles:
                if isinstance(modele, dict) and "Modele" in modele and modele["Modele"] == modele_a_supprimer:
                    modeles.remove(modele)
        # Réécrivez le fichier JSON avec les modifications
        with open("compagnies.json", "w") as json_file:
            json.dump(compagnies_data, json_file, indent=4)

    def charger_donnees_produits(self):
        try:
            with open("produits.json", "r") as json_file:
                data = json.load(json_file)
                listeproduits = data.get("produit", [])
                combobox_produits = ["", "Ajouter Produit", "Supprimer Produit"] + listeproduits
                self.liste_combo_produits["values"] = combobox_produits
        except FileNotFoundError:
            self.liste_combo_produits["values"] = ["Ajouter Produit", "Supprimer Produit"]

    def selection_combo_produits(self, event):
        self.entry_modele.delete(0, tk.END)
        self.entry_compagnie.delete(0, tk.END)
        selection = self.liste_combo_produits.get()
        if selection in ["","Ajouter Produit", "Supprimer Produit"]:
            self.ajouter_supprimer_produit(selection)
        else:
            self.informations_text.configure(state="normal")
            self.informations_text.delete("1.0","end")
            self.modeles_listbox.delete(0,"end")
            self.afficher_compagnies()

    def ajouter_supprimer_produit(self, operation):
        self.informations_text.configure(state="normal")
        self.informations_text.delete("1.0","end")
        self.compagnies_listbox.delete(0,"end")
        self.modeles_listbox.delete(0,"end")
        if operation == "Ajouter Produit":# Code pour ajoutet un produit
            nouveau_produit = sd.askstring("Nouveau Produit", "Entrez le nom du nouveau produit:").capitalize()
            if nouveau_produit:
                listeproduits = self.lire_produits()
                listeproduits.append(nouveau_produit)
                self.ecrire_produits(listeproduits)
                self.liste_combo_produits.set(nouveau_produit)  # Sélection par défaut
                self.charger_donnees_produits()
                self.entry_compagnie.focus()
        elif operation == "Supprimer Produit": # Code pour supprimer un produit
            supprimer_produit = sd.askstring("Supprimer Produit", "Entrez le nom du produit à supprimer:").capitalize()
            listeproduits = self.lire_produits()
            if supprimer_produit in listeproduits:
                confirmation = messagebox.askyesno("Supprimer le produit", "Voulez-vous vraiment supprimer le produit ?")
                if confirmation:
                    listeproduits.remove(supprimer_produit)
                    self.ecrire_produits(listeproduits)
                    self.charger_donnees_produits()

    def lire_produits(self):
        if self.fichier_produits_existe:
            with open("produits.json", "r") as json_file:
                data = json.load(json_file)
                return data.get("produit", [])
        else:
            return []

    def ecrire_produits(self, produits):
        data = {"produit": produits}
        with open("produits.json", "w") as json_file:
            json.dump(data, json_file)
        self.fichier_produits_existe = True  # Marquer le fichier comme existant après la première écriture

    def quitter(self):
        if messagebox.askyesno("Confirmation", "Êtes-vous sûr de\n vouloir quitter ?"):
            self.fenetre.destroy()

if __name__ == "__main__":
    fenetre_principale = tk.Tk()
    app = InterfaceUtilisateur(fenetre_principale)
    fenetre_principale.mainloop()