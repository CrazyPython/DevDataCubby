# Module: DataCubby
# Datacubby is generally a module for learning how to code objects used in 
# outlining applications like task managers, and other heirarchical, 
# parent:child data structures
#    


from time import *
import pickle


class Cubby(object):
    """ Basic class containing core parent/child functionality """
    def __init__(self, parentCubby, cubbyName):
        self.incept = time() # timestamp the creation the instance

        # human readable creation date string
        self.creationDate = strftime('%Y %m %d %H %M %S', 
                                    (localtime(self.incept))
                                    )
        
        # same as dictionary key in parent cubby's "children dictionary"
        self.keyname = cubbyName 
       
        # the primary description of the data held in the cubby
        self.slugline = "" 
        
        self.parent = parentCubby # passed in as argument, containment mechanism
        self.children = {} # holds instances of this class created as children
        self.userFields = {} # holds properties universal to all instances

    def add_child(self, cubbykey):
        self.children[cubbykey] = Cubby(self, cubbykey)

    def present_children(self):
        """ 
        Streamlines recursive function calls from client classes 
        that traverse heirarchy. (refactor to be @property?)
        """
        for child in self.children.values():
            yield child

    def reverse_traversal(self):
        """
        Return a list that specifies the path of
        dictionary keys from the root of the heirarchy
        to "self".
        """

        AllAncestors = [self.keyname]
        def masterlist(curCubby):
            AllAncestors.insert(0, curCubby.parent.keyname)
            parentCubby = curCubby.parent
            if parentCubby.parent:
                masterlist(parentCubby)

        masterlist(self)
        return AllAncestors

    def change_parent(self, candidate, validlist):
        """ tests to be sure target parent exists before allowing change """
        # this needs to move to the cabinet class, 
        # and made into 2 ops, 'prune' and 'graft'

        if candidate in validlist:
            self.parent = candidate
            return parent()
        else:
            return "Invalid Parent, No change in parent cubby!"  
        # this needs to be turned into a try/except block

    def conform_userFields(self, masterList):
        """
        Conforms the keys for the self.userfield names to the list 
        common to all cubbies in file, retaining any stored values 
        by building copy before altering.
        Client class object, notably Cabinet, calls this method when
        the masterlist held as an attribute of that class is altered.
        """
        conformedFields = dict.fromkeys(masterList)
        oldUserData = self.userFields.copy() 
        conformedFields.update(oldUserData)
        self.userFields.clear() 
            # add a condition that tests to see if some 
            # prior keys and values will be deleted, 
            # offer user chance to change mind
        self.userFields = conformedFields.copy() 

    def edit_userFieldData():
        """ This method intended as prescribed means for 
        the user to change the values held in the User Defined Fields.
        self.userfields
        """
        pass

    def sum_customfield(self, fldname):
        sum = 0
        x = self.children.values()
        for y in x:
            print y.userFields[fldname]
            sum += y.userFields[fldname]
        return sum



    def __str__(self):
        rep = "NAME: " + str(self.keyname) +  " | TIMESTAMP: " + str(self.creationDate) + " | CubbyId: " + str(id(self))
        if self.children:
            rep += " **has children**"
        rep += "\n slugline: " + self.slugline + "\n"
        if self.userFields:
            for key in self.userFields:
                rep += " |" + str(key) + ": " +  str(self.userFields.get(key, "n/a"))
        return rep



