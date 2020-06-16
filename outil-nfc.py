"""
--- Script de récupération des données des capteurs via le NFC Reader

version: 0.3

--- Librairies utilisée:
nfcpy : Permet de récupérer les informations des capteurs
xlsxwriter : Permet d'écrire des fichier xlsx pour Excel
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

		# rangement des données dans un dictionnaire
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
				except:
					donnees.get(info[0]).append(info[1])
			else:
				donnees.get(info[0]).append(info[1])
		print(donnees)

		clf.close()
		num_capt += 1
		autre = str(input('Un autre capteur? (o/n)'))
		

	# écriture dans le fichier Excel
	# Ouverture du fichier Excel et de la feuille
	workbook = xlsxwriter.Workbook(f'donnees_sorties\\{nom_fichier}.xlsx')
	worksheet = workbook.add_worksheet()

	# écriture en gras des titres de colonnes
	bold = workbook.add_format({'bold': True})

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
		worksheet.write(f'{chr(x+65)}1', template[x], bold)

		if 'DevEUI' in template[x]:
			deveuis = donnees.get("DevEui")
			y = 2
			for deveui in deveuis:
				worksheet.write(f'{chr(x+65)}{y}', deveui)
				y += 1
		
		elif 'AppEUI' in template[x]:
			noms = donnees.get("AppEui")
			y = 2
			for nom in noms:
				worksheet.write(f'{chr(x+65)}{y}', nom)
				y += 1

		elif 'AppKey' in template[x]:
			appkeys = donnees.get("AppKey")
			y = 2
			for appkey in appkeys:
				worksheet.write(f'{chr(x+65)}{y}', appkey)
				y += 1

	# On commence à écrire le reste des données dans le fichier Excel, en évitant les données déjà écrites
	x = 11
	alpha = True
	for field in donnees:
		# Cette partie vérifie que le code ascii des colonnes (de 65 à 90, soit de A à Z)
		# soit bien inférieur à 26 pour éviter les cellules qui n'éxistent pas
		# et on recommence une boucle en commençant avec deux lettres
		if alpha == True:
			cell = f'{chr(x+65)}'
		else:
			cell = f'A{chr(x+65)}'

		if field not in ['DevEui', 'AppEui', 'AppKey']:
			y = 2
			for data in donnees[field]:
				worksheet.write(f'{cell}{y}', data)
				y += 1
			worksheet.write(f'{cell}1', field, bold)
			x += 1
		if x > 25:
			alpha = False
			x = 0
			

	# On ferme le fichier Excel
	workbook.close()
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
