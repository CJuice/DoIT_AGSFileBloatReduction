"""
Walk the specified directory, checking the age of folders and files, deleting all that are greater than 5 days in age.
Walk the Temp folder on ArcGIS Server machines. Check the modified date of all folders and files. Delete all items
that are older than 5 days in age unless they are one of the specified folders to skip. See the tuple variable of
directories to skip. Print out indications of age and item path and name that are deleted so that there is transparency.
Date Created: 20190221
Author: CJuice
Revisions:

"""


def main():
    import os
    import datetime

    # root_project_path = os.path.dirname(__file__)   # DEVELOPMENT
    # DIRECTORY_TO_EXAMINE = os.path.join(root_project_path, "Files_For_Testing")    # DEVELOPMENT

    DIRECTORIES_TO_SKIP = ("system", "utilities", "hsperfdata_arcgis-service")
    DIRECTORY_TO_EXAMINE = r"C:\Users\arcgis-service\AppData\Local\Temp"    # PRODUCTION
    FIVE_DAYS_TIME = datetime.timedelta(days=5)
    now = datetime.datetime.now()

    try:
        for root, dirnames, files in os.walk(DIRECTORY_TO_EXAMINE):

            # Need to revise dirnames list and remove the folders we want to skip
            for item in DIRECTORIES_TO_SKIP:
                if item in dirnames:
                    dirnames.remove(item)
                    print("\t\tWill not be evaluated: {}".format(item))
                    print("\t\tRemaining dirnames for consideration: {}".format(dirnames))

            # For each directory, look at the residing folders and files. Begin with folders first.
            for folder in dirnames:
                full_folder_path = os.path.join(root, folder)
                time_dir_last_modified = os.path.getmtime(full_folder_path)
                duration_since_folder_last_modified = now - datetime.datetime.fromtimestamp(time_dir_last_modified)
                print("Folder: {} , Age: {}".format(full_folder_path, duration_since_folder_last_modified))
                is_older_than_five_days = duration_since_folder_last_modified > FIVE_DAYS_TIME
                if is_older_than_five_days:
                    os.remove(folder)
                    print("\tFOLDER: {} has been removed. Age: {}".format(full_folder_path, duration_since_folder_last_modified))

            for file in files:

                # For files in the directory, process them.
                full_file_path = os.path.join(root, file)
                time_file_last_modified = os.path.getmtime(full_file_path)
                duration_since_file_last_modified = now - datetime.datetime.fromtimestamp(time_file_last_modified)
                is_older_than_five_days = duration_since_file_last_modified > FIVE_DAYS_TIME
                if is_older_than_five_days:
                    os.remove(full_file_path)
                    print("\tFILE: {} has been removed. Age: {}".format(full_file_path, duration_since_file_last_modified))
                    
    except IOError as io_err:
        print(io_err)
        exit()
    except Exception as e:
        print(e)
        exit()


if __name__ == "__main__":
    main()

