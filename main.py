from aiogram import Bot, Dispatcher, executor, types
import re
import random
import string

API_TOKEN = "token"

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


def check_password_strength(password):
    score = 0
    recommendations = []

    if len(password) >= 12:
        score += 2
    elif len(password) >= 8:
        score += 1
    else:
        recommendations.append("Увеличьте длину пароля до 12 символов или больше.")

    if re.search(r"[A-Z]", password):
        score += 1
    else:
        recommendations.append("Добавьте хотя бы одну заглавную букву.")

    if re.search(r"[a-z]", password):
        score += 1
    else:
        recommendations.append("Добавьте хотя бы одну строчную букву.")

    if re.search(r"[0-9]", password):
        score += 1
    else:
        recommendations.append("Добавьте хотя бы одну цифру.")

    if re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        score += 2
    else:
        recommendations.append("Добавьте специальные символы, например: @, #, $, %.")

    if score >= 7:
        strength = "Надёжный"
    elif 4 <= score < 7:
        strength = "Средний"
    else:
        strength = "Слабый"

    return strength, recommendations


def generate_secure_password(length=12):
    all_characters = string.ascii_letters + string.digits + "!@#$%^&*(),.?\":{}|<>"
    password = ''.join(random.choice(all_characters) for _ in range(length))
    return password


@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    await message.answer(
        "Привет! Я бот для проверки надёжности паролей. Отправь мне свой пароль, и я проверю его силу. "
        "Для генерации надёжного пароля отправь команду /generate."
    )


@dp.message_handler(commands=["generate"])
async def generate_password(message: types.Message):
    secure_password = generate_secure_password()
    await message.answer(f"Вот ваш надёжный пароль: {secure_password}\n"
                         f"Сохраните его в безопасном месте.")


@dp.message_handler()
async def check_password(message: types.Message):
    password = message.text
    strength, recommendations = check_password_strength(password)

    response = f"Пароль: {strength}\n"
    if recommendations:
        response += "Рекомендации по улучшению:\n" + "\n".join(f"- {rec}" for rec in recommendations)

    await message.answer(response)


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
