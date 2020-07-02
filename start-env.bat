@echo off
IF exist donnees_sorties ( echo Ok ) ELSE ( mkdir donnees_sorties && echo Dossier donnees_sorties créé. )
IF exist entrees_csv ( echo  Ok ) ELSE ( mkdir entrees_csv && echo Dossier entrees_csv créé. )
start env-python\Scripts\activate.bat
