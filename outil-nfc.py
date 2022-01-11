"""
--- Script de récupération des données des capteurs via le NFC Reader

version: 0.4.2

--- Librairies utilisée:
nfcpy : Permet de récupérer les informations des capteurs
xlsxwriter : Permet d'écrire des fichier xlsx pour Excel
ndef : Permet le formatage des données dans la norme NDEF
"""


import nfc
import xlsxwriter
import argparse
import ndef


# une fonction pour détecter les arguments et les utiliser dans le programme
def arg_parser():
    parser = argparse.ArgumentParser(
        description="Outil de lecture et d'écriture de capteur ERS Eye"
    )

    mode = parser.add_mutually_exclusive_group(required=True)

    # pour le mode lecture
    mode.add_argument("-l", "--lire", help="mode lecture",
                      action="store_true", dest="lecture")

    # pour le mode ecriture
    mode.add_argument("-e", "--ecrire", help="mode ecriture",
                      action="store_true", dest="ecriture")

    # définir le nom du fichier en sortie de la lecture ou en entrée de l'écriture
    parser.add_argument("-f", "--fichier",
                        help="""défini le nom du fichier en sortie(mode lecture) ou en entrée(mode écriture),
        suffixes -spot et -donnees seront ajouté en sortie.
        Pour le fichier dans le mode écriture, placez le fichier dans le dossier entrees_csv\\""",
                        metavar='nom_fichier')

    # affiche toutes les données du capteur récupérées par le programme
    parser.add_argument(
        "-v", "--verbose", help="affiche les données du capteur", action="store_true")

    return(parser.parse_args())


