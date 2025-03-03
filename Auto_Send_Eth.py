from web3 import Web3

# 🔹 Masukkan API Key Infura
INFURA_URL = "https://mainnet.infura.io/v3/YOUR_INFURA_PROJECT_ID"
web3 = Web3(Web3.HTTPProvider(INFURA_URL))

# 🔹 Masukkan Private Key Pengirim
PRIVATE_KEY = "YOUR_PRIVATE_KEY"  # Jangan bagikan private key ini!
SENDER_ADDRESS = web3.eth.account.from_key(PRIVATE_KEY).address

# 🔹 Daftar alamat penerima & jumlah ETH yang dikirim
RECIPIENTS = [
    {"address": "0xRecipientAddress1", "amount": 0.01},  # Kirim 0.01 ETH
    {"address": "0xRecipientAddress2", "amount": 0.005}, # Kirim 0.005 ETH
    {"address": "0xRecipientAddress3", "amount": 0.02},  # Kirim 0.02 ETH
]

# 🔹 Fungsi untuk mengirim ETH ke banyak alamat
def send_eth_multiple():
    if not web3.is_connected():
        print("❌ Gagal terhubung ke Ethereum. Cek API Key Infura!")
        return
    
    # 🔹 Cek saldo pengirim
    balance = web3.eth.get_balance(SENDER_ADDRESS)
    balance_eth = web3.from_wei(balance, 'ether')
    print(f"💰 Saldo Pengirim: {balance_eth} ETH")

    # 🔹 Ambil nonce awal
    nonce = web3.eth.get_transaction_count(SENDER_ADDRESS, "pending")

    for recipient in RECIPIENTS:
        to_address = recipient["address"]
        amount_eth = recipient["amount"]
        amount_wei = web3.to_wei(amount_eth, 'ether')

        # 🔹 Cek apakah saldo cukup
        if amount_wei > balance:
            print(f"⚠️ Saldo tidak cukup untuk mengirim {amount_eth} ETH ke {to_address}")
            continue

        # 🔹 Konfigurasi transaksi
        tx = {
            'nonce': nonce,
            'to': to_address,
            'value': amount_wei,
            'gas': 21000,  # Gas untuk transfer ETH
            'gasPrice': web3.to_wei(50, 'gwei'),  # Sesuaikan dengan kondisi jaringan
            'chainId': 1  # Ethereum Mainnet
        }

        # 🔹 Tanda tangani transaksi
        signed_tx = web3.eth.account.sign_transaction(tx, PRIVATE_KEY)

        # 🔹 Kirim transaksi ke jaringan
        tx_hash = web3.eth.send_raw_transaction(signed_tx.raw_transaction)
        print(f"✅ Transaksi ke {to_address} berhasil! Hash: {web3.to_hex(tx_hash)}")

        # 🔹 Tambah nonce untuk transaksi berikutnya
        nonce += 1  

        # 🔹 Perbarui saldo
        balance -= (amount_wei + tx["gas"] * tx["gasPrice"])

# 🔥 Jalankan fungsi pengiriman ETH
send_eth_multiple()
