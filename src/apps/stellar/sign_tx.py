from apps.common import seed
from apps.stellar.writers import *
from apps.stellar.operations import serialize_op
from apps.stellar import layout
from apps.stellar import consts
from apps.stellar import helpers
from trezor.messages.StellarSignTx import StellarSignTx
from trezor.messages.StellarTxOpRequest import StellarTxOpRequest
from trezor.messages.StellarSignedTx import StellarSignedTx
from trezor.crypto.curve import ed25519
from trezor.crypto.hashlib import sha256
from ubinascii import hexlify

STELLAR_CURVE = 'ed25519'
TX_TYPE = bytearray('\x00\x00\x00\x02')


async def sign_tx_loop(ctx, msg: StellarSignTx):
    signer = sign_tx(msg, msg)
    res = None
    while True:
        req = signer.send(res)
        if isinstance(req, StellarTxOpRequest):
            res = await ctx.call(req, *consts.op_wire_types)
        elif isinstance(req, StellarSignedTx):
            break
        elif isinstance(req, helpers.UiConfirmInit):
            res = await layout.require_confirm_init(ctx, req.pubkey, req.network)
        elif isinstance(req, helpers.UiConfirmMemo):
            res = await layout.require_confirm_memo(ctx, req.memo_type, req.memo_text)
        elif isinstance(req, helpers.UiConfirmFinal):
            res = await layout.require_confirm_final(ctx, req.fee, req.num_operations)
        else:
            raise TypeError('Stellar: Invalid signing instruction')
    return req


async def sign_tx(ctx, msg):

    # serialize

    # confirm init
    await helpers.confirm_init(msg.pubkey, msg.network_passphrase)
    await helpers.confirm_memo(msg.memo_type, msg.memo_text)
    await helpers.confirm_final(msg.fee, msg.num_operations)

    # sign
    # (note that the signature does not include the 4-byte hint since it can be calculated from the public key)
    digest = sha256(w).digest()
    signature = ed25519.sign(node.private_key(), digest)

    # Add the public key for verification that the right account was used for signing
    resp = StellarSignedTx()
    resp.public_key = pubkey
    resp.signature = signature

    yield resp


def node_derive(root, address_n: list):
    node = root.clone()
    node.derive_path(address_n)
    return node
