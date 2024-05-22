'''
Programme Gestion de données géographiques
@auteur   Artur Rusu
@matricule    e2270085
@date     18-05-2024
'''


import csv
import json
import math
import os

class DonneesGeo:
    def __init__(self, ville, pays, latitude, longitude):
        self.ville = ville
        self.pays = pays
        self.latitude = float(latitude)
        self.longitude = float(longitude)

    def __str__(self):
        return f"{self.ville}, {self.pays}, {self.latitude}, {self.longitude}"

def lireDonneesCsv(nomFichier):
    listeDonnees = []
    with open(nomFichier, mode='r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        print(f"En-têtes du fichier CSV : {reader.fieldnames}") 
        fieldnames = [fieldname.strip() for fieldname in reader.fieldnames]  
        print(f"En-têtes corrigés : {fieldnames}")  
        for row in reader:
            try:
                donnee = DonneesGeo(row['Ville'], row['Pays'], row['Latitude'], row['Longitude'])
                listeDonnees.append(donnee)
            except KeyError as e:
                print(f"Erreur de clé : {e}. Erreur dans les entêtes du Fichier CSV.")
    return listeDonnees


def ecrireDonneesJson(nomFichier, listeObjDonneesGeo):
    listeDict = [obj.__dict__ for obj in listeObjDonneesGeo]
    with open(nomFichier, mode='w', encoding='utf-8') as jsonfile:
        json.dump(listeDict, jsonfile, indent=4)

def trouverDistanceMin(nomFichier):
    def haversine(lat1, lon1, lat2, lon2):
        R = 6371  # Rayon Terre en kilomètres
        phi1, phi2 = math.radians(lat1), math.radians(lat2)
        delta_phi = math.radians(lat2 - lat1)
        delta_lambda = math.radians(lon2 - lon1)
        a = math.sin(delta_phi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2) ** 2
        return R * (2 * math.atan2(math.sqrt(a), math.sqrt(1 - a)))

    with open(nomFichier, mode='r', encoding='utf-8') as jsonfile:
        donnees = json.load(jsonfile)

    print("Données JSON chargées :")
    print(donnees)

    min_distance = float('inf')
    ville1 = ville2 = None

    for i in range(len(donnees)):
        for j in range(i + 1, len(donnees)):
            d1, d2 = donnees[i], donnees[j]
            distance = haversine(d1['latitude'], d1['longitude'], d2['latitude'], d2['longitude'])
            print(f"Calcul de la distance entre {d1['ville']} {d1['pays']} et {d2['ville']} {d2['pays']} : {distance:.2f} km")
            if distance < min_distance:
                min_distance = distance
                ville1, ville2 = d1, d2

    print(f"Distance minimale en kilomètres entre 2 villes : "
          f"Ville 1 : {ville1['ville']} {ville1['pays']} {ville1['latitude']} {ville1['longitude']} "
          f"et Ville 2 : {ville2['ville']} {ville2['pays']} {ville2['latitude']} {ville2['longitude']} "
          f"Distance en kilomètres : {min_distance:.2f}")

    return ville1, ville2, min_distance


def ecrireDistancesCSV(filename, ville1, ville2, min_distance):
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Ville1', 'Pays1', 'Ville2', 'Pays2', 'Distance'])
        writer.writerow([ville1['ville'], ville1['pays'], ville2['ville'], ville2['pays'], f"{min_distance:.2f}"])
    print("Les calculs de distances ont été sauvegardés dans distances.csv.")

def afficherMenu():
    print("1- Lire les données du fichier csv, créer les objets et afficher les données.")
    print("2- Sauvegarder les données dans un fichier .json.")
    print("3- Lire les données du fichier .json, déterminer et afficher les données associées à la distance minimale entre deux villes et sauvegarder les calculs dans distances.csv.")
    print("Entrez un numéro pour choisir une option ou appuyez sur 'q' pour quitter :")
    
def main():
    current_directory = os.path.dirname(os.path.abspath(__file__))
    csv_file = os.path.join(current_directory, 'Donnees.csv')
    json_file = os.path.join(current_directory, 'donnees.json')
    csv_file2 = os.path.join(current_directory, 'distances.csv')

    donneesGeo = []

    while True:
        afficherMenu()
        choix = input()

        if choix == '1':
            donneesGeo = lireDonneesCsv(csv_file)
            print("Ville, Pays, Latitude, Longitude")
            for donnee in donneesGeo:
                print(donnee)
            input("Appuyez sur une touche pour continuer...")

        elif choix == '2':
            if not donneesGeo:
                print("Veuillez d'abord lire les données du fichier csv.")
            else:
                ecrireDonneesJson(json_file, donneesGeo)
                print("Les données ont été sauvegardées dans donnees.json.")
                input("Appuyez sur une touche pour continuer...")

        elif choix == '3':
            if not donneesGeo:
              print("Veuillez d'abord sauvegarder les données dans un fichier json.")
            else:
              ville1, ville2, min_distance = trouverDistanceMin(json_file)
              ecrireDistancesCSV(csv_file2, ville1, ville2, min_distance)
            break 

        elif choix == 'q':
            break

        else:
            print("Option non valide, réessayez.")

if __name__ == "__main__":
    main()
