import ftplib
from tqdm import trange


class GetImagesPls:
    def __init__(self, ftp_host, ftp_username, ftp_passwd, working_dir,
                 start_month=1, end_month=12,
                 start_hr=0, end_hr=23):

        self.ftp_host = ftp_host
        self.ftp_username = ftp_username
        self.ftp_passwd = ftp_passwd
        self.working_dir = working_dir

        self.start_month = start_month
        self.end_month = end_month
        self.start_hr = start_hr
        self.end_hr = end_hr

        self.ftp_obj = self.ftp_make_connection()

    def ftp_make_connection(self):
        ftp_obj = ftplib.FTP()

        # Make Connection
        print("Trying to make a connection...")
        ftp_obj.connect(self.ftp_host)
        ftp_obj.login(user=self.ftp_username, passwd=self.ftp_passwd)
        print("Connection established...")

        # Setting working directory
        ftp_obj.cwd(self.working_dir)

        return ftp_obj

    @staticmethod
    def fetch_folders(ftp_obj):
        # Fetching folders
        print("Fetching folders...")
        folders = ftp_obj.nlst()
        return folders

    def filter_by_month(self):
        """
        Args:
            date_list (str): List containing name of all folders.
            Folders correspond to specific date
            start_month (int, optional): Should be an integer between 1 and 12.
            Defaults to 1.
            end_month (int, optional): Should be an integer between 1 and 12.
            Defaults to 12.

        Returns:
            str: Returns a filtered list containing only entries within the 
            range start_month till end_month
        """

        date_list = GetImagesPls.fetch_folders(self.ftp_obj)

        if self.start_month not in range(1, 12, 1):
            print(f"Invalid start_month: {self.start_month}, using defaults")
            self.start_month = 1

        if self.end_month not in range(1, 12, 1):
            print(f"Invalid end_month: {self.end_month}, using defaults")
            self.end_month = 12

        filtered_date_list = []

        for date in date_list:
            month = int(date[4:6])

            if month >= self.start_month and month <= self.end_month:
                filtered_date_list.append(date)

        self.filtered_date_list = filtered_date_list

        return None

    @staticmethod
    def filter_by_time(file_name, start_hr, end_hr):
        # time in hours from 00 to 24

        if start_hr not in range(0, 23, 1):
            print(f"Invalid start_month: {start_hr}, using defaults")
            start_hr = 0

        if end_hr not in range(0, 23, 1):
            print(f"Invalid end_month: {end_hr}, using defaults")
            end_hr = 23

        # add check here
        hr = int(file_name[8:10])

        if hr >= start_hr and hr <= end_hr:
            return True
        else:
            return False

    def fetch_file_names(self):
        all_files = []

        for i in trange(len(self.filtered_date_list), desc="Days"):
            folder = self.filtered_date_list[i]
            self.ftp_obj.cwd(self.working_dir + "/" + folder)
            files = self.ftp_obj.nlst()

            for j in trange(len(files), desc="Snaps"):
                file = files[j]
                if file.split(".")[-1] == "jpg":
                    date_flag = GetImagesPls.filter_by_time(file,
                                                            self.start_hr,
                                                            self.end_hr)
                    # Add time filter here
                    if date_flag:

                        all_files.append(self.working_dir + "/" +
                                         folder + "/" + file)

        self.all_files = all_files
        return None

    def logging_1(self):
        print(self.filtered_date_list)

    def logging_2(self):
        print(self.all_files)

    def logging_3(self):
        print(f"Num Images: {len(self.all_files) * 350 / 1000000:.2f} GB")


def main():
    # ftp_host = "ftp.schreder-cms.com"
    # ftp = ftplib.FTP()
    # # Make Connection
    # ftp.connect(ftp_host)
    # ftp.login(user='20318_01', passwd='I5Ayut5c')
    # print("Connection established...")

    # # Setting working directory
    # ftp.cwd(working_dir)

    ftp_host = "ftp.schreder-cms.com"
    ftp_username = '20318_01'
    ftp_passwd = 'I5Ayut5c'
    working_dir = "/asi16_data/asi_16030"

    # Creting getimgobj
    some_obj = GetImagesPls(ftp_host,
                            ftp_username,
                            ftp_passwd,
                            working_dir,
                            start_month=7,
                            end_month=7,
                            start_hr=12,
                            end_hr=14)

    some_obj.filter_by_month()
    some_obj.logging_1()

    some_obj.fetch_file_names()
    some_obj.logging_2()
    some_obj.logging_3()

    # # Filtering by months
    # folders = filter_by_month(folders, start_month=5, end_month=8)

    # # Fetching all file paths
    # all_files = fetch_file_names(working_dir, folders, ftp)

    # print(len(all_files))
    # print(all_files[0:3])

    # ftp.cwd("/asi16_data/asi_16030/")

    # # fetch files
    # files = ftp.nlst()

    # for file in files:

    # handle = open(files[0], "wb")
    # ftp.retrbinary('RETR ' + files[0], handle.write)


if __name__ == "__main__":
    main()
