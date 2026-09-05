"""Release resource confidentiality, authenticity and CSV coverage regression."""
import importlib.util
import sys
sys.dont_write_bytecode = True
from pathlib import Path
import tempfile
import unittest
import base64
from cryptography.exceptions import InvalidTag
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

ROOT = Path(__file__).resolve().parents[3]
PROJECT = ROOT / 'templates/game/wuwei'
spec = importlib.util.spec_from_file_location('wuwei_pack', PROJECT / 'tools/pack_data.py')
pack_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pack_module)


class PackTests(unittest.TestCase):
    def test_all_runtime_tables_authenticated(self):
        scratch = ROOT / '_scratch'
        scratch.mkdir(exist_ok=True)
        with tempfile.TemporaryDirectory(prefix='wuwei-pack-test-', dir=scratch) as directory:
            output = Path(directory)
            pack_module.pack(PROJECT / 'data', output)
            expected = {p.name for p in (PROJECT / 'data').glob('*.csv') if p.stem not in pack_module.EXCLUDED_TABLES}
            self.assertEqual({p.name for p in output.glob('*.csv')}, expected)
            self.assertNotIn('source_tables.csv', expected)
            for path in output.glob('*.csv'):
                magic, nonce, ciphertext, tag = path.read_text().split('|')
                self.assertEqual(magic, 'WUW1')
                nonce, ciphertext, tag = [base64.b64decode(v, validate=True) for v in (nonce, ciphertext, tag)]
                plain = AESGCM(pack_module.KEY).decrypt(nonce, ciphertext + tag, pack_module.AAD)
                self.assertEqual(plain, (PROJECT / 'data' / path.name).read_bytes())
                with self.assertRaises(InvalidTag):
                    AESGCM(pack_module.KEY).decrypt(nonce, ciphertext + bytes([tag[0] ^ 1]) + tag[1:], pack_module.AAD)


if __name__ == '__main__':
    unittest.main()
