import ftplib
from tqdm import trange
from tqdm import tqdm
from pprint import pprint

# Local Modules
from asiCD.asiCD_utils import load_json


class GetImagesPls:
    """
    Describe
        member functions
        public variables
    """

    def __init__(
        self,
        ftp_host,
        ftp_username,
        ftp_passwd,
        ftp_working_dir,
        local_output_path,
        start_month=1,
        end_month=12,
        start_hr=0,
        end_hr=23,
        sampling_rate=10,
        log_level=4,
    ):

        self.ftp_host = ftp_host
        self.ftp_username = ftp_username
        self.ftp_passwd = ftp_passwd
        self.ftp_working_dir = ftp_working_dir
        self.local_output_path = local_output_path

        self.start_month = start_month
        self.end_month = end_month
        self.start_hr = start_hr
        self.end_hr = end_hr
        self.sampling_rate = sampling_rate
        self.log_level = log_level

        self.ftp_obj = self.ftp_make_connection()

    def ftp_make_connection(self):
        """
        Creates an FTP object.
        Establish an ftp connection with the host ftp server.
        Changes the current working directory to the ftp_working_directory.

        Returns:
            ftp_obj (bool) : Returns an object of the class ftplib.FTP() after establishing a connection to the server.
        """
        ftp_obj = ftplib.FTP()

        # Make Connection
        print("Trying to make a connection...")
        ftp_obj.connect(self.ftp_host)
        ftp_obj.login(user=self.ftp_username, passwd=self.ftp_passwd)
        print("Connection established...")

        # Setting working directory
        ftp_obj.cwd(self.ftp_working_dir)

        return ftp_obj

    # @staticmethod any justification??
    def fetch_folders(self):
        """
        Creates a list of all folders in the current working directory.
        """
        # Fetching folders
        print("Fetching folders...")
        self.folders = self.ftp_obj.nlst()
        # return self.folders

    def filter_by_month(self):
        """
        Creates a filtered list containing folders that lie within the specified month interval.
        """

        # check if input parameters are valid and set defaults if not
        if self.start_month not in range(1, 12, 1):
            print(f"Invalid start_month: {self.start_month}, using defaults")
            start_month = 1

        if self.end_month not in range(1, 12, 1):
            print(f"Invalid end_month: {self.end_month}, using defaults")
            end_month = 12

        # obtain a list of all folder from the cwd in the ftp host # parameterized. no need to call method again
        # folder_list = GetImagesPls.fetch_folders(self.ftp_obj)

        filtered_by_month_folder_list = []

        for folder in self.folders:
            month = int(folder[4:6])

            if month >= self.start_month and month <= self.end_month:
                filtered_by_month_folder_list.append(folder)

        self.filtered_by_month_folder_list = filtered_by_month_folder_list

        # return filtered_by_month_folder_list

    def fetch_file_names(self):
        """
        Creates a filtered list of all filepaths for all jpg files in a folder.
        Files are filtered based on specified time range.
        """

        file_paths = []

        for i in trange(len(self.folders), desc="Days"):
            folder = self.folders[i]
            self.ftp_obj.cwd(self.ftp_working_dir + "/" + folder)
            files = self.ftp_obj.nlst()

            for j in trange(len(files), desc="Snaps"):
                file = files[j]
                if file.split(".")[-1] == "jpg":
                    date_flag = self.filter_by_time(file, self.start_hr, self.end_hr)
                    # freq_flag => sample on a per hour basis
                    # Add time filter here
                    if date_flag:
                        file_paths.append(
                            self.ftp_working_dir + "/" + folder + "/" + file
                        )

        self.file_paths = file_paths
        # return file_paths

    # @staticmethod any justification??
    def filter_by_time(self, file_name):
        """
        Sets flag to True or False based on condition for provided filename

        Args:
            file_name (str): Filename of image excluding the extension

        Returns:
            bool : Returns True if file_name is within the range of start_hr to end_hr,
                    else returns False otherwise
        """
        # time in hours from 00 to 24

        if self.start_hr not in range(0, 23, 1):
            print(f"Invalid start_month: {self.start_hr}, using defaults")
            start_hr = 0

        if self.end_hr not in range(0, 23, 1):
            print(f"Invalid end_month: {self.end_hr}, using defaults")
            end_hr = 23

        # add check here
        hr = int(file_name[8:10])

        if hr >= self.start_hr and hr <= self.end_hr:
            return True
        else:
            return False

    def sampling_per_hour(self):
        """
        Creates a reduced subset of images/files to be taken into consideration by sampling them per hour.
        """
        sampled_file_paths = []
        all_file_paths = self.file_paths
        # hours = self.end_hr - self.start_hr

        count = 0
        for _ in range(int(len(self.file_paths) / (self.sampling_rate)) - 1):
            sampled_file_paths.append(all_file_paths[count + self.sampling_rate])
            count = count + self.sampling_rate

        self.sampled_file_paths = sampled_file_paths

    def download_files(self):
        """
        Downloads files from the ftp server after applying filters based on month, time and sampling rate.
        """
        self.fetch_folders()
        self.filter_by_month()
        self.fetch_file_names()
        self.filter_by_time()
        self.sampling_per_hour()

        for file_path in tqdm(self.sampled_file_paths):

            file_dir = "/".join(file_path.split("/")[:-1])
            file_name = file_path.split("/")[-1]

            # Changing to file directory
            self.ftp_obj.cwd(file_dir)

            # Downloading the file
            local_file = open(self.local_output_path + "/" + file_name, "wb")
            self.ftp_obj.retrbinary("RETR " + file_name, local_file.write)
            local_file.close()

    def log_level(self):
        logs = {
            1: self.logging_1(),
            2: self.logging_2(),
            3: self.logging_3(),
            4: self.logging_4(),
        }
        logs.get(self.log_level)

    def logging_1(self):
        """Logging for filtered folder list"""
        print(self.filtered_by_month_folder_list)

    def logging_2(self):
        """Logging for filepaths"""
        pprint(self.file_paths[:10])

    def logging_3(self):
        """Logging for sampled files list"""
        pprint(self.sampling_per_hour()[:10])

    def logging_4(self, img_size_kb=180):
        """Logging from estimated size of original files to be  downloaded and for sampled files

        Args:
            img_size_kb (int, optional): Estimated average file size. Defaults to 180.
        """

        d_size_original = (len(self.file_paths) * img_size_kb) / 1000000
        d_size_sample = d_size_original / self.sampling_rate

        print(f"Original Size: {d_size_original:.2f} GB")
        print(f"Sample Size: {d_size_sample:.2f} GB")


def main():

    credentials = load_json("credentials.json")

    ftp_host = credentials["ftp_host"]
    ftp_username = credentials["ftp_username"]
    ftp_passwd = credentials["ftp_passwd"]

    ftp_working_dir = "/asi16_data/asi_16030"
    local_output_path = "dataset/asi"

    # Creting getimgobj
    some_obj = GetImagesPls(
        ftp_host,
        ftp_username,
        ftp_passwd,
        ftp_working_dir,
        local_output_path,
        start_month=7,
        end_month=7,
        start_hr=12,
        end_hr=12,
        sampling_rate=20,
        log_level=1,
    )
    # ftp_make_connection method is called and connection is established and the cwd is changed to ftp_working_dir

    some_obj.download_files()


if __name__ == "__main__":
    main()
