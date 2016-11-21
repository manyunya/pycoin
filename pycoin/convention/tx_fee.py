
import io
from urllib2 import Request, urlopen, URLError
import json


TX_FEE_PER_THOUSAND_BYTES = 10000


def recommended_fee_for_tx(tx, recommanded_fee = False, default_fpk = "low_fee_per_kb", cap = 100000):
    """
    Return the recommended transaction fee in satoshis.
    This is a grossly simplified version of this function.
    TODO: improve to consider TxOut sizes.
      - whether the transaction contains "dust"
      - whether any outputs are less than 0.001
      - update for bitcoind v0.90 new fee schedule

    default_fpk can be low_fee_per_kb, medium_fee_per_kb, high_fee_per_kb

    cap defines the maximum fee per transaction (default 0.001 BTC)
     this is to prevent high transaction fees due to spam attacks on the network

    """
    s = io.BytesIO()
    tx.stream(s)
    tx_byte_count = len(s.getvalue())
    if recommanded_fee:
        try:
            request = Request('http://api.blockcypher.com/v1/btc/main')
            response = urlopen(request)
            RecomFeeResp = json.loads(response.read())
            TX_FEE_PER_THOUSAND_BYTES = RecomFeeResp.get(default_fpk)
        except URLError, e:
            TX_FEE_PER_THOUSAND_BYTES = 10000

    tx_fee = TX_FEE_PER_THOUSAND_BYTES * ((999+tx_byte_count)//1000)

    if tx_fee > cap:
        return cap

    return tx_fee
