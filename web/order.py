import requests
import tokens

def from_order_to_text(order):
    text = f'НОВЫЙ ЗАКАЗ!\nИмя: {order["name"].data}\nE-mail: {order["email"].data}\nТелефон: {order["phone"].data}\n\n-------\n\n'
    for product in order['products']:
        text += f'Товар: {product[0]}\nКоличество: {product[1]}\nЦена: {product[0].price}р.\n\n-------\n\n'
    sum_ = sum([item.price * amount for item, amount in order["products"]])
    text += f'Сумма: {sum_}р.'
    return text


def send_telegram(text):
    token = tokens.TOKEN
    url = "https://api.telegram.org/bot"
    channel_id = tokens.CHAT_ID
    url += token
    method = url + "/sendMessage"

    r = requests.post(method, data={
         "chat_id": channel_id,
         "text": text
          })

    if r.status_code != 200:
        pass