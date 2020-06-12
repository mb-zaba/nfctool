"""
--- Script de récupération des données des capteurs via le NFC Reader

--- Librairies utilisée:
pyscard : Fait la liaison avec le lecteur NFC
nfcpy : Permet de récupérer les informations des capteurs
xlwt : Permet d'écrire un fichier Excel
"""

import sys, nfc, xlwt

# tant que le programme continue, c'est qu'il y a une carte sur le lecteur lorsque l'on tape Entrée
try:
	workbook = xlwt.Workbook()
	sheet = workbook.add_sheet('Sheet_1')
	row_num = 0
	autre = 'o'
	# La boucle permet de rentrer plusieurs capteurs les uns après les autres
	while autre == 'o':
		# connexion à la carte NFC par le lecteur USB
		clf = nfc.ContactlessFrontend('usb')

		# récupération des données du capteur et mise en forme en dictionnaire
		tag = clf.connect(rdwr={'on-connect': lambda tag: False})
		assert tag.ndef is not None
		records = str(tag.ndef.records[0]).split('\'')
		data = records[3].split('\n')
		print(len(data))
		infos = {}
		for i in range(0, len(data)-1):
			info = data[i].split(':')
			infos[info[0]] = info[1]
		print(infos)
		# démarrage de l'écriture dans un fichier Excel
		# écriture des titres des colonnes
		if row_num == 0:
			row = sheet.row(row_num)
			col_num = 1
			for clé in infos:
				row.write(col_num, clé)
				col_num += 1
			row_num +=1

		# écriture des données
		row = sheet.row(row_num)
		row.write(0, f'Capteur {row_num}')
		col_num = 1
		for valeur in infos.values():
			row.write(col_num, valeur)
			col_num += 1

		row_num += 1
		clf.close()
		workbook.save("donnees_capteurs.xls")
		autre = str(input('Un autre capteur? (o/n)'))

except:
	print("\nArrêt du programme.")