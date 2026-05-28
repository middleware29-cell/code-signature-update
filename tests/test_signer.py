import unittest
import tempfile
import shutil
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.key_manager import KeyManager
from src.signer import FileSigner
from src.verifier import SignatureVerifier


class TestSigner(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.km = KeyManager(self.test_dir)
        self.private_key, self.public_key = self.km.generate_keypair("test")
        self.signer = FileSigner(self.private_key)
        self.verifier = SignatureVerifier(self.public_key)
        self.test_file = Path(self.test_dir) / "test.txt"
        self.test_file.write_text("Contenu de test")
    
    def tearDown(self):
        shutil.rmtree(self.test_dir)
    
    def test_sign_file_creates_signature(self):
        self.signer.sign_file(self.test_file)
        sig_file = self.test_file.with_suffix(".txt.sig")
        self.assertTrue(sig_file.exists())
    
    def test_verify_valid_signature(self):
        self.signer.sign_file(self.test_file)
        is_valid, message = self.verifier.verify_file(self.test_file)
        self.assertTrue(is_valid)
    
    def test_verify_invalid_signature(self):
        self.signer.sign_file(self.test_file)
        self.test_file.write_text("Contenu modifié")
        is_valid, message = self.verifier.verify_file(self.test_file)
        self.assertFalse(is_valid)
    
    def test_sign_bytes(self):
        data = b"Donnees de test"
        signature = self.signer.sign_bytes(data)
        self.assertIsInstance(signature, str)
        self.assertTrue(len(signature) > 0)


if __name__ == "__main__":
    unittest.main()