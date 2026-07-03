import socket

MODEM_IP = '127.0.0.1'
MODEM_PORT = 8100 # Default for many KISS-over-TCP sound modems

# Establish TCP connection to the modem
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((MODEM_IP, MODEM_PORT))
    
    # Send KISS Command: FEND (0xC0), Command Byte (0x00 for Data), Payload, FEND (0xC0)
    # The payload 'TEST' is a placeholder. AX.25 usually requires headers (e.g., CALLSIGN).
    payload = b'\xc0\x00TEST\xc0'
    s.send(payload)
    
    print("Packet sent to modem!")

except Exception as e:
    print(f"Error: {e}")
finally:
    s.close()
