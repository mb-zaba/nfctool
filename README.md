# outil-nfc

Outil de lecture de capteur en NFC

## Utilisation
**Il faut changer le driver du lecteur NFC et installer libusb en suivant la documentation [NFCpy](https://nfcpy.readthedocs.io/en/latest/)**

1. Lancez le script start-env.bat
2. Lancez le programme en ligne de commande `python3 outil-nfc.py [ -l | -e ] [ -c | -u ] -f nom_fichier`
- Les options `-l` et `-e` (ou `--lecture` et `ecriture`) sont les modes de lecture et d'écriture, respectivement.
- Les options `-c` et `-u` (ou `--create` et `--update`) définissent l'action effectuée lors de l'injection dans spot objenious.

### Mode lecture

Le mode lecture lit les données du capteur posé sur le lecteur NFC et crée 2 fichiers.
Un fichier avec le suffixe -spot qui est le fichier à intégrer dans spot objenious et un fichier avec le suffixe -donnees qui contient les valeurs de configuration du capteur

- Placez un capteur sur le lecteur, les données récupérées seront affichées si l'argument `-v` est présent.
- Entrez `o` pour ajouter un nouveau capteur ou `n` pour finir le script


### Mode écriture

Le mode écriture lit les données de configuration de capteur dans un fichier CSV, et les écrit dans les tags du capteur.

- Placez un capteur sur le lecteur, les données écrites dans le capteur seront affichées si l'argument `-v` est présent.

Voici la liste des champs qu'il est possible d'écrire dans le capteur : https://www.elsys.se/en/elsys-nfc-settings-specification/

## Librairies
- [NFCpy](https://nfcpy.readthedocs.io/)
- [xlsxwrite](https://xlsxwrite.readthedocs.io/)
- [xlsxwriter](https://xlsxwriter.readthedocs.io/)


## Erreurs possibles
Il est possible que des erreurs apparaissent.
Voici comment résoudre certaines erreurs :

### LIBUSB_ERROR_NOT_SUPPORTED
Cette erreur apparaît lorsque le driver du lecteur NFC est mal configuré.
Il faut alors utiliser le logiciel [Zadig](https://zadig.akeo.ie).
1. Lancez l'exécutable et cliquez sur Options -> List all devices
2. Ensuite, dans la liste, selectionnez ACS122U PICC Interface.
3. Selectionnez le driver WinUSB et installez le.
