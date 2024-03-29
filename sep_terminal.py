import os
import sys
import shutil
import datetime
from PIL import Image
 

"""
checks the existence of a file and renames it if it exists on the destination and returns the abs path of destination
"""
def check_existace_and_rename(src_path, dest_path):
    i = 1
    file_name = os.path.basename(src_path)
    name_temp = file_name
    is_name_changed = False
    while os.path.exists(dest_path + os.sep + name_temp):
        is_name_changed = True
        name_temp = file_name
        name_without_extension = os.path.splitext(name_temp)[0]
        extension = os.path.splitext(name_temp)[1]

        name_temp = name_without_extension + "(" + i.__str__() + ")" + extension
        i += 1

    return (dest_path + os.sep + name_temp), is_name_changed, src_path 

"""
moves file
"""
def move_file(src, dest):
    try:
        shutil.move(src, dest)
        return 1
    except(FileNotFoundError):
        print("file not found")
        return 0

"""
copies file
"""
def copy_file(src, dest):
    try:
        shutil.copy(src, dest)
        return 1
    except(FileNotFoundError):
        print("file not found")
        return 0

"""
gets date from exif data
"""
def get_date_taken_EXIF(path):
    try:
        date = Image.open(path)._getexif()[36867]
        date = date.replace(":", "-")
        return date, True
    except:
        return 0, False

"""
gets file modify date from os
"""
def get_date_modification_SYSTEM(path):
    try:
        posix_time = os.path.getmtime(path)
        date = datetime.datetime.utcfromtimestamp(posix_time).strftime('%Y-%m-%d %H-%M-%S')
        return date, True
    except(FileNotFoundError):
        return 0, False

"""
creates dir if not exists returns it regardless
"""
def create_dir_if_not_exists(dir_path, dir_name):
    dir = dir_path + os.sep + dir_name
    try:
        os.makedirs(dir)
        return dir
    except FileExistsError:
        return dir

"""
checks the extensions list for selecting files if * is given returns 1 to accept all files
"""
def check_extension(extensions_list, path):
    if (extensions_list[0] == "*"):
        return 1
    else:
        for extension in extensions_list:
            if (os.path.splitext(path)[1] == extension):
                return 1
        return 0

"""
prints list line by line
"""
def printlist(list):
    for i in range(len(list)):
        print((i + 1).__str__() + ": " + list[i])


"""
writes list line by line
"""
def writelist(file, list):
    for i in range(len(list)):
        file.write((i + 1).__str__() + ": " + list[i] + "\n")


"""
gets commands entered converts them into usefull format
"""
def parse_command(date_source_selection, cp_or_mv_selection, day_monty_year_selection,extensions, path_from, path_to):

    extensions_list = []

    are_parameters_ok = True


    if( not (date_source_selection == "-E" or date_source_selection == "-S" or date_source_selection == "-ES")):
        are_parameters_ok = False


    if( not (cp_or_mv_selection == "-cp" or cp_or_mv_selection == "-mv")):
        are_parameters_ok = False

    if( not (day_monty_year_selection == "-d" or day_monty_year_selection == "-m" or day_monty_year_selection == "-y")):
        are_parameters_ok = False

    if(extensions == "*"):
        extensions_list.append("*")
    elif(len(extensions) != 0):
        extensions_list = extensions.split(',')
    else:
        are_parameters_ok = False
        print("extension error")


    if( not os.path.isdir(path_from)):
        are_parameters_ok = False
        print(path_from + " is not a dir")


    new_main_dir_path, new_main_dir_name = os.path.split(path_to)
    if( not os.path.isdir(new_main_dir_path)):
        are_parameters_ok = False
        print(new_main_dir_path + " is not a dir")

    return are_parameters_ok, extensions_list

"""
useage information for -- jelp menu
"""
def help():
    print("""
        Info: This program separates and re-folders files according to their system modification or exif dates.
        
        -E use only exif date
        -S use only system provided modification date
        -ES use both but prioritise exif
        
        -cp copy files to the new directory
        -mv move files to the new directory
        
        -d is daily separation depth
        -m is monthly separation depth
        -y is yearly separation depth
        
        --help opens this info page
        
        you can use * for all files or type individual file extensions
        
        example usages:
        sep.py -ES -cp -m .jpg,.png,.txt C:\somedir\old_folder C:\somedir\hi_new_folder
        sep.py -S -mv -d * C:\somedir\old_folder C:\somedir\hi_new_folder
        
        NOTE: All fields are necessary you need to specify all of it like in the examples,
              extensions are case sensitive be careful. 
    """)


