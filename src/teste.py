import subprocess

# Exécute le premier fichier Python
subprocess.run(["python3", "webtoon_downloader.py", "https://www.webtoons.com/fr/fantasy/tower-of-god/list?title_no=1832", "--latest"], check=True)

#subprocess.run(["python", "co.py"], check=True)
subprocess.run(["python", "renomme.py"], check=True)
# Exécute la commande après la fin de l'exécution du premier fichier
subprocess.run(["npx", "ts-node", "start.ts"],shell=True, check=True)

#subprocess.run(["python", "adition.py"], check=True)
