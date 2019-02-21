"""
"""


def main():
    import os
    import datetime

    root_project_path = os.path.dirname(__file__)
    DIRECTORIES_TO_SKIP = ("system", "utilities", "hsperfdata_arcgis-service")
    DIRECTORY_TO_EXAMINE = os.path.join(root_project_path, "Files_For_Testing")    # DEVELOPMENT
    # DIRECTORY_TO_EXAMINE = r"C:\Users\arcgis-service\AppData\Local\Temp"    # PRODUCTION
    FIVE_DAYS_TIME = datetime.timedelta(days=5)
    now = datetime.datetime.now()

    try:
        for dirs, dirname, files in os.walk(DIRECTORY_TO_EXAMINE):
            # print("DIRS: {}".format(dirs))
            # print("\t{}".format(dirname))
            # print("\t{}".format(files))
            for item in DIRECTORIES_TO_SKIP:
                if item in dirname:
                    dirname.remove(item)
                    print("\t\tFolder removed from dirname: {}".format(item))
                    print("\t\tdirname is now: {}".format(dirname))

            # For each directory, look at the residing folders and files. Begin with folders first.
            for folder in dirname:
                full_folder_path = os.path.join(dirs, folder)
                # For folders in the directory, check to see if they are in the skip list. If not, process them
                if os.path.basename(folder) in DIRECTORIES_TO_SKIP:
                    print("Skipping {}".format(folder))
                    continue

                time_dir_last_modified = os.path.getmtime(full_folder_path)
                duration_since_folder_last_modified = now - datetime.datetime.fromtimestamp(time_dir_last_modified)
                is_older_than_five_days = duration_since_folder_last_modified >= FIVE_DAYS_TIME
                if is_older_than_five_days:
                    # os.remove(folder)
                    print("FOLDER: {} has been removed. Age: ".format(full_folder_path, duration_since_folder_last_modified))

            for file in files:

                # For files in the directory, process them.
                full_file_path = os.path.join(dirs, file)
                time_file_last_modified = os.path.getmtime(full_file_path)
                duration_since_file_last_modified = now - datetime.datetime.fromtimestamp(time_file_last_modified)
                is_older_than_five_days = duration_since_file_last_modified >= FIVE_DAYS_TIME
                if is_older_than_five_days:
                    # os.remove(full_file_path)
                    print("FILE: {} has been removed. Age: {}".format(full_file_path, duration_since_file_last_modified))
    except IOError as io_err:
        print(io_err)
        exit()
    except Exception as e:
        print(e)
        exit()


if __name__ == "__main__":
    main()

