import ftplib
from tqdm import trange
from tqdm import tqdm
from pprint import pprint

# Local Modules
from asiCD.asiCD_utils import load_json


class asiParser:

    def __init__(self, ftp_host, ftp_username, ftp_passwd, ftp_working_dir,
                 local_output_path, run_mode="DEBUG"):

        self.ftp_host = ftp_host
        self.ftp_username = ftp_username
        self.ftp_passwd = ftp_passwd
        self.ftp_working_dir = ftp_working_dir
        self.local_output_path = local_output_path
        self.run_mode = run_mode

        self.ftp_obj = self.ftp_make_connection()

    def ftp_make_connection(self):
        ftp_obj = ftplib.FTP()

        # Make Connection
        print("Trying to make a connection...")
        ftp_obj.connect(self.ftp_host)
        ftp_obj.login(user=self.ftp_username, passwd=self.ftp_passwd)
        print("Connection established...")

        # Setting working directory
        ftp_obj.cwd(self.ftp_working_dir)

        return ftp_obj

    @staticmethod
    def fetch_folders(ftp_obj):
        # Fetching folders
        folders = ftp_obj.nlst()
        return folders

    @staticmethod
    def filter_by_month(date_list, start_month, end_month):
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

        if start_month not in range(1, 12, 1):
            print(f"Invalid start_month: {start_month}, using defaults")
            start_month = 1

        if end_month not in range(1, 12, 1):
            print(f"Invalid end_month: {end_month}, using defaults")
            end_month = 12

        filtered_date_list = []

        for date in date_list:
            month = int(date[4:6])

            if month >= start_month and month <= end_month:
                filtered_date_list.append(date)

        return filtered_date_list

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

    @staticmethod
    def sampling_per_hour(all_file_paths, sampling_rate):
        # TODO change rate to mean samples per hour
        sampled_file_paths = []
        count = 0
        for _ in range(int(len(all_file_paths)/(sampling_rate))-1):
            sampled_file_paths.append(all_file_paths[count + sampling_rate])
            count = count + sampling_rate

        return sampled_file_paths

    def get_filtered_files(self, start_m, end_m, start_hr, end_hr, s_rate=-1):

        # Apply month filter
        folder_all = asiParser.fetch_folders(self.ftp_obj)
        folder_fil_m = asiParser.filter_by_month(folder_all, start_m, end_m)

        # Logging
        if self.run_mode == "DEBUG":
            asiParser.log_folder_names(folder_all,
                                       tag="All folder available", limit=20)
            asiParser.log_folder_names(folder_fil_m,
                                       tag="Filtered folder list", limit=20)

        # Apply date filter
        files_fil_mt = []
        for i in trange(len(folder_fil_m), desc="Days"):
            folder = folder_fil_m[i]
            self.ftp_obj.cwd(self.ftp_working_dir + "/" + folder)
            files = self.ftp_obj.nlst()

            # TODO Add sampling here
            # freq_flag => randomly sample on a per hour basis
            for j in range(len(files)):
                file = files[j]
                if file.split(".")[-1] == "jpg":
                    date_flag = asiParser.filter_by_time(file,
                                                         start_hr,
                                                         end_hr)
                    if date_flag:
                        files_fil_mt.append(self.ftp_working_dir + "/" +
                                            folder + "/" + file)

        asiParser.log_dataset_size(num_files=len(files_fil_mt),
                                   sampling_rate=s_rate)

        # Apply Sampling filter
        if s_rate >= 1:
            files_fil_mts = asiParser.sampling_per_hour(files_fil_mt,
                                                        s_rate)
        else:
            return files_fil_mt

        return files_fil_mts

    def download_files(self, start_m:int, end_m:int, start_hr:int, end_hr:int, s_rate:int):
        """Download image files from the FTP server based on certain conditions.
            NOTE: All-Sky Images are recorded every 20 seconds, i.e., 3 images per minute. 

        Args:
            start_m (int): Starting month of the year from which data is to be considered 
            end_m (int): Month of the year till which data is to be considered
            start_hr (int): Hour of the day from which data is to be considered
            end_hr (int): Hour of the day till which data is to be considered
            s_rate (int): Every nth(s_rate) image to be considered. Example: For s_rate = 180, every 180th image is considered. 

        Returns:
            [type]: [description]
        """
        sampled_file_paths = self.get_filtered_files(start_m=start_m,
                                                     end_m=end_m,
                                                     start_hr=start_hr,
                                                     end_hr=end_hr,
                                                     s_rate=s_rate)

        for file_path in tqdm(sampled_file_paths):

            file_dir = "/".join(file_path.split("/")[:-1])
            file_name = file_path.split("/")[-1]

            # Changing to file directory
            self.ftp_obj.cwd(file_dir)

            # Downloading the file
            local_file = open(self.local_output_path + "/" + file_name, 'wb')
            self.ftp_obj.retrbinary('RETR ' + file_name, local_file.write)
            local_file.close()

        return True

    # Logging Fucntions
    @staticmethod
    def log_folder_names(folder_list, tag, limit=0):
        """Logging folder list
        """
        print(tag)
        pprint(folder_list[0:limit])

    @staticmethod
    def log_dataset_size(num_files, sampling_rate, img_size_kb=180):
        # TODO use ftp.size to get dataset size
        d_size_original = (num_files * img_size_kb) / 1000000
        d_size_sample = abs(d_size_original / sampling_rate)

        print(f"Original Size:\t {d_size_original:.3f} GB")
        print(f"Sample Size:\t {d_size_sample:.3f} GB")


def main():

    credentials = load_json("credentials.json")

    ftp_host = credentials["ftp_host"]
    ftp_username = credentials["ftp_username"]
    ftp_passwd = credentials["ftp_passwd"]

    ftp_working_dir = "/asi16_data/asi_16030"
    local_output_path = "dataset/asi"

    # Creating ftp parser obj
    some_obj = asiParser(ftp_host,
                         ftp_username,
                         ftp_passwd,
                         ftp_working_dir,
                         local_output_path,
                         run_mode="RUN")

    # sample_dates = some_obj.get_filtered_files(start_m=7,
    #                                            end_m=7,
    #                                            start_hr=12,
    #                                            end_hr=12,
    #                                            s_rate=20)
    # pprint(sample_dates[0:10])

    some_obj.download_files(start_m=7,
                            end_m=8,
                            start_hr=10,
                            end_hr=16,
                            s_rate=180)


if __name__ == "__main__":
    main()
