import threading
from recibirCorreo import monitor_inbox

def start_monitoring_thread():
    monitoring_thread = threading.Thread(target=monitor_inbox)
    monitoring_thread.daemon = True  # Permite que el hilo se cierre cuando el programa principal termine
    monitoring_thread.start()

if __name__ == '__main__':
    start_monitoring_thread()
    # Mantén el programa principal corriendo
    while True:
        pass