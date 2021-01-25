import unittest
from src.Crate.Crate import Crate

class Test_Crate(unittest.TestCase):
    def test_crate___init__(self):
        crate = Crate("test/sample")

        self.assertEquals(crate.path, "test/sample")
        self.assertEquals(crate.json_path, "test/sample/ro-crate-metadata.json")
        self.assertEquals(crate.maps["$Crate"].id , crate.graph["ro-crate-metadata.json"]["about"]["@id"])

if __name__ == '__main__':
    unittest.main()
