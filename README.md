# outil-nfc

Outil de lecture de capteur en NFC

## Utilisation
**Il faut changer le driver du lecteur NFC et installer libusb en suivant la documentation [NFCpy](https://nfcpy.readthedocs.io/en/latest/)**

### Mode lecture

1. Lancez le script start-env.bat
2. Lancez le programme en ligne de commande `python3 outil-nfc.py --lecture nom_fichier`
3. Placez un capteur sur le lecteur
4. Entrez `o` pour ajouter un nouveau capteur ou `n` pour finir le script

## Librairies
- [NFCpy](https://nfcpy.readthedocs.io/)
- [xlsxwrite](https://xlsxwrite.readthedocs.io/)