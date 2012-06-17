# commandDataCubby  VERSION 004
# This program is a command line interface to the functionality contained in the module called
# DataCubby.
# 
# Uses a class called cabinet to handle view, controller, and persistance
# Version 004 is conceived to provide a command line interface to 
# 1. Version 004 of DataCubby, it is substantially different from prior versions due to moving class:Cabinet


import sys
from DataCubby import *



# MAIN


def getChoice(curCub):
    theMenu = '''
    1) Exit
    2) Open a saved Data Cubby Cabinet
    3) Save current Data Cubby Cabinet and Continue
    4) View Sorted List of Cubbies
    5) Enter the incept code of an existing Cubby to Focus on
    6) Edit the Mainfact of the current Cubby
    7) Add a child to the Current Cubby
    8) Edit the data in the user defined fields of the current Cubby
    9) Change user defined fields
    '''
    print theMenu
    print "\n _________The Current Cubby is: _________"
    print "*", curCub, "\n"
    print "*********************************************************************"
    choice = input("\nEnter the number of the action you would like to take from the menu above: ")
    return choice
    print "*********************************************************************"

def main():
    print "\n ************ Welcome to the command line version of DataCubby! ***********\n"
    
    commandCabinet = Cabinet()
    choice = getChoice(commandCabinet.focusCubby)
    while choice != 1:
        if choice == 2:
            cf = input('Enter the File name of the Cubby you want to open: ')
            commandCabinet.rootCubby = commandCabinet.open_cabinet(cf) # prog question: does prior rootCubby and children get garbage collected?
            commandCabinet.focusCubby = commandCabinet.rootCubby
        elif choice == 3:
            df = input('Enter the file name you want to save this Cubby as: ')
            commandCabinet.save_cabinet(commandCabinet.rootCubby, df)
        elif choice == 4:
            print "\n"
            print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
            for g in commandCabinet.flatlist_cubbies(commandCabinet.rootCubby):
                print g
            print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
        elif choice == 5:
            focusName = raw_input("Enter the name of the Cubby you want to Focus on: ") #needs to be enfolded in a try except block
            commandCabinet.focusCubby = commandCabinet.choose_cubby(commandCabinet.rootCubby, int(focusName))
        elif choice == 6:
            mf = raw_input('Enter the main information for the current cubby: ')
            commandCabinet.focusCubby.mainfact = mf
        elif choice == 7:
            cc = raw_input('Enter short one or two word name for the Cubby: ')
            commandCabinet.focusCubby.add_child(cc)
        elif choice == 8:
            commandCabinet.focusCubby.edit_userFieldData()
        elif choice == 9:
	    fldname = raw_input('Enter new field name with no spaces:' )
	    commandCabinet.userFieldsGlobal.append(fldname)
	    commandCabinet.propogate_user_fields(commandCabinet.userFieldsGlobal, commandCabinet.rootCubby) 
        else: 
            print "Invalid choice, try again"
        choice = getChoice(commandCabinet.focusCubby)


    sys.exit()
	    


main()

if __name__ == "__main__":
    main()
