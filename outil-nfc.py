"""
--- Script de récupération des données des capteurs via le NFC Reader

version: 0.3

--- Librairies utilisée:
nfcpy : Permet de récupérer les informations des capteurs
"""

import sys, nfc, os

# affiche l'aide
def aide():
	print('utilisation:\tpython3 lecteur_nfc.py mode nom_fichier\n')
	print('mode:')
	print('\t--lecture nom_fichier\t\tLit les données des capteurs et sort un fichier xls')
	print('\t--ecriture nom_fichier\t\tLit les données d\'un fichier CSV donné en argument\n\t\t\t\t\tet écrit les données dans un capteur')
	print('\t--help,-h\t\t\tAffiche cette aide')
	print('\nProgramme de lecture et d\'écriture pour capteur ERS Eye.')

# fonction de lecture du capteur
def lecture(nom_fichier):
	# Ouverture du fichier CSV
	if nom_fichier.endswith('.csv'):
		fichier_csv = open(f'donnees_sorties\\{nom_fichier}', 'a')
	else:
		fichier_csv = open(f'donnees_sorties\\{nom_fichier}.csv', 'a')
	num_capteur = 0
	autre = 'o'
	clés = []
	try:
		# La boucle permet de rentrer plusieurs capteurs les uns après les autres
		while autre == 'o':
			# contient les données attendues
			donnees = {'DevEui':'', 'Ota':'', 'Ack':'', 'AppEui':'', 'AppKey':'', 'SplPer':'', 'TempPer':'',
				'LightPer':'', 'PirPer':'', 'PirCfg':'', 'PirSens':'', 'EyePer':'', 'SendPer':'', 'VddPer':'',
				'PerOvr':'', 'DrDef':'', 'DrMax':'', 'DrMin':'', 'Plan':'', 'Link':'', 'QSize':'', 'QOffset':'',
				'QPurge':'', 'Port':'', 'Plans':'', 'Sensor':'', 'FW':''
			}
			try:
				# connexion à la carte NFC par le lecteur USB
				clf = nfc.ContactlessFrontend('usb')

				# récupération des données du capteur et mise en forme en dictionnaire
				tag = clf.connect(rdwr={'on-connect': lambda tag: False})
				assert tag.ndef is not None
				records = tag.ndef.records[0]
				data = records.text.split('\n')
				for i in range(0, len(data)-1):
					info = data[i].split(':')
					donnees[info[0]] = info[1]
				print('Capteur lu')


				# démarrage de l'écriture dans les fichiers excel et csv
				# écriture des titres des colonnes
				if num_capteur == 0:
					for clé in donnees:
						clés.append(clé)
					fichier_csv.write(f"{';'.join(donnees)}\n")

				for clé in donnees:
					if clé not in clés:
						fichier_csv.write(f"{';'.join()}")

				# écriture des données
				num_capteur += 1
				fichier_csv.write(f"{';'.join(donnees.values())}\n")

			except Exception as e:
				print(f'Pas de capteur\n{e}')

			finally:
				clf.close()
				autre = str(input('Un autre capteur? (o/n)'))

	finally:
		print(f"Fichier sauvegardé: donnees_sorties\\{nom_fichier}.csv")
		fichier_csv.close()

# fonction d'écriture du capteur
def ecriture(filename):
	num_line = 1
	try:
		# ouverture du fichier
		file = open(filename, 'r')
		for line in file:
			if num_line == 1:
				keys = line.split(';')
				print(keys)
			num_line += 1
	except:
		print('Erreur lors de l\'ouverture du fichier')

# début du programme
if __name__ == '__main__':
	if len(sys.argv) < 3:
		aide()
	else:
		try:
			if sys.argv[1] not in ('--ecriture', '--lecture'):
				aide()
			else:
				if sys.argv[1] == '--ecriture':
					ecriture(sys.argv[2])
				elif sys.argv[1] == '--lecture':
					lecture(sys.argv[2])
		except:
			aide()