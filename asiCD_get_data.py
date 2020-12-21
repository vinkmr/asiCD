import ftplib

ftp_host = "ftp.schreder-cms.com"

ftp = ftplib.FTP()

ftp.connect(ftp_host)

ftp.login(user='20318_01',passwd='I5Ayut5c' )

ftp.cwd("/asi16_data/asi_16030/20190703/")

files = ftp.nlst()

print(files)

handle = open(files[0],"wb")
# for file in files:
ftp.retrbinary('RETR ' + files[0], handle.write)