# sauvegarde-worpress
Scripts python avec sauvegarde déportée en ftp et rapport par email (msmtp)
Les tests on été fait sur Pyhton 2.7.17 et Debian 10

LE SCRIPT (sauver-complete.py) FAIT UNE SAUVEGARDE DE TYPE "COMPLETE" D'UN SITE WORDPRESS
L'envoi du mail fait appel à msmtp (adapter selon votre infrastructure) via le script bash maillog.sh.
        (Dans le fichier maillog.sh adapter en saisissant l'adresse mail de destination)
Le script sauvegarde également les fichiers hosts, hostname, interfaces, resolv.conf et 000-default.conf du serveur web
"Un dump" de la base Mysql est réalisé afin de pouvoir éventuellement faire une intervention manuelle sur la base de donnée

Autres variables à adapter (fichier sauver-complete.py) :
ATTENTION: dans ce script j'efface les anciennes sauvegardes, CHANGER CETTE VALEUR EN SECONDES pour le nombre de jours pendant lesquels vous voulez conserver vos sauvegardes (variable deux_minutes_ago)

BACKUP_PATH = '/home/backup/' >> Dossier pour la sauvegarde sur le serveur
WEB_PATH = '/var/www/html/wordpress' >> Dossier du site Wordpress sur le serveur
SQL_PATH = '/var/lib/mysql' >>Chemin vers la Base Mysql
DB_USER = 'root' >> Utilisateur avec des droits administrateur de la base de données
DB_USER_PASSWORD = 'Admin-pwd' >> Mot de passe du compte ci-dessus
DB_NAME = 'wordpress_db' >> Nom de la base de donnée Wordpress
FTP_IP_SRV='192.168.134.133' >> IP du serveur FTP distant
FTP_PORT='21' >> Port du serveur FTP
FTP_USER='sauvegarde' >> Compte utilisateur avec des droits d'écriture sur le FTP
FTP_PASS='Admin-sav' >> Mot de passe du compte ci-dessus
FILE_SAV_DUMPSQL =  DATEJOUR + "-dumpsql.tar.bz2" >> Donnera un fichier "daté" à la sauvegarde du dump de la base de donnée
FILE_SAV_WORDPRESS =  DATEJOUR + "-wordpress.tar.bz2" >> Donnera un fichier "daté" à la sauvegarde du dossier Wordpress
FILE_SAV_MYSQL =  DATEJOUR + "-mysql.tar.bz2" >> Donnera un fichier "daté" à la sauvegarde du dossier Mysql
FILE_SAV_LAN = DATEJOUR + "-conf-lan.tar.bz2" >> Donnera un fichier "daté" à la sauvegarde des fichiers "réseaux"
FILE_SAV_APACHE_DEFAULT = DATEJOUR + "-apache-default.tar.bz2" >> Donnera un fichier daté à la sauvegarde de apache
FILE_LOG = DATEJOUR + "-log" >> Donnera un fichier daté pour le log de la sauvegarde

Avec crontab -e sur le serveur web vous pouvez ensuite planifier cette sauvegarde 


LE SCRIPT (sauver-incre.py) FAIT UNE SAUVEGARDE DE TYPE "INCREMENTIELLE J+1" SELON LA COMPLETE CI-DESSUS
L'envoi du mail fait appel à msmtp (adapter selon votre infrastructure) via le script bash maillog-incre1.sh.
        (Dans le fichier maillog-incre1.sh adapter en saisissant l'adresse mail de destination)
Le script sauvegarde les fichiers modifiés depuis la sauvegarde complète ci-dessus en ce qui concerne les dossiers WEB_PATH et
SQL_PATH
>> Complète = JOUR J et sauver-incre.py fait une incrementielle J+1
>> Jour J+2, J+3 .../... pas codé actuellement.
