"""
--- Script de récupération des données des capteurs via le NFC Reader

version: 0.2

--- Librairies utilisée:
nfcpy : Permet de récupérer les informations des capteurs
xlwt : Permet d'écrire un fichier Excel
"""

import sys, nfc, xlwt

# fonction de lecture du capteur
def lecture():
	# création de la feuille du fichier Excel
	workbook = xlwt.Workbook()
	sheet = workbook.add_sheet('Sheet_1')

	row_num = 0
	autre = 'o'
	clés = []
	try:
		# La boucle permet de rentrer plusieurs capteurs les uns après les autres
		while autre == 'o':
			# contient les données de bases attendues
			donnees = {
				'DevEui':'',
				'Ota':'',
				'Ack':'',
				'AppEui':'',
				'AppKey':'',
				'SplPer':'',
				'TempPer':'',
				'LightPer':'',
				'PirPer':'',
				'PirCfg':'',
				'PirSens':'',
				'EyePer':'',
				'SendPer':'',
				'VddPer':'',
				'PerOvr':'',
				'DrDef':'',
				'DrMax':'',
				'DrMin':'',
				'Plan':'',
				'Link':'',
				'QSize':'',
				'QOffset':'',
				'QPurge':'',
				'Port':'',
				'Plans':'',
				'Sensor':'',
				'FW':''
			}
			try:
				# connexion à la carte NFC par le lecteur USB
				clf = nfc.ContactlessFrontend('usb')

				# récupération des données du capteur et mise en forme en dictionnaire
				tag = clf.connect(rdwr={'on-connect': lambda tag: False})
				assert tag.ndef is not None
				records = str(tag.ndef.records[0]).split('\'')
				data = records[3].split('\n')
				for i in range(0, len(data)-1):
					info = data[i].split(':')
					donnees[info[0]] = info[1]
				print('Capteur lu')
				# démarrage de l'écriture dans un fichier Excel
				# écriture des titres des colonnes
				if row_num == 0:
					row = sheet.row(row_num)
					col_num = 1
					for clé in donnees:
						row.write(col_num, clé)
						clés.append(clé)
						col_num += 1
					row_num += 1

				for clé in donnees:
					if clé not in clés:
						sheet.write(0, col_num, clé)
						col_num += 1
	

				# écriture des données
				row = sheet.row(row_num)
				row.write(0, f'Capteur {row_num}')
				col_num = 1
				for valeur in donnees.values():
					row.write(col_num, valeur)
					col_num += 1
				row_num += 1

			except:
				print(f'Pas de capteur\n{sys.exc_info()[0]}')

			finally:
				clf.close()
				autre = str(input('Un autre capteur? (o/n)'))

	finally:
		nom_fichier = str(input('Nom du fichier Excel: '))
		workbook.save(f"{nom_fichier}.xls")

print('Lecteur NFC.\nTapez "l" pour lire les données du capteur ou "e" pour écrire les données dans le capteur.')
print('Le mode écriture lit les données d\'un fichier CSV')
mode = str(input('> '))
while mode not in ('l', 'e'):
	mode = str(input())
if mode == 'e':
	ecriture()
else:
	lecture()