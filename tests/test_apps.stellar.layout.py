from common import *
from apps.stellar.operations.layout import format_asset_type
from trezor.messages.StellarAssetType import StellarAssetType


class TestStellarLayout(unittest.TestCase):

    def test_format(self):
        m = StellarAssetType()
        m.issuer = unhexlify('0000642466b185b843152e9e219151dbc5892027ec40101a517bed5ca030c2e0')
        m.code = 'USD'
        m.type = 1
        self.assertEqual(format_asset_type(m), 'USD (GAAAA)')

        m = StellarAssetType()
        m.issuer = unhexlify('0000642466b185b843152e9e219151dbc5892027ec40101a517bed5ca030c2e0')
        m.code = 'AAABBBCCCDDD'
        m.type = 2
        self.assertEqual(format_asset_type(m), 'AAABBBCCCDDD (GAAAA)')

        m = StellarAssetType()
        m.issuer = unhexlify('0000642466b185b843152e9e219151dbc5892027ec40101a517bed5ca030c2e0')
        m.code = 'XLM'
        m.type = 0
        self.assertEqual(format_asset_type(m), 'XLM (native asset)')


if __name__ == '__main__':
    unittest.main()