"""
writes lists to a file
"""
def write_extra_info_to_file(path, file_name, all_files_list, files_with_no_exif_list, changed_file_names_list):
    with open(path + os.sep + file_name + ".txt", 'a', encoding='utf-8') as file:

        #if exif is not selected we should notify
        if(files_with_no_exif_list[0] == "exif_not_selected"):
            exif_count = "exif data not scanned (if you want to get exif information, use with exif option selected)"
        else:
            exif_count = len(files_with_no_exif_list).__str__()
        

        file.write("--- Content of the file --- \n 1-All files and their old and new directories. Total: " + len(all_files_list).__str__()
                + " \n 2-Files with no exif data. Total: " + exif_count
                + "\n 3-Files that renamed because of the name collision. Total: " +  len(changed_file_names_list).__str__())
        file.write("\n")
        file.write("\n")
        
        file.write("\n")
        file.write("\n")
        file.write("----------------------------------------------------")
        file.write("\n")
        file.write("--- List of all files and directories old -> new ---")
        file.write("\n")
        file.write("----------------------------------------------------")
        file.write("\n")
        file.write("\n")

        writelist(file, all_files_list)
        
        file.write("\n")
        file.write("\n")
        file.write("--------------------------------------------------")
        file.write("\n")
        file.write("--- List of files that has no exif information ---")
        file.write("\n")
        file.write("--------------------------------------------------")
        file.write("\n")
        file.write("\n")

        writelist(file, files_with_no_exif_list)
        
        file.write("\n")
        file.write("\n")
        file.write("----------------------------------------------------------------")
        file.write("\n")
        file.write("--- List of files that renamed because of the name collision ---")
        file.write("\n")
        file.write("----------------------------------------------------------------")
        file.write("\n")
        file.write("\n")

        writelist(file, changed_file_names_list)
        
            


