from PIL import Image, ImageColor
import webcolors
import re
from telegram.ext import Updater, CallbackContext, MessageHandler, CallbackQueryHandler, Filters, CommandHandler
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
import os
import pickle
import random


def closest_colour(requested_colour):
    min_colours = {}
    for key, name in webcolors.CSS3_HEX_TO_NAMES.items():
        r_c, g_c, b_c = webcolors.hex_to_rgb(key)
        rd = (r_c - requested_colour[0]) ** 2
        gd = (g_c - requested_colour[1]) ** 2
        bd = (b_c - requested_colour[2]) ** 2
        min_colours[(rd + gd + bd)] = name
    return min_colours[min(min_colours.keys())]


def get_colour_name(requested_colour):
    try:
        closest_name = actual_name = webcolors.rgb_to_name(requested_colour)
    except ValueError:
        closest_name = closest_colour(requested_colour)
        actual_name = None
    return actual_name, closest_name


def most_frequent_colour(image):
    w, h = image.size
    pixels = image.getcolors(w * h)

    most_frequent_pixel = pixels[0]

    for count, colour in pixels:
        if count > most_frequent_pixel[0]:
            most_frequent_pixel = (count, colour)

    return most_frequent_pixel


def get_clean_color(color):
    pattern_list = ['blue', 'green', 'red', 'orange', 'yellow', 'violet', 'brown', 'black', 'white']

    for pattern in pattern_list:

        match = re.search(pattern, color)
        if match:
            return color[match.span()[0]:match.span()[1]]

    return "no_match"



def get_color(image_path: str):
    actual_name, closer_name = get_colour_name(most_frequent_colour(Image.open(image_path))[1])
    if actual_name:
        return get_clean_color(actual_name)
    else:
        return get_clean_color(closer_name)


def get_route_by_color(color):
    color_dict = {
        'blue': 1,
        'green': 3,
        'red': 4,
        'orange': 5,
        'yellow': 8,
        'violet': -1,
        'brown': -1,
        'black': -1,
        'white': -1
    }
    if not color:
        color = random.randint(1,10)
    model = pickle.load(open('prod/finalized_model.sav', 'rb'))
    route = random.choice(str(model.predict([[color_dict[color]]])).split('.'))
    return route


def send_route(update: Update, context: CallbackContext, image_name):
    comment_dict = {
        'blue': 'У Вас преобладает синий цвет. Синий символизирует спокойствие и удовлетворенность. Рекомендуемый релаксационный маршрут:',
        'green': 'У Вас преобладает зелёный цвет. Зелёный  символизирует чувство уверенности, настойчивость, иногда упрямство. Рекомендуемый релаксационный маршрут:',
        'red': 'У Вас преобладает красный цвет. Красный символизирует силу волевого усилия, агрессивность, наступательные тенденции, возбуждение. Рекомендуемый релаксационный маршрут:',
        'orange': 'У Вас преобладает оранжевый цвет. Оранжевый символизирует силу волевого усилия, агрессивность, наступательные тенденции, возбуждение. Рекомендуемый релаксационный маршрут:',
        'yellow': 'У Вас преобладает желтый цвет. Желтый символизирует активность, стремление к общению, экспансивность, веселость. Рекомендуемый релаксационный маршрут:',
        'violet': 'У Вас преобладает фиолетовый цвет. Фиолетовый символизирует негативные тенденции: тревожность, стресс, переживание страха, огорчения. Рекомендуемый релаксационный маршрут:',
        'brown': 'У Вас преобладает коричневый цвет. Коричневый символизирует негативные тенденции: тревожность, стресс, переживание страха, огорчения. Рекомендуемый релаксационный маршрут:',
        'black': 'У Вас преобладает черный цвет. Черный символизирует негативные тенденции: тревожность, стресс, переживание страха, огорчения. Рекомендуемый релаксационный маршрут:',
        'white': 'У Вас преобладает белый цвет. Белый символизирует негативные тенденции: тревожность, стресс, переживание страха, огорчения. Рекомендуемый релаксационный маршрут:'
    }




    color = get_color(image_name)

    if color == "no_match":
        route = get_route_by_color("blue")
        context.bot.send_sticker(update.message.chat.id, open(f'stickers/blue.tgs', 'rb'))
        context.bot.send_message(update.message.chat.id, "Извините, но у нас нет маргрута для вашего цвета(\nНо знаете, у нас есть рекомендации под люое настроени! Вот они:")
        context.bot.send_message(update.message.chat.id, route[2:])
    else:

        route = get_route_by_color(color)

        context.bot.send_sticker(update.message.chat.id, open(f'stickers/{color}.tgs','rb'))
        context.bot.send_message(update.message.chat.id, comment_dict[color])



        context.bot.send_message(update.message.chat.id, route[2:])
    context.bot.send_message(update.message.chat.id, "Если у тебя изменилось настроение, закрась картинку снова и отправь мне!\nА если ты хочешь начать сначала и получить шаблон нажми /start")

    os.remove(image_name)
