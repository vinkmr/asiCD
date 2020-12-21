import ftplib


def filter_by_month(date_list, start_month=1, end_month=12):
    """To filter the directories based on months

    Args:
        date_list ([list:str]): [List containing name of all folders. Folders correspond to specific date]
        start_month (int, optional): [Should be an integer between 1 and 12]. Defaults to 1.
        end_month (int, optional): [Should be an integer between 1 and 12]. Defaults to 12.

    Returns:
        [list:str]: [Returns a filtered list containing only entries within the range start_month till end_month]
    """

    if start_month not in range(1, 12, 1):
        print(f"Invalid start_month: {start_month}, using defaults")
        start_month = 1

    if end_month not in range(1, 12, 1):
        print(f"Invalid end_month: {end_month}, using defaults")
        end_month = 12

    filterd_date_list = []

    for date in date_list:
        month = date[4:6]

        if int(month) >= start_month and int(month) <= end_month:
            filterd_date_list.append(date)

    return filterd_date_list


def main():
    ftp_host = "ftp.schreder-cms.com"
    ftp = ftplib.FTP()

    # Make Connection
    ftp.connect(ftp_host)
    ftp.login(user='20318_01', passwd='I5Ayut5c')

    # fetch folders
    ftp.cwd("/asi16_data/asi_16030/")
    folders = ftp.nlst()
    folders = filter_by_month(folders, start_month=5, end_month=8)
    # print(folders)

    # #
    # ftp.cwd("/asi16_data/asi_16030/")

    # # fetch files
    # files = ftp.nlst()

    # for file in files:

    # handle = open(files[0], "wb")
    # ftp.retrbinary('RETR ' + files[0], handle.write)


if __name__ == "__main__":
    main()
