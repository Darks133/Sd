from instagrapi import Client
import time

# Configurar la API
cl = Client()

# Iniciar sesión
cl.login('user_spoof600', 'Cuenta-000-1')

# Ruta de la imagen que quieres enviar
image_path = "ios.png"

# Función para enviar un mensaje con el menú y la foto
def send_menu_with_image(chat_id):
    menu_text = """🔸 **Bienvenido al bot** 🔸

Selecciona una de las siguientes opciones:

1️⃣ Opción 1: Información general
2️⃣ Opción 2: Ayuda
3️⃣ Opción 3: Contactar soporte

Escribe el número de la opción que deseas seleccionar."""
    
    # Enviar la imagen con el mensaje
    cl.direct_send(menu_text, threads=[chat_id], media=image_path)

# Función para escuchar mensajes en los chats
def listen_for_messages():
    print("Escuchando nuevos mensajes...")
    while True:
        # Obtener todos los hilos de conversación (chats)
        threads = cl.direct_threads()
        for thread in threads:
            thread_id = thread.id
            messages = thread.messages
            for message in messages:
                if message.text == ".menu":  # Si el mensaje es ".menu"
                    print(f"Comando '.menu' detectado en el chat {thread_id}")
                    send_menu_with_image(thread_id)  # Responde con el menú y la imagen
        time.sleep(5)  # Revisa cada 5 segundos nuevos mensajes

# Llamar a la función para escuchar mensajes
listen_for_messages()
