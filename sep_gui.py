import os
import sys
import shutil
import datetime
from PIL import Image

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QFileDialog, QFrame
import threading





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
frame class
"""
class sep_frame(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()

        self.init_variables()
        self.create_frame()



    """
    inits variables
    """
    def init_variables(self):
        #current dir
        #self.old_file_dir = os.getcwd()
        #self.new_file_dir = os.getcwd() + os.sep + "new_folder"

        #desktop
        self.old_file_dir = os.path.abspath(os.path.expanduser("~/Desktop"))
        self.new_file_dir = os.path.abspath(os.path.expanduser("~/Desktop") + os.sep + "new_folder")

        #create threads veriable
        self.thread

        #for stopping thread
        self.stop_thread = False



    """
    creates frame
    """
    def create_frame(self):

        self.setWindowTitle("Easy Separate")
        self.setGeometry(100, 100, 300, 250)
        self.setFixedSize(400, 260)

        self.labels()
        self.line_edits()
        self.buttons()
        self.radio_butons()
        self.checkoxes()

        self.show()



    """
    label options
    """
    def labels(self):

        self.info_label = QtWidgets.QLabel(self)

        #shows borders
        self.info_label.setFrameShape(QFrame.Panel)
        self.info_label.setFrameShadow(QFrame.Sunken)
        self.info_label.setLineWidth(2)

        self.info_label.setText("EASY SEPARATE")
        self.info_label.move(10, 130)
        self.info_label.setFixedSize(380,30)
        self.info_label.setAlignment(QtCore.Qt.AlignCenter)

        labbel_font1 = self.info_label.font()
        labbel_font1.setPointSize(10)
        labbel_font1.setBold(True)
        self.info_label.setFont(labbel_font1)

    """
    lineedit options
    """
    def line_edits(self):

        self.old_file_line = QtWidgets.QLineEdit(self)
        self.old_file_line.setText(self.old_file_dir)
        self.old_file_line.move(120, 10)
        self.old_file_line.setFixedSize(270,30)

        self.new_file_line = QtWidgets.QLineEdit(self)
        self.new_file_line.setText(self.new_file_dir)
        self.new_file_line.move(120, 50)
        self.new_file_line.setFixedSize(270, 30)

        self.extensions_line = QtWidgets.QLineEdit(self)
        self.extensions_line.setText(".jpg,.png,.txt")
        self.extensions_line.move(120, 90)
        self.extensions_line.setFixedSize(270, 30)
        self.extensions_line.setEnabled(False)

        line_font1 = self.old_file_line.font()
        line_font1.setPointSize(10)
        line_font1.setBold(True)
        self.old_file_line.setFont(line_font1)
        self.new_file_line.setFont(line_font1)
        self.extensions_line.setFont(line_font1)



    """
    opens file selection dialog for old file
    """
    def old_file_button_function(self):
        file = str(os.path.abspath(QFileDialog.getExistingDirectory(self, "Select Directory")))
        self.old_file_line.setText(file)

    """
    opens file selection dialog for new file
    """
    def new_file_button_function(self):
        file = str(os.path.abspath(QFileDialog.getExistingDirectory(self, "Select Directory")))
        self.new_file_line.setText(file)

    """
    creates info pop up
    """
    def info_button_function(self):
        QtWidgets.QMessageBox.information(self,'INFO',"""
This program separates and re-folders files according to their system modification or exif dates.
        
