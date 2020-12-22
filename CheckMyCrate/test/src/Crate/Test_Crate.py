import unittest
from src.Crate.Crate import Crate

class Test_Crate(unittest.TestCase):
    def test_crate___init__(self):
        crate = Crate("test/sample/","test/sample/ro-crate-metadata.json")

        assert(crate.path, "test/sample/")
        assert(crate.json_path, "test/sample/ro-crate-metadata.json")
        assert(crate.maps["$Crate"], "./")

if __name__ == '__main__':
    unittest.main()
