import struct

# KISS Protocol Constants
FEND = 0xC0
FESC = 0xDB
TFEND = 0xDC
TFESC = 0xDD
CMD_DATA = 0x00

# AX.25 Constants
PID_NOLAYER3 = 0xF0
CONTROL_UI = 0x03

def encode_callsign(callsign, ssid=0, is_last=False):
    """Encodes a callsign and SSID into the 7-byte AX.25 address format."""
    # Pad callsign to 6 chars with spaces
    callsign = callsign.upper().ljust(6)
    
    # Shift ASCII chars left by 1 bit
    encoded_bytes = [ord(c) << 1 for c in callsign]
    
    # Last byte: SSID (shifted), extension bit (bit 0), and last address bit (bit 7)
    ssid_byte = (ssid & 0x0F) << 1
    if is_last:
        ssid_byte |= 0x01  # Set bit 0 (End of Address indicator)
    encoded_bytes.append(ssid_byte)
    
    return bytes(encoded_bytes)

def calculate_crc(data):
    """Calculates the CRC-16-CCITT for AX.25."""
    crc = 0xFFFF
    for byte in data:
        crc ^= byte << 8
        for _ in range(8):
            if crc & 0x8000:
                crc = (crc << 1) ^ 0x1021
            else:
                crc = crc << 1
    crc = crc ^ 0xFFFF
    # Return little-endian
    return struct.pack('<H', crc & 0xFFFF)

def hdlc_stuffing(data):
    """Applies HDLC bit-stuffing principles (in this context: escaped for KISS)."""
    stuffed = bytearray()
    for byte in data:
        if byte == FEND:
            stuffed.extend([FESC, TFEND])
        elif byte == FESC:
            stuffed.extend([FESC, TFESC])
        else:
            stuffed.append(byte)
    return stuffed

def build_ax25_frame(source, dest, info, dest_ssid=0, src_ssid=0):
    """Builds the raw AX.25 frame bytes."""
    # 1. Address Field (Dest + Src)
    address_field = bytearray()
    address_field.extend(encode_callsign(dest, dest_ssid, is_last=False))
    address_field.extend(encode_callsign(source, src_ssid, is_last=True))
    
    # 2. Control and PID fields
    control_field = bytes([CONTROL_UI])
    pid_field = bytes([PID_NOLAYER3])
    
    # Combine into full frame
    frame = address_field + control_field + pid_field + info
    
    # 3. Append Frame Check Sequence (FCS)
    fcs = calculate_crc(frame)
    return frame + fcs

def encode_kiss_frame(ax25_data, port=0):
    """Encodes AX.25 frame into a KISS frame packet."""
    # KISS command byte (Port 0, Command 0)
    cmd_byte = (port & 0x0F) << 4 | CMD_DATA
    
    # Assemble packet payload
    packet = bytearray([cmd_byte]) + ax25_data
    
    # Escape bytes and wrap in FEND
    stuffed_packet = hdlc_stuffing(packet)
    
    kiss_frame = bytearray([FEND])
    kiss_frame.extend(stuffed_packet)
    kiss_frame.append(FEND)
    
    return bytes(kiss_frame)

if __name__ == "__main__":
    # Example values
    SRC_CALL = "NOCALL"
    DEST_CALL = "APRS"
    MESSAGE = b"TEST-123"
    
    # 1. Construct AX.25 Frame
    ax25_frame = build_ax25_frame(
        source=SRC_CALL,
        dest=DEST_CALL,
        info=MESSAGE,
        dest_ssid=0,
        src_ssid=0
    )
    
    # 2. Encode into KISS format
    kiss_packet = encode_kiss_frame(ax25_frame, port=0)
    
    print(f"AX.25 Frame (Hex): {ax25_frame.hex().upper()}")
    print(f"KISS Frame (Hex):  {kiss_packet.hex().upper()}")
