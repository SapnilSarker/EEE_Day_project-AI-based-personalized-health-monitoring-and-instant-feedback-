import requests
from urllib.parse import quote

def telegram_bot_sendtext(bot_message, friend_chat_id):
    bot_token = '6408347648:AAEdmV3Guchw1fcji3yj2Oc7XbJXoTLGm8I'  # Replace with your bot token
    encoded_message = quote(bot_message)
    
    send_text = f'https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={friend_chat_id}&parse_mode=Markdown&text={encoded_message}'

    try:
        response = requests.post(send_text)
        return response.json()
    except Exception as e:
        print("Error in sending message: ", e)
        return None

# Example usage
friend_chat_id = '01738588238'  # Your friend's chat ID
telegram_bot_sendtext('Hello, how are you?', friend_chat_id)
