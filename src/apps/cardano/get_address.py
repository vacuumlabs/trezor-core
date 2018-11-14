from trezor import log, wire
from trezor.crypto import bip32
from trezor.messages.CardanoAddress import CardanoAddress

from .address import derive_address_and_node

from apps.common import seed, storage
from apps.common.layout import address_n_to_str, show_address, show_qr


async def get_address(ctx, msg):
    mnemonic = storage.get_mnemonic()
    passphrase = await seed._get_cached_passphrase(ctx)
    root_node = bip32.from_mnemonic_cardano(mnemonic, passphrase)

    try:
        address, _ = derive_address_and_node(root_node, msg.address_n)
    except ValueError as e:
        if __debug__:
            log.exception(__name__, e)
        raise wire.ProcessError("Deriving address failed")
    mnemonic = None
    root_node = None
    if msg.show_display:
        desc = address_n_to_str(msg.address_n)
        while True:
            if await show_address(ctx, address, desc=desc):
                break
            if await show_qr(ctx, address, desc=desc):
                break

    return CardanoAddress(address=address)
