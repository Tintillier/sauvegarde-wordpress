#!/usr/bin/python2
# -*- coding: utf-8 -*-

#import librairies
import os
import time
import sys
import subprocess
import glob
import ftplib
import shutil
from dateutil.relativedelta import relativedelta
# if not found, apt-get install python-dateutil
from datetime import date
from datetime import datetime


#initialisation variables
DATETIME = time.strftime('%Y%d%m-%H%M%S')
DATEJOUR =  time.strftime('%Y%d%m')
BACKUP_PATH = '/home/backup/'
WEB_PATH = '/var/www/html/wordpress'
SQL_PATH = '/var/lib/mysql'
DB_HOST = 'localhost'
DB_USER = 'root'
DB_USER_PASSWORD = 'Admin-pwd'
DB_NAME = 'wordpress_db'
FTP_IP_SRV='192.168.134.133'
FTP_PORT='21'
FTP_USER='sauvegarde'
FTP_PASS='Admin-sav'
FILE_SAV_WORDPRESS =  DATEJOUR + "-wordpress-INCRE-1.tar.bz2" #-1 ière incrementielle
FILE_SAV_MYSQL =  DATEJOUR + "-mysql-INCRE-1.tar.bz2" #-1 1ère incrementielle
FILE_LOG = DATEJOUR + "-log-INCRE-1" #log de la 1ere incrementielle
today = time.strftime('%Y%d%m')
print("Date du jour:", today )
hier =  ((datetime.today()- relativedelta(days=1)).strftime('%Y%d%m'))
print("Date d'hier;", hier)
dateStr = hier
print('Hier dans la variable : ' ,dateStr)
FILE_LOG_COMPLETE = dateStr + "-log"
FILE_SAV_WORDPRESS_HIER =  dateStr + "-wordpress-INCRE-1.tar.bz2" #-1 ière incrementielle
FILE_SAV_MYSQL_HIER =  dateStr + "-mysql-INCRE-1.tar.bz2" #-1 1ère incrementielle
FILE_SAV_LAN_HIER = dateStr + "-conf-lan-INCRE-1.tar.bz2" #-1 1ière incrementielle
FILE_SAV_APACHE_DEFAULT_HIER = dateStr + "-apache-default-INCRE-1.tar.bz2" #-1 1ère incremententielle
LASUITE = 'none'

#verifier que la sauvegarde complète J-1 existe en cherchant le log de la complète
try:
 	f = open(BACKUP_PATH+FILE_LOG_COMPLETE)
	 # est ce que fichier log du jour existe
	LASUITE = 'ok' #sauvegarde complète J-1 existe
except IOError:
    	print ("sauvegarde complète J-1 inexistante")
	LASUITE = 'ko'
else:
  	 # action
	print ("on fait la suite")

