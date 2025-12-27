import time
import struct
# SCAPY is the real library used for packet crafting
from scapy.all import IP, UDP, Raw, send

# CRYPTOGRAPHY is the standard library for real encryption
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os

# ==============================================================================
# CONFIGURATION
# ==============================================================================
TARGET_IP = "192.168.1.1"  # In a story, this would be the 6G Node IP
TARGET_PORT = 62201        # The port the server is silently listening on
MY_ID = "OP_77_ALPHA"      # User ID

# ==============================================================================
# REAL ENCRYPTION (AES-GCM)
# ==============================================================================
def encrypt_payload(message):
    # Real hackers don't roll their own crypto. They use AES.
    # Generate a random 32-byte key (in reality, this key is pre-shared)
    key = os.urandom(32)
    iv = os.urandom(12) # Initialization Vector

    # Encrypt using AES-GCM (Galois/Counter Mode)
    encryptor = Cipher(
        algorithms.AES(key),
        modes.GCM(iv),
        backend=default_backend()
    ).encryptor()

    ciphertext = encryptor.update(message.encode()) + encryptor.finalize()
    
    # Return the raw bytes: IV + Tag + Ciphertext
    return iv + encryptor.tag + ciphertext

# ==============================================================================
# PACKET CONSTRUCTION
# ==============================================================================
def send_ghost_packet():
    print(f"[*] Targeting {TARGET_IP} with Single Packet Authorization...")

    # 1. CREATE PAYLOAD
    # We pack the data into a binary format.
    # Format: Timestamp (8 bytes) + User ID
    timestamp = int(time.time())
    raw_message = f"{timestamp}:{MY_ID}"
    
    print(f"[*] Encrypting payload: {raw_message}")
    encrypted_data = encrypt_payload(raw_message)

    # 2. BUILD THE PACKET LAYERS (The "Scapy" way)
    # Layer 1: IP (Addressing)
    ip_layer = IP(dst=TARGET_IP)
    
    # Layer 2: UDP (Transport)
    # sport=55000 is our source port. dport=62201 is where we knock.
    udp_layer = UDP(sport=55000, dport=TARGET_PORT)
    
    # Layer 3: The Payload
    # This places our encrypted bytes inside the packet.
    payload_layer = Raw(load=encrypted_data)

    # Stack them together using the '/' operator (Scapy syntax)
    full_packet = ip_layer / udp_layer / payload_layer

    # 3. SEND THE PACKET
    # verbose=0 makes it silent (no console output from scapy)
    print(f"[>] Sending {len(full_packet)} bytes via UDP...")
    send(full_packet, verbose=0)
    
    print("[+] Packet sent. If the key was valid, the firewall is now open.")

if __name__ == "__main__":
    send_ghost_packet()