"""
gets all file paths in a directory separetes those files according to the given values and re-folders them
"""
def seperate(date_source_selection, cp_or_mv_selection, day_monty_year_selection, extensions_list, old_main_dir,new_main_dir):

    # -------------------------------------------gating all files from all subdirs--------------------------------------

    all_subdirs = []  # unused
    file_paths = []

    for sub_dir in os.walk(old_main_dir):                         # walks on subdirs
        all_subdirs.append(sub_dir[0])                            # apends all subdirs (unused)
        file_paths_temp = os.listdir(sub_dir[0])                  # gets all files from a subdir and puts them inside file_paths_temp
        for file_path_temp in file_paths_temp:                    # walks on the files that we get from a single subdir
            abs_path = sub_dir[0] + os.sep + file_path_temp       # adds path to the name of the file to get abs path
            if (os.path.isfile(abs_path)):                        # checks if abs path is file or folder if it is file than ok
                if (check_extension(extensions_list,abs_path)):   # calls check extensions function for checking the extension
                    file_paths.append(abs_path)                   # if extension is ok than apend it to file paths


    # printlist(file_paths)

    # ------------------------------copy or move files to apropriate destinations-----------------------------------

    # split new path and name
    new_main_dir_path, new_main_dir_name = os.path.split(new_main_dir)

    # create new folder for puting seperated stuff in
    create_dir_if_not_exists(dir_path=new_main_dir_path, dir_name=new_main_dir_name)

    # status for informatin
    status = 1
    
    #those lists are for report file they are for collecting and displaying extra information in the report file
    changed_file_names_list = []
    files_with_no_exif_list = []
    all_files_list = []

    for file_path in file_paths:

        print(len(file_paths).__str__() + "/" + status.__str__() + " -> " + os.path.basename(file_path))
        status += 1

        # these are needed to understand existance ofdates
        is_exif_exists = False
        is_modified_date_exists = False

        # this part tries to get exif date if E or ES option selected
        if (date_source_selection == "-E" or date_source_selection == "-ES"):
            # getting exif date
            date, is_exif_exists = get_date_taken_EXIF(path=file_path)
            # if date exists
            if (is_exif_exists):
                if (day_monty_year_selection == "-y" or day_monty_year_selection == "-m" or day_monty_year_selection == "-d"):
                    dir_for_copy = create_dir_if_not_exists(dir_path=new_main_dir, dir_name=date[:4] + "-exif")
                    if (day_monty_year_selection == "-m" or day_monty_year_selection == "-d"):
                        dir_for_copy = create_dir_if_not_exists(dir_path=dir_for_copy, dir_name=date[:7])
                        if (day_monty_year_selection == "-d"):
                            dir_for_copy = create_dir_if_not_exists(dir_path=dir_for_copy, dir_name=date[:10])
            else:
                #---(FOR report text)--- appending files that has no exif info to the list ---(FOR report text)---
                files_with_no_exif_list.append(file_path)

        # this part gets system provided modify date if S or ES option selected
        if ((date_source_selection == "-S" or date_source_selection == "-ES") and (not is_exif_exists)):
            # getting system date
            date, is_modified_date_exists = get_date_modification_SYSTEM(path=file_path)
            # if date exists
            if (is_modified_date_exists):
                if (day_monty_year_selection == "-y" or day_monty_year_selection == "-m" or day_monty_year_selection == "-d"):
                    dir_for_copy = create_dir_if_not_exists(dir_path=new_main_dir, dir_name=date[:4])
                    if (day_monty_year_selection == "-m" or day_monty_year_selection == "-d"):
                        dir_for_copy = create_dir_if_not_exists(dir_path=dir_for_copy, dir_name=date[:7])
                        if (day_monty_year_selection == "-d"):
                            dir_for_copy = create_dir_if_not_exists(dir_path=dir_for_copy, dir_name=date[:10])

        # if no date found anywhere don't touch that file
        if (not is_modified_date_exists and not is_exif_exists):
            continue

        #now we have destination path but there can be collision so we check for that and make a rename if needed
        dest, is_name_changed, original_src = check_existace_and_rename(src_path=file_path, dest_path=dir_for_copy)

        #---(FOR report text)--- if name changed append this file to changed_file_names_list ---(FOR report text)---
        if(is_name_changed):
            changed_file_names_list.append(original_src + " -> " + dest)

        #---(FOR report text)--- append every file to all_files_list this will be used in the report text ---(FOR report text)---
        all_files_list.append(original_src + " -> " + dest)

        # copy or move file to destination
        if (cp_or_mv_selection == "-cp"):
            copy_file(src=file_path, dest=dest)
        elif (cp_or_mv_selection == "-mv"):
            move_file(src=file_path, dest=dest)

    #---(FOR report text)--- if exif id not checked at all we need to show it in the report ---(FOR report text)---
    if(date_source_selection == "-S"):
        files_with_no_exif_list.append("exif_not_selected")

    #writing all the extra information to info file
    write_extra_info_to_file(new_main_dir, "Report", all_files_list, files_with_no_exif_list, changed_file_names_list)



"""
uses 6 arguments -date source- copy or move -day month year selection- -extension to use- -old path- and -new path-
parses those 6 arguments via parse_command function if there is a problem with arguments offers help if not calls separate function to make separation
"""
if __name__ == "__main__":
    try:
        date_source_selection = str(sys.argv[1])
        cp_or_mv_selection = str(sys.argv[2])
        day_monty_year_selection = str(sys.argv[3])
        extensions = str(sys.argv[4])
        path_from = str(sys.argv[5])
        path_to = str(sys.argv[6])

        are_parameters_ok, extensions_list = parse_command(date_source_selection, cp_or_mv_selection, day_monty_year_selection, extensions, path_from, path_to)

        if(are_parameters_ok):
            seperate(date_source_selection, cp_or_mv_selection, day_monty_year_selection, extensions_list, path_from, path_to)
        else:
            raise ValueError

    except:
        try:
            if (date_source_selection == "--help"):
                help()
            else:
                raise ValueError
        except:
            print("Invalid input")
            print("--help for usage details")
            exit(0)




