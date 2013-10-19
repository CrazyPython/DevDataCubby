import unittest
from DataCubby import Cubby, Cabinet

class TestCubby(unittest.TestCase):

    
    def setUp(self):
        self.trunk = Cubby(None, 'trunk')

    def test_add_child(self):
        self.trunk.add_child('Fruits')
        self.assertEqual(('trunk', 'Fruits'),
                         (self.trunk.children['Fruits'].parent.keyname,
                          self.trunk.children['Fruits'].keyname))

    def test_present_children(self):
        self.trunk.add_child('Vegetables')
        self.trunk.add_child('Cheeses')
        x = self.trunk.present_children()
        self.assertIn(x.next().keyname, ['Fruits', 'Vegetables', 'Cheeses'])

    def test_reverse_traversal(self):
        self.trunk.add_child('Vegetables')
        self.trunk.children['Vegetables'].add_child('Potatoes')
        self.trunk.children['Vegetables'].children['Potatoes'].add_child('Russet')
        cursor = self.trunk.children['Vegetables'].children['Potatoes'].children['Russet']
        p = cursor.reverse_traversal()
        self.assertEqual(['trunk', 'Vegetables', 'Potatoes', 'Russet'], p)
       
class TestCabinet(unittest.TestCase):

    def setUp(self):
        self.sandbox = Cabinet()

    def test_Cabinet_init_with_rootCubby(self):
        """
        make sure the cabinet is created with a rootcubby, which won't have a parent,
        therefore it is initialized with the string 'root'
        """
        self.sandbox.rootCubby.mainfact = 'test suite generated rootfact'
        self.assertEqual('test suite generated rootfact', self.sandbox.rootCubby.mainfact)
        self.assertEqual('Root', self.sandbox.rootCubby.parent)
        self.assertEqual([], self.sandbox.userFieldsGlobal)
        






    
if __name__ == "__main__":
    unittest.main()