if LASUITE == 'ok': #action car sauvegarde complète J-1 existe
	#sauvegarde precedante est la complete et je fais la 1ere  incrementielle
	#fonction pause
	def wait():
		e=raw_input()
		print e

	wait()

	#fichier pour le log du jour
	try:
	    f = open(BACKUP_PATH+FILE_LOG)
	    # est ce que fichier log du jour existe
	except IOError:
	     f = open(BACKUP_PATH+FILE_LOG,"w+") #existe pas on le crée
	     f.write("Subject: SAUVEGARDE INCREMENTIELLE N°1 J2 DU ...") #subjetc: pour l'objet du mail
	     f.write(DATETIME) #ecriture de jour et heure
	     f.write("--------------------------\n")
	finally:
	    f.close() #on ferme le fichier

	#******début processus sauvegarde INCREMENTIELLE****
	print ("sauvegarde incrementielle 1 du dossier site wordpress")
	print "fichier: ", FILE_SAV_WORDPRESS
	print "dans: ", BACKUP_PATH
	try:
		subprocess.call(['tar', '-cvf', BACKUP_PATH + FILE_SAV_WORDPRESS, '-N', BACKUP_PATH + FILE_LOG, WEB_PATH]) #incrementielle differences depuis date du jour de creation du log incrementielle
	except:
		with open(BACKUP_PATH+FILE_LOG,'a') as f: #ouverture du fichier log du jour
			f.write("le...")
			f.write(DATETIME) #ecrire dans log heure et date
			f.write("  ERREUR sur la sauvegarde incrementielle 1 LOCALE de wordpress\n") #ecriture erreur dans log
		print ("erreur rencontrée sauvegarde incrementielle 1 du dossier wordpress")
	else:
		with open(BACKUP_PATH+FILE_LOG,'a') as f: #ouverture du fichier log du jour
			f.write("le...")
			f.write(DATETIME) #ecriture de jour et heure 
	        	f.write("  sauvegarde locale incrementielle 1 wordpress réalisée\n") #ecriture sauvegarde faite dans log
		print ('sauvegarde incrementielle 1 dossier wordpress faite')

	print ("sauvegarde incrementielle 1 du dossier Mysql")
	print "fichier: ", FILE_SAV_MYSQL
	print "dans: ", BACKUP_PATH
	try:
		subprocess.call(['tar', '-cvf', BACKUP_PATH + FILE_SAV_MYSQL, '-N', BACKUP_PATH + FILE_LOG, SQL_PATH]) incrementielle differences depuis date du jour de creation du log incrementielle
		with open(BACKUP_PATH+FILE_LOG,'a') as f: #ouverture du fichier log du jour
			f.write("le...")
			f.write(DATETIME) #ecrire dans log heure et date
			f.write("   ERREUR sur la sauvegarde incrementielle 1 LOCALE du dossier Mysql\n") #ecriture erreur dans log
		print ("erreur rencontrée sur sauvegarde incrementielle 1 locale du dossier Mysql")
	else:
		with open(BACKUP_PATH+FILE_LOG,'a') as f: #ouverture du fichier log du jour
			f.write("le...")
			f.write(DATETIME) #ecriture de jour et heure
	        	f.write("  sauvegarde incrementielle 1 locale du dossier Mysql réalisée\n") #ecriture sauvegarde faite dans log
		print ('sauvegarde incrementielle 1 dossier Mysql faite')

	#fin sauvegarde écriture de fin dans log
	with open(BACKUP_PATH+FILE_LOG,'a') as f: #ouverture du fichier log du jour
		f.write("FIN DE LA SAUVEGARDE INCREMENTIELLE 1 LOCALE DU ...") #ecriture fin de sauvegarde
		f.write(DATETIME) #ecriture de jour et heure
		f.write("--------------------------\n")

	#suppression des sauvegardes en local de plus de 2mn changer 120 pour 5 jours eb 432000
	print ("suppression anciens des fichiers en local de plus de 2mn = 120s et 5 jours = 432000 s")
	deux_minutes_ago = time.time() - 432000
	os.chdir(BACKUP_PATH)
	for somefile in os.listdir('.'):
	    mtime=os.path.getmtime(somefile)
	    if mtime < deux_minutes_ago:
	        os.unlink(somefile)
	print ("nettoyage effectué")

	#transfert vers serveur ftp des sauvegardes
	with open(BACKUP_PATH+FILE_LOG,'a') as f: #ouverture du fichier log du jour
	     f.write("-------------------------------\n")
	     f.write("le...")
	     f.write(DATETIME) #ecriture de jour et heure
	     f.write("  TRANSFERT FTP\n") #ecriture sauvegarde faite dans log

	print ("transfert ftp")
	#transfert sauvegarde dossier wordpress 
	try:
		ftp = ftplib.FTP(FTP_IP_SRV)
		ftp.connect(FTP_IP_SRV, FTP_PORT)
		ftp.login(user = FTP_USER, passwd = FTP_PASS)
		ftp.storbinary("STOR " + FILE_SAV_WORDPRESS, open(FILE_SAV_WORDPRESS, 'rb'))
	except:
	        with open(BACKUP_PATH+FILE_LOG,'a') as f: #ouverture du fichier log du jour
	                f.write("le...")
	                f.write(DATETIME) #ecrire dans log heure et date
	                f.write("   ERREUR sur TRANSFERT FTP sauvegarde incrementielle 1 du dossier Wordpress\n") #ecriture erreur dans log
	        print ("erreur rencontrée")
	else:
	        with open(BACKUP_PATH+FILE_LOG,'a') as f: #ouverture du fichier log du jour
        	        f.write("le...")
	                f.write(DATETIME) #ecriture de jour et heure
        	        f.write("  transfert vers ftp sauvegarde incrementielle 1 du dossier wordpress réalisé\n") #ecriture sauvegarde faite dans log
	        print ('transfert sauvegarde incrementielle 1 dossier wordpress par ftp fait')

	#transfert sauvegarde dossier mysql
	try:
	        ftp = ftplib.FTP(FTP_IP_SRV)
	        ftp.connect(FTP_IP_SRV, FTP_PORT)
	        ftp.login(user = FTP_USER, passwd = FTP_PASS)
	        ftp.storbinary("STOR " + FILE_SAV_MYSQL, open(FILE_SAV_MYSQL, 'rb'))
	except:
	        with open(BACKUP_PATH+FILE_LOG,'a') as f: #ouverture du fichier log du jour
        	        f.write("le...")
	                f.write(DATETIME) #ecrire dans log heure et date
        	        f.write("   ERREUR sur TRANSFERT FTP sauvegarde incrementielle 1  du dossier Mysql\n") #ecriture erreur dans log
	        print ("erreur rencontrée")
	else:
	        with open(BACKUP_PATH+FILE_LOG,'a') as f: #ouverture du fichier log du jour
        	        f.write("le...")
	          	f.write(DATETIME) #ecriture de jour et heure
        	       	f.write("  transfert vers ftp sauvegarde incrementielle 1  du dossier Mysql réalisé\n") #ecriture sauvegarde faite d$
	        print ('transfert sauvegarde incrementielle 1 dossier Mysql par ftp fait')

	#transfert du log
	try:
	        ftp = ftplib.FTP(FTP_IP_SRV)
	        ftp.connect(FTP_IP_SRV, FTP_PORT)
	        ftp.login(user = FTP_USER, passwd = FTP_PASS)
	        ftp.storbinary("STOR " + FILE_LOG, open(FILE_LOG, 'rb'))
	except:
	        with open(BACKUP_PATH+FILE_LOG,'a') as f: #ouverture du fichier log du jour
        	        f.write("le...")
                	f.write(DATETIME) #ecrire dans log heure et date
	                f.write("   ERREUR sur TRANSFERT incrementielle 1 FTP du fichier LOG\n") #ecriture erreur dans log
	        print ("erreur rencontrée")
	else:
	        with open(BACKUP_PATH+FILE_LOG,'a') as f: #ouverture du fichier log du jour
        	        f.write("le...")
	                f.write(DATETIME) #ecriture de jour et heure
        	        f.write("  transfert vers ftp du fichier LOG incrementielle 1  réalisé\n") #ecriture sauvegarde faite d$
	        print ('transfert du LOG V1 de la sauvegarde incrementielle 1 wordpress par ftp fait')

	with open(BACKUP_PATH+FILE_LOG,'a') as f: #ouverture du fichier log du jour
	     f.write("-------------------------------\n")
	     f.write("le...")
	     f.write(DATETIME) #ecriture de jour et heure
	     f.write(" FIN TRANSFERT FTP\n") #ecriture sauvegarde faite dans log

	#transfert dernière ecriture du log
	try:
		ftp = ftplib.FTP(FTP_IP_SRV)
		ftp.connect(FTP_IP_SRV, FTP_PORT)
		ftp.login(user = FTP_USER, passwd = FTP_PASS)
		ftp.storbinary("STOR " + FILE_LOG, open(FILE_LOG, 'rb'))
		print ("transfert ftp LOG final et autres fichiers de sauvegardes finis")
	except:
		print ("erreur fermeture log")
	else:
		print ("fermeture log ok")

	#envoi par mail du rapport (fichier log)
	try:
		filePath = shutil.copy(FILE_LOG, 'LOG-INCRE') #fichier log qui sera envoyé par mail
		#filePath = shutil.copy('/etc/apache2/sites-available/000-default.conf', BACKUP_PATH)
		subprocess.call('/home/superadmin/script/maillog-incre1.sh')
	except:
		print ("erreur envoie mail log")
	else:
	    	print ("fin envoie mail log")

	#FIN
	print ("ensemble des sauvegardes terminées")
	print ("sauvegarde finie")
else:
	print("abandon") #car sauvegarde complète J-1 inexistante

