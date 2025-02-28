import network
import urequests
import utime
import machine

# ----------- Configuración WiFi -----------
SSID = "Depto4&5"
PASSWORD = "22360656"

# ----------- Configuración ThingSpeak -----------
THINGSPEAK_API_KEY = "DMNMMZ9NEI8S23PP"  # Reemplaza con tu API key de ThingSpeak
THINGSPEAK_URL = "https://api.thingspeak.com/update"

# ----------- Configuración de pines y ADC -----------
# Ajusta el pin ADC según tu placa (ej. 26, 27, 28 en Raspberry Pi Pico)
adc = machine.ADC(26)

# ----------- Funciones -----------

def conectar_wifi():
    """
    Conecta a la red WiFi usando las credenciales SSID y PASSWORD.
    """
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(SSID, PASSWORD)
    
    print("Conectando a WiFi...")
    while not wlan.isconnected():
        utime.sleep(1)
    print("Conectado. Dirección IP:", wlan.ifconfig()[0])

def leer_temperatura():
    """
    Lee el valor del ADC y lo convierte a temperatura en grados Celsius
    asumiendo un LM35 (10mV/°C).
    """
    valor_adc = adc.read_u16()              # Lectura de 16 bits (0-65535)
    voltaje = (valor_adc / 65535) * 3.3     # Convertir a voltios
    temperatura_c = voltaje * 100           # LM35 entrega 10mV/°C => voltaje*100 = °C
    return temperatura_c

def enviar_a_thingspeak(temperatura):
    """
    Envía el valor de 'temperatura' a ThingSpeak mediante una petición HTTP GET.
    """
    try:
        url = f"{THINGSPEAK_URL}?api_key={THINGSPEAK_API_KEY}&field1={temperatura}"
        respuesta = urequests.get(url)
        print("Respuesta de ThingSpeak:", respuesta.text)
        respuesta.close()
    except Exception as e:
        print("Error al enviar datos:", str(e))

# ----------- Programa principal -----------
def main():
    # 1) Conectar a WiFi
    conectar_wifi()

    # Bucle infinito para leer y enviar temperatura cada 180 segundos
    while True:
        # 2) Leer la temperatura en °C
        temperatura = leer_temperatura()
        
        # 3) Mostrar la temperatura en consola
        print("Temperatura medida (°C):", temperatura)
        
        # 4) Enviar datos a ThingSpeak
        enviar_a_thingspeak(temperatura)
        
        # 5) Esperar 180 segundos antes de la próxima medición
        utime.sleep(180)

# Ejecutar el programa principal
if __name__ == "__main__":
    main()