usage:
1-select the folder that you want to re-folder.
2-select new folder that will be used as root folder for separated files.
3-type extensions to be separated or check all extensions box.
4-select exif or system modify date or both (if both is selected exif will be prioritised).
5-select year month or day to select separation dept.
6-select move or copy.
7-press separate button to start process.
""")

    """
    stops thread
    """
    def stop_button_function(self):
        self.stop_thread = True
        self.info_label.setText("stopped")

    """
    when separate button clicked takes all parameters from gui checks them and creates a thread for separate function
     ----------------------------THREAD IS USED TO PREVENT FREZING OF THE FRAME------------------------------------------------------------------------
    """
    def separate_button_function(self):
        self.stop_thread = False
        are_parameters_ok, date_source_selection, cp_or_mv_selection, day_monty_year_selection, extensions_list, path_from, path_to = self.value_collector()
        if(are_parameters_ok):
            self.thread = threading.Thread(target=self.seperate, args=(date_source_selection, cp_or_mv_selection, day_monty_year_selection, extensions_list, path_from, path_to), daemon = True)
            self.thread.start()
            #self.seperate(date_source_selection, cp_or_mv_selection, day_monty_year_selection, extensions_list, path_from, path_to)

    """
    button options
    """
    def buttons(self):
        self.old_file_button = QtWidgets.QPushButton(self)
        self.old_file_button.setText("select old")
        self.old_file_button.move(10, 10)
        self.old_file_button.clicked.connect(self.old_file_button_function)

        self.new_file_button = QtWidgets.QPushButton(self)
        self.new_file_button.setText("select new")
        self.new_file_button.move(10, 50)
        self.new_file_button.clicked.connect(self.new_file_button_function)

        self.info_button = QtWidgets.QPushButton(self)
        self.info_button.setText("Info")
        self.info_button.move(315, 165)
        self.info_button.setFixedSize(75, 27)
        self.info_button.clicked.connect(self.info_button_function)

        self.stop_button = QtWidgets.QPushButton(self)
        self.stop_button.setText("stop")
        self.stop_button.move(315, 195)
        self.stop_button.setFixedSize(75, 27)
        self.stop_button.clicked.connect(self.stop_button_function)

        self.separate_button = QtWidgets.QPushButton(self)
        self.separate_button.setText("Separate")
        self.separate_button.move(315, 225)
        self.separate_button.setFixedSize(75,27)
        self.separate_button.clicked.connect(self.separate_button_function)



    """
    radiobutton options
    """
    def radio_butons(self):
        self.S = QtWidgets.QRadioButton("system modify", self)
        self.S.move(10, 170)
        self.S.setChecked(True)

        self.E = QtWidgets.QRadioButton("EXIF", self)
        self.E.move(10, 200)

        self.ES = QtWidgets.QRadioButton("EXIF + system", self)
        self.ES.move(10, 230)

        S_E_ES_button_group = QtWidgets.QButtonGroup(self)
        S_E_ES_button_group.addButton(self.S)
        S_E_ES_button_group.addButton(self.E)
        S_E_ES_button_group.addButton(self.ES)


        self.year = QtWidgets.QRadioButton("year", self)
        self.year.move(150, 170)

        self.month = QtWidgets.QRadioButton("month", self)
        self.month.move(150, 200)
        self.month.setChecked(True)

        self.day = QtWidgets.QRadioButton("day", self)
        self.day.move(150, 230)

        year_month_day_button_group = QtWidgets.QButtonGroup(self)
        year_month_day_button_group.addButton(self.year)
        year_month_day_button_group.addButton(self.month)
        year_month_day_button_group.addButton(self.day)


        self.cp = QtWidgets.QRadioButton("copy", self)
        self.cp.move(250, 170)
        self.cp.setChecked(True)

        self.mv = QtWidgets.QRadioButton("move", self)
        self.mv.move(250, 200)

        cp_mv_button_group = QtWidgets.QButtonGroup(self)
        cp_mv_button_group.addButton(self.cp)
        cp_mv_button_group.addButton(self.mv)



    """
    toggles all extensions usage checbox
    """
    def extensions_checkox_function(self):
        if(self.extensions_line.isEnabled()):
            self.extensions_line.setEnabled(False)
        else:
            self.extensions_line.setEnabled(True)

    """
    checkox options
    """
    def checkoxes(self):
        self.extensions_checkox = QtWidgets.QCheckBox("all extensions", self)
        self.extensions_checkox.move(10, 95)
        self.extensions_checkox.clicked.connect(self.extensions_checkox_function)
        self.extensions_checkox.setChecked(True)




    """
    gets necessary values from gui converts them for separate function
    """
    def value_collector(self):
        date_source_selection = ""
        cp_or_mv_selection = ""
        day_monty_year_selection = ""
        extensions_list = []
        path_from = ""
        path_to = ""

        are_parameters_ok = True

        if(self.S.isChecked()):
            date_source_selection = "-S"
        elif(self.E.isChecked()):
            date_source_selection = "-E"
        elif(self.ES.isChecked()):
            date_source_selection = "-ES"


        if (self.year.isChecked()):
            day_monty_year_selection = "-y"
        elif (self.month.isChecked()):
            day_monty_year_selection = "-m"
        elif (self.day.isChecked()):
            day_monty_year_selection = "-d"


        if (self.cp.isChecked()):
            cp_or_mv_selection = "-cp"
        elif (self.mv.isChecked()):
            cp_or_mv_selection = "-mv"

        #spilts extensions by comma
        if(self.extensions_checkox.isChecked()):
            extensions_list.append("*")
        else:
            extensions_list = self.extensions_line.text().split(',')

        #checks old directoryes existence
        if (not os.path.isdir(self.old_file_line.text())):
            are_parameters_ok = False
            self.info_label.setText("Directory error! (old)")
        else:
            path_from = self.old_file_line.text()

        #checks if new directory exists but checks only the path if name is not exists it will be created
        new_main_dir_path, new_main_dir_name = os.path.split(self.new_file_line.text())
        if (not os.path.isdir(new_main_dir_path)):
            are_parameters_ok = False
            self.info_label.setText("Directory error! (new)")
        else:
            path_to = self.new_file_line.text()


        return are_parameters_ok, date_source_selection, cp_or_mv_selection, day_monty_year_selection, extensions_list, path_from, path_to



    """
    writes lists to a file
    """
    def write_extra_info_to_file(self, path, file_name, all_files_list, files_with_no_exif_list, changed_file_names_list):
        with open(path + os.sep + file_name + ".txt", 'a', encoding='utf-8') as file:

            # if exif is not selected we should notify
            if (files_with_no_exif_list[0] == "exif_not_selected"):
                exif_count = "exif data not scanned (if you want to get exif information, use with exif option selected)"
            else:
                exif_count = len(files_with_no_exif_list).__str__()

            file.write("--- Content of the file --- \n 1-All files and their old and new directories. Total: " + len(
                all_files_list).__str__()
                       + " \n 2-Files with no exif data. Total: " + exif_count
                       + "\n 3-Files that renamed because of the name collision. Total: " + len(
                changed_file_names_list).__str__())
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
    def seperate(self, date_source_selection, cp_or_mv_selection, day_monty_year_selection, extensions_list, old_main_dir,new_main_dir):

        # -------------------------------------------gating all files from all subdirs--------------------------------------

        #---(FOR GUI)--- give info ---(FOR GUI)---
        self.info_label.setText("collecting directories")

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

            #---(FOR GUI)--- this is for stopping thread if stop button pressed ---(FOR GUI)---
            if (self.stop_thread):
                return


        # printlist(file_paths)

        # ------------------------------copy or move files to apropriate destinations-----------------------------------

        #split new path and name
        new_main_dir_path, new_main_dir_name = os.path.split(new_main_dir)

        #create new folder for puting seperated stuff in
        create_dir_if_not_exists(dir_path=new_main_dir_path, dir_name=new_main_dir_name)

        #status for informatin
        status = 1
        
        #those lists are for report file they are for collecting and displaying extra information in the report file
        changed_file_names_list = []
        files_with_no_exif_list = []
        all_files_list = []

        for file_path in file_paths:

            # ---(FOR GUI)--- this is for stopping thread if stop button pressed ---(FOR GUI)---
            if (self.stop_thread):
                return

            #---(FOR GUI)--- update info label with percentage ---(FOR GUI)---
            self.info_label.setText(len(file_paths).__str__() + "/" + status.__str__() + "   %" + int((status/len(file_paths))*100).__str__())

            #print(len(file_paths).__str__() + "/" + status.__str__() + " -> " + os.path.basename(file_path))
            status += 1

            #these are needed to understand existance ofdates
            is_exif_exists = False
            is_modified_date_exists = False


            #this part tries to get exif date if E or ES option selected
            if (date_source_selection == "-E" or date_source_selection == "-ES"):
                #getting exif date
                date, is_exif_exists = get_date_taken_EXIF(path=file_path)
                #if date exists
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

            #this part gets system provided modify date if S or ES option selected
            if ((date_source_selection == "-S" or date_source_selection == "-ES") and (not is_exif_exists)):
                #getting system date
                date, is_modified_date_exists = get_date_modification_SYSTEM(path=file_path)
                #if date exists
                if (is_modified_date_exists):
                    if (day_monty_year_selection == "-y" or day_monty_year_selection == "-m" or day_monty_year_selection == "-d"):
                        dir_for_copy = create_dir_if_not_exists(dir_path=new_main_dir, dir_name=date[:4])
                        if (day_monty_year_selection == "-m" or day_monty_year_selection == "-d"):
                            dir_for_copy = create_dir_if_not_exists(dir_path=dir_for_copy, dir_name=date[:7])
                            if (day_monty_year_selection == "-d"):
                                dir_for_copy = create_dir_if_not_exists(dir_path=dir_for_copy, dir_name=date[:10])


            #if no date found anywhere dont touch that file
            if (not is_modified_date_exists and not is_exif_exists):
                continue


            #now we have destination path but there can be collision so we check for that and make a rename if needed
            dest, is_name_changed, original_src = check_existace_and_rename(src_path=file_path, dest_path=dir_for_copy)

            #---(FOR report text)--- if name changed append this file to changed_file_names_list ---(FOR report text)---
            if(is_name_changed):
                changed_file_names_list.append(original_src + " -> " + dest)

            #---(FOR report text)--- append every file to all_files_list this will be used in the report text ---(FOR report text)---
            all_files_list.append(original_src + " -> " + dest)

            #copy or move file to destination
            if (cp_or_mv_selection == "-cp"):
                copy_file(src=file_path, dest=dest)
            elif (cp_or_mv_selection == "-mv"):
                move_file(src=file_path, dest=dest)
        
        #---(FOR GUI)--- showing final results on the info label ---(FOR GUI)---
        self.info_label.setText(len(file_paths).__str__() + "/" + (status - 1).__str__() + " see report file for extra info")
        
        #---(FOR report text)--- if exif id not checked at all we need to show it in the report ---(FOR report text)---
        if(date_source_selection == "-S"):
            files_with_no_exif_list.append("exif_not_selected")

        #writing all the extra information to info file
        self.write_extra_info_to_file(new_main_dir, "Report", all_files_list, files_with_no_exif_list, changed_file_names_list)
       
        



if __name__=='__main__':
    app = QtWidgets.QApplication(sys.argv)
    sf = sep_frame()
    sys.exit(app.exec_())