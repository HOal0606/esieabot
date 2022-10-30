# esieabot
langage python

Le programme commande le bot ESIEA

le version de python est de 3.90 à 3.10

les pré-requis à installer dans le système du bot :

	Installtion mise à jour système
	Installation python3 :
		sudo apt install python3-pip
		sudo apt install python3-pip python3-cffi
		sudo pip3 install -U setuptools
		sudo pip3 install discord.py
		
	installation discord.py 

les commandes pour faire diriger le bot sont :

	à prendre en compte les "xxx" en fin de commande = vitesse du robot plafonner à 255.

        ss : arrêt robot (en cas d'arrêt d'urgence ou arrêt)        
        ffxxx : avance robot tout droit        
        frxxx : robot tourne à droit      
        flxxx : robot tourne à gauche    
        bbxxx : robot recule
        help : afficher les commandes

pour activer le lancement automatique du programme au démarrage suivre les étapes suivantes

	* ajouter fichier monProgPython.service dans le repertoire /etc/systemd/system
	* ajouter les lignes suivantes :
		ExecStart= "chemin du programme"/esieabotPy.py 
		[Unit]
		Description=esieabot-Python
		[Service]
		Type=simple
		ExecStart= /usr/bin/python3.9 /boot/esieabot/service/esieabotPy.py
		Restart=on-failure
		RestartSec=30
		StandardOutput=file:/boot/esieabot/logs/esieabotPy.log
		StandardError=file:/boot/esieabot/logs/esieabotPy.log
		[Install]
		WantedBy=multi-user.target
	* activer le lancement avecles commandes suivnates:
		sudo systemctl daemon-reload
		sudo systemctl monProgPython.service



