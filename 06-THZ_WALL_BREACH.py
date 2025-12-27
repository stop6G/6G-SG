import numpy as np
import time

# ==============================================================================
# CONFIGURATION
# ==============================================================================
ROOM_SIZE = (10, 10)  # 10x10 meter room
SCAN_RESOLUTION = 64  # Points per meter

def scan_room_csi():
    print("[*] Hijacking 6G Pilot Signals for Channel State Information (CSI)...")
    print("[*] Calibrating reflection baseline...")
    time.sleep(1)
    
    # 1. GENERATE FAKE SENSOR DATA
    # In reality, you'd read this from a WiFi card's firmware.
    # Here, we create a matrix of zeros (empty air).
    room_matrix = np.zeros(ROOM_SIZE)
    
    # 2. INSERT HIDDEN TARGETS
    # We simulate a person standing at coordinates (3, 5) and (7, 2)
    # The signal "attenuation" is higher where mass exists.
    room_matrix[3, 5] = 0.9  # Strong reflection (Human)
    room_matrix[7, 2] = 0.8  # Strong reflection (Human)
    
    # Add some noise (simulating furniture/walls)
    noise = np.random.normal(0, 0.1, ROOM_SIZE)
    scan_data = room_matrix + noise

    # 3. RENDER ASCII HEATMAP
    # We interpret the radio waves into visuals
    print("\n--- [ THZ VISUALIZER OUTPUT ] ---")
    for row in scan_data:
        line = ""
        for signal_strength in row:
            if signal_strength > 0.7:
                line += "██"  # Human detected
            elif signal_strength > 0.3:
                line += "░░"  # Ghost/Noise
            else:
                line += "  "  # Empty space
        print(line)
        time.sleep(0.05) # Scan line effect

    print("\n[+] Scan Complete. 2 Biological Targets identified.")

if __name__ == "__main__":
    scan_room_csi()