class outil_nfc:
    # fonction pour formatter la configuration en dictionnaire
    def conf_to_dict(self, data, donnees, num_capt):
        for i in range(0, len(data)-1):
            info = data[i].split(':')
            if info[0] not in donnees:
                donnees[info[0]] = []
                for j in range(num_capt):
                    donnees.get(info[0]).append('')

            # Toutes les données étant récupérées en chaines de caractère,
            # on transforme les nombres en 'int' pour éviter les warnings dans Excel
            # Les valeurs de AppEui, AppKey et DevEui sont en hexadécimal, on évite donc de les transformer
            if info[0] not in ['AppEui', 'AppKey', 'DevEui']:
                try:
                    donnees.get(info[0]).append(int(info[1]))
                except Exception as e:
                    print(e)
                    donnees.get(info[0]).append(info[1])
            else:
                donnees.get(info[0]).append(info[1])
        return(donnees)

    # fonction de lecture du capteur

    def lecture(self, nom_fichier, verbose):
        nouv_capt = 'o'
        num_capt = 0
        donnees = {}

        # La boucle permet de rentrer plusieurs capteurs les uns après les autres
        while nouv_capt == 'o':
            print('Placez un capteur sur le lecteur.\n')
            # connexion à la carte NFC par le lecteur USB
            clf = nfc.ContactlessFrontend('usb')

            # récupération des données du capteur
            tag = clf.connect(rdwr={'on-connect': lambda tag: False})
            print('Capteur lu')
            records = tag.ndef.records[0]
            if verbose:
                print(records)
            data = records.text.split('\n')

            donnees = outil_nfc.conf_to_dict(data, donnees, num_capt)

            clf.close()
            num_capt += 1
            nouv_capt = str(input('Un autre capteur? (o/n)'))
            while nouv_capt not in ['o', 'n']:
                nouv_capt = str(input('Un autre capteur? (o/n)'))

        # écriture dans le fichier Excel
        # Ouverture du fichier Excel et de la feuille
        fichier_spot = xlsxwriter.Workbook(
            f'donnees_sorties\\{nom_fichier}-spot.xlsx')
        fichier_data = xlsxwriter.Workbook(
            f'donnees_sorties\\{nom_fichier}-donnees.xlsx')

        spot_sheet = fichier_spot.add_worksheet()
        data_sheet = fichier_data.add_worksheet()

        # écriture en gras des titres de colonnes
        bold = fichier_spot.add_format({'bold': True})

        # titres de colonnes du template à respecter pour spot.objenious
        template = ['Action (create / update) *',
                    'Nom du capteur *',
                    'Profil de capteur (code) *',
                    'Groupe (code)',
                    'AppEUI (bigendian) * (update non pris en compte)',
                    'DevEUI (bigendian) * (Identifiant du capteur - update impossible)',
                    'AppKey * (update non pris en compte)',
                    'Equipement associé',
                    'Latitude',
                    'Longitude',
                    'Actif (oui/non)'
                    ]

        # cette partie écrit dans le fichier Excel les colonnes du template en fonction des données trouvées
        # la variable x sert d'index dans le tableau et en y ajoutant 65 a le code Ascii des lettres majuscules
        # la variable y est pour la ligne dans le tableau Excel
        x = 0
        for x in range(0, len(template)):
            spot_sheet.write(f'{chr(x+65)}1', template[x], bold)

            if 'DevEUI' in template[x]:
                try:
                    deveuis = donnees.get("DevEui")
                    y = 2
                    for deveui in deveuis:
                        spot_sheet.write(f'{chr(x+65)}{y}', deveui)
                        y += 1
                except Exception as e:
                    print("Erreur: DevEui\n", e)

            elif 'AppEUI' in template[x]:
                noms = donnees.get("AppEui")
                y = 2
                for nom in noms:
                    spot_sheet.write(f'{chr(x+65)}{y}', nom)
                    y += 1

            elif 'AppKey' in template[x]:
                appkeys = donnees.get("AppKey")
                y = 2
                for appkey in appkeys:
                    spot_sheet.write(f'{chr(x+65)}{y}', appkey)
                    y += 1

            elif 'Profil' in template[x]:
                for i in range(2, num_capt+2):
                    spot_sheet.write(f'{chr(x+65)}{i}',
                                     'elsys-ers-cde4320234203')

            elif 'Groupe' in template[x]:
                for i in range(2, num_capt+2):
                    spot_sheet.write(f'{chr(x+65)}{i}', 'test_perverie')

        # écriture du fichier de données
        x = 0
        alpha = True
        for field in donnees:
            # Cette partie vérifie que le code ascii des colonnes (de 65 à 90, soit de A à Z)
            # soit bien inférieur à 26 pour éviter les cellules qui n'éxistent pas
            # et on recommence une boucle en commençant avec deux lettres
            if alpha is True:
                cell = f'{chr(x+65)}'
            else:
                cell = f'A{chr(x+65)}'

            y = 2
            for data in donnees[field]:
                data_sheet.write(f'{cell}{y}', data)
                y += 1
            data_sheet.write(f'{cell}1', field)
            x += 1
            if x > 25:
                alpha = False
                x = 0
        # On ferme le fichier Excel
        fichier_spot.close()
        fichier_data.close()
        print(f'{num_capt} capteur(s) ajouté(s)')
        print(f"Fichier d'injection: donnees_sorties\\{nom_fichier}-spot.xlsx")
        print(
            f"Fichier de données: donnees_sorties\\{nom_fichier}-donnees.xlsx")
        print('Certains champs du fichier d\'injection sont à remplir à la main.')

    # fonction d'écriture du capteur

    def ecriture(self, filename, verbose):
        num_capt = 0
        ndef_messages = []
        deveuis = []
        donnees = {}

        # ouverture et lecture du fichier csv
        if filename.endswith(".csv"):
            file = open(f'entrees_csv\\{filename}')
        else:
            file = open(f'entrees_csv\\{filename}.csv')

        # on récupère les titres des valeurs
        titres = file.readline().split(';')
        for i in range(0, len(titres)):
            titres[i] = titres[i].replace('\n', "")

        # on récupère les données de configuration du fichier CSV
        for line in file:
            settings = ''
            line = line.split(';')
            for j in range(0, len(line)):
                line[j] = line[j].replace('\n', '')
                settings += f'{titres[j]}:{line[j]}\n'
                if titres[j] == 'DevEui':
                    deveuis.append(line[j])
            ndef_messages.append(settings)
        file.close()

        for setting in ndef_messages:
            if verbose:
                print(setting)
            record = ndef.TextRecord(setting)

            print('\nPlacez le capteur sur le lecteur\nDevEui :',
                  deveuis[num_capt])
            # connexion à la carte NFC par le lecteur USB
            clf = nfc.ContactlessFrontend('usb')

            # récupération des données du capteur
            tag = clf.connect(rdwr={'on-connect': lambda tag: False})

            data = tag.ndef.records[0].text.split('\n')

            donnees = outil_nfc.conf_to_dict(data, donnees, num_capt)

            if donnees.get('DevEui') == deveuis[num_capt]:
                # écriture de la configuration dans le capteur
                tag.ndef.records = [record]
            else:
                print('Erreur: DevEui different.')

            clf.close()
            num_capt += 1


# début du programme
if __name__ == '__main__':
    args = arg_parser()
    if args.lecture:
        outil_nfc.lecture(args.fichier, args.verbose)
    elif args.ecriture:
        outil_nfc.ecriture(args.fichier, args.verbose)
