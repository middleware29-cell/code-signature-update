import unittest
import tempfile
import shutil
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.key_manager import KeyManager
from src.signer import FileSigner
from src.verifier import SignatureVerifier


class TestVerifier(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.km = KeyManager(self.test_dir)
        self.private_key, self.public_key = self.km.generate_keypair("test")
        self.signer = FileSigner(self.private_key)
        self.verifier = SignatureVerifier(self.public_key)
        self.test_file = Path(self.test_dir) / "app.py"
        self.test_file.write_text("print('Hello')")
        self.signer.sign_file(self.test_file)
    
    def tearDown(self):
        shutil.rmtree(self.test_dir)
    
    def test_verify_update_package_valid(self):
        result = self.verifier.verify_update_package(self.test_file)
        self.assertTrue(result)
    
    def test_missing_signature(self):
        file3 = Path(self.test_dir) / "nosig.py"
        file3.write_text("print('No signature')")
        is_valid, message = self.verifier.verify_file(file3)
        self.assertFalse(is_valid)


if __name__ == "__main__":
    unittest.main()