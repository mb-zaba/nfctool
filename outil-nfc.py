"""
--- Script de récupération des données des capteurs via le NFC Reader

version: 0.3

--- Librairies utilisée:
nfcpy : Permet de récupérer les informations des capteurs
"""

import sys, nfc, os, xlsxwriter

# affiche l'aide
def aide():
	print('utilisation:\tpython3 lecteur_nfc.py mode nom_fichier\n')
	print('mode:')
	print('\t--lecture nom_fichier\t\tLit les données des capteurs et sort un fichier Excel')
	print('\t--ecriture nom_fichier\t\tLit les données d\'un fichier CSV donné en argument\n\t\t\t\t\tet écrit les données dans un capteur')
	print('\t--help,-h\t\t\tAffiche cette aide')
	print('\nProgramme de lecture et d\'écriture pour capteur ERS Eye.')

# fonction de lecture du capteur
def lecture(nom_fichier):
	autre = 'o'
	num_capt = 0
	donnees = {}

	# La boucle permet de rentrer plusieurs capteurs les uns après les autres
	while autre == 'o':
		print('Placez un capteur sur le lecteur.\n')
		# connexion à la carte NFC par le lecteur USB
		clf = nfc.ContactlessFrontend('usb')

		# récupération des données du capteur
		tag = clf.connect(rdwr={'on-connect': lambda tag: False})
		print(f'Capteur lu')
		records = tag.ndef.records[0]
		data = records.text.split('\n')

		# écriture des données dans un dictionnaire
		for i in range(0, len(data)-1):
			info = data[i].split(':')
			if info[0] not in donnees:
				donnees[info[0]] = []
				for j in range(num_capt):
					donnees.get(info[0]).append('')
			try:
				donnees.get(info[0]).append(int(info[1]))
			except:
				donnees.get(info[0]).append(info[1])
		$print(donnees)

		clf.close()
		num_capt += 1
		autre = str(input('Un autre capteur? (o/n)'))
		

	# écriture dans le fichier Excel
	# Ouverture du fichier Excel
	workbook = xlsxwriter.Workbook(f'{nom_fichier}.xlsx')
	worksheet = workbook.add_worksheet()
	gras = workbook.add_format({'bold': True})
	template = ('Action (create / update) *',
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
		)
	

	print(f"Fichier sauvegardé: donnees_sorties\\{nom_fichier}.xlsx")

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
		if sys.argv[1] not in ('--ecriture', '--lecture'):
			aide()
		else:
			if sys.argv[1] == '--ecriture':
				ecriture(sys.argv[2])
			elif sys.argv[1] == '--lecture':
				lecture(sys.argv[2])