class Cabinet(object):
    def __init__(self):
        """
        Instantiate an empty Root Cubby to graft new or unpickled cubbies onto, 
        and a catalog to hold/serialize all children.  Develop to be Singleton 
        """
        self.rootCubby = Cubby( 'Root', 'Root')
        self.focusCubby = self.rootCubby # this cubby is used as the cursor
        self.userFieldsGlobal = [] # List of user defined Field Names. 

    def open_cabinet(self, filename):
        """
        persistence mechanism for loading from file object. 
        Is set up to potentially allow grafting
        """
        file = open(filename, 'rb')
        loadCubby = pickle.load(file)
        file.close()
        return loadCubby

    def save_cabinet(self, curCub, filename):
        filename = filename +".cby"
        file = open(filename, 'wb')
        pickle.dump(curCub, file, -1)
        file.close()

    def flatlist_cubbies(self, someCubby):
        """
        This function stores all the cubbies in a flattened list object 
        sorted by parent cubby.
        """
        AllDescendents = []
        def masterlist(curCubby):
            AllDescendents.append(curCubby)
            if curCubby.children:
                for x in curCubby.present_children:
                    masterlist(x)

        masterlist(someCubby)

        return AllDescendents


    def choose_cubby(self, someCubby, IDsearch):
        """
        traverses the branch of cubbys starting with the cubby 
        passed as an argument to match the choice incept code
        """
        candidates = self.flatlist_cubbies(someCubby)
	try:

	    for x in candidates: 
		if id(x) == IDsearch:
		    chosen = x
		else:
		    chosen = None
	    return chosen

	except:
	    pass

    def find_cubby(self):
        """ uses regex etc. to choose a cubby based on search criteria """
        pass

    def propogate_user_fields(self, usrfields, curCub):
        """
        Conforms all of the child cubby nodes of the calling object 
        to the same user field names.
        """
        for each in curCub.present_children():
            each.conform_userFields(usrfields)
            self.propogate_user_fields(usrfields, each)


# TestSuite

def test():
    """
    Temporary Idle/ IDE  Function to create root test object during 
    module development
    """
    sandbox = Cabinet()
    sandbox.userFieldsGlobal.append('Cost Est')
    sandbox.propogate_user_fields(sandbox.userFieldsGlobal, sandbox.rootCubby)
    sandbox.rootCubby.slugline = "This is the Test Suite Generated main fact for the root cubby of sandbox."
    sandbox.rootCubby.userFields['Cost Est'] = 20 
    print sandbox.rootCubby
    sandbox.userFieldsGlobal.append('Cost Actual')
    sandbox.propogate_user_fields(sandbox.userFieldsGlobal, sandbox.rootCubby)
    sandbox.rootCubby.userFields['Cost Actual'] = 19
    print sandbox.rootCubby
    print sandbox.focusCubby
    sandbox.rootCubby.add_child('Fruits')
    sandbox.rootCubby.add_child('Vegetables')
    sandbox.rootCubby.add_child('Cheeses')
    sandbox.rootCubby.children['Cheeses'].add_child('swiss')
    sandbox.rootCubby.children['Cheeses'].add_child('cheddar')
    sandbox.rootCubby.children['Cheeses'].add_child('jack')
    sandbox.rootCubby.children['Fruits'].add_child('apple')
    sandbox.rootCubby.children['Fruits'].add_child('pear')
    sandbox.rootCubby.children['Fruits'].add_child('grape')
    sandbox.rootCubby.children['Fruits'].children['apple'].add_child('granny')
    sandbox.propogate_user_fields(sandbox.userFieldsGlobal, sandbox.rootCubby)
    for x in sandbox.rootCubby.present_children: print x
    print "flat list test"
    for y in sandbox.flatlist_cubbies(sandbox.rootCubby) : print y
    print "subtotal tests"
    sandbox.rootCubby.children['Fruits'].children['apple']. \
        userFields['Cost Actual'] = 10
    sandbox.rootCubby.children['Fruits'].children['pear']. \
        userFields['Cost Actual'] = 14
    sandbox.rootCubby.children['Fruits'].children['grape']. \
        userFields['Cost Actual'] = 13
    sandbox.rootCubby.children['Cheeses'].children['swiss']. \
        userFields['Cost Actual'] = 10
    sandbox.rootCubby.children['Cheeses'].children['cheddar']. \
        userFields['Cost Actual'] = 12
    sandbox.rootCubby.children['Cheeses'].children['jack']. \
        userFields['Cost Actual'] = 11
    s = sandbox.rootCubby.children['Fruits'].sum_customfield('Cost Actual')
    print s
    #q = sandbox.rootCubby.children['Cheeses'].userFields['Cost Actual'] 
    #foo = sandbox.rootCubby.children['Cheeses'].sum_customfield('Cost Actual')
    print q
    for y in sandbox.flatlist_cubbies(sandbox.rootCubby): print y    
    sandbox.save_cabinet(sandbox.rootCubby, 'Playground')
    return sandbox




# MAIN

if __name__ == "__main__":
    print "This is a module with classes for managing heirarchical data."
    print "if called as main, will generate a test suite with print output"
    test()

