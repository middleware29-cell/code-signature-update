import unittest
import tempfile
import shutil
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.key_manager import KeyManager
from src.signer import FileSigner
from src.verifier import SignatureVerifier
from src.attack_simulator import AttackSimulator


class TestAttack(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.km = KeyManager(self.test_dir)
        self.private_key, self.public_key = self.km.generate_keypair("test")
        self.signer = FileSigner(self.private_key)
        self.verifier = SignatureVerifier(self.public_key)
        
        self.test_file = Path(self.test_dir) / "victim.py"
        self.test_file.write_text("print('Application legitime')")
        self.signer.sign_file(self.test_file)
        
        self.attack_sim = AttackSimulator(self.verifier)
    
    def tearDown(self):
        shutil.rmtree(self.test_dir)
    
    def test_detect_file_modification(self):
        """Test détection de modification de fichier"""
        result = self.attack_sim.simulate_file_modification(self.test_file)
        self.assertTrue(result['detected'])
    
    def test_detect_signature_replacement(self):
        """Test détection de remplacement de signature"""
        sig_file = self.test_file.with_suffix(".py.sig")
        result = self.attack_sim.simulate_signature_replacement(self.test_file, sig_file)
        self.assertTrue(result['detected'])
    
    def test_run_all_attacks(self):
        """Test exécution de toutes les attaques"""
        results = self.attack_sim.run_all_attacks(self.test_file)
        self.assertEqual(results['total_attacks'], 3)
        self.assertEqual(results['detected'], 3)


if __name__ == "__main__":
    unittest.main()