import serial
import time
import struct
from collections import deque

PORT = "/dev/ttyUSB1"
BAUDRATE = 115200
TIMEOUT = 1

CPM_TO_USVH = 153.0  # costante GQ per SBM-20
WINDOW_SIZE = 10  # numero di campioni per la media

def send_cmd(ser, cmd, resp_len=0, is_ascii=False):
    """
    Invia comando RFC1801 al GMC e legge risposta.
    - cmd: stringa comando (es. 'GETVER')
    - resp_len: numero di byte attesi (0 = nessuna lettura)
    - is_ascii: se True decodifica in ASCII
    """
    ser.reset_input_buffer()
    packet = f"<{cmd}>>".encode("ascii")
    ser.write(packet)
    time.sleep(0.1)

    if resp_len <= 0:
        return None

    data = ser.read(resp_len)
    if not data or len(data) < resp_len:
        return None

    return data.decode("ascii", errors="ignore").strip() if is_ascii else data

def read_variable_ascii(ser, cmd, timeout=1.0):
    """
    Per comandi RFC1801 che ritornano ASCII di lunghezza variabile,
    leggiamo fino a timeout o fino a '>>' (indicatore di fine pacchetto).
    """
    ser.reset_input_buffer()
    ser.write(f"<{cmd}>>".encode("ascii"))
    deadline = time.time() + timeout
    buffer = b""
    while time.time() < deadline:
        chunk = ser.read(1)
        if chunk:
            buffer += chunk
        else:
            break
    return buffer.decode("ascii", errors="ignore").strip()

def main():
    ser = serial.Serial(PORT, BAUDRATE, timeout=TIMEOUT)
    try:
        print(f"Connesso a {PORT} @ {BAUDRATE}")
        time.sleep(0.5)

        # --- DISATTIVA HEARTBEAT ---
        print("Disabilito heartbeat (HEARTBEAT0)")
        send_cmd(ser, "HEARTBEAT0")

        # --- VERSIONE ASCII ---
        version = read_variable_ascii(ser, "GETVER", timeout=1.5)
        print("Versione:", version if version else "<nessuna risposta>")

        print("\nInizio lettura continua (Ctrl+C per uscire)...\n")

        # --- LOOP CONTINUO ---
        while True:
            # --- CPM (4 byte big endian) ---
            raw_cpm = send_cmd(ser, "GETCPM", resp_len=4)
            if raw_cpm:
                cpm = struct.unpack(">I", raw_cpm)[0]
                # µSv/h CALCOLATO
                usvh = round(cpm / CPM_TO_USVH, 4)
                print(f"CPM: {cpm} | µSv/h: {usvh}")
            else:
                print("CPM: nessuna risposta")

            time.sleep(1)  # Leggi ogni secondo

    except KeyboardInterrupt:
        print("\nInterrotto dall'utente")
    finally:
        ser.close()
        print("Porta seriale chiusa")

if __name__ == "__main__":
    main()
