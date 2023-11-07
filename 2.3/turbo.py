import time
import copy
import re
import datetime
import discord
import openai
import requests
import BingImageCreator

VERSION = "2.3"

print(f"Wersja {VERSION}")
print("Wersja z 7 listopada 2023")

OPENAIAPIKEY = "sk-EBELEgGQoAl5Czm5BFVxT3BlbkFJpIOSzKvL5E"
DISCORDTOKEN = 'MTEwMzMxNDEwMDg0ODY5NzM5NQ.Gpa4_P.8GA-9-mNechsER0RoMYmKnHYa9cF'
# BINGAPIKEY = "1RyTnuvfpTRQyOg1ih4Dg7u0U9PkRNKVXkW87pKjw6hT9Gq-jEiEJJpvYbGfM78Rmm5R5kB64ArgUHdsUOX1lD38cxuQJZ10k7AX_CmGU8397teGg3VbEsZmkTAZxcz9jYBmXpCHgV0DOAVNlg9T606R_o5Px2gufzLm8WbcbEYsiMnGvuyAsCSN_FJFgeYJM1S4xkl2Z2v7yV9J8-hikPhSK_rf4SI-M8"
BINGAPIKEYLIST = []
AUTHKEYOPERIONA = ""

with open("turbo_keys.txt", "r", encoding="utf-8") as f:
    temp = f.read()
    temp = temp.split("\n")
    OPENAIAPIKEY = temp[0]
    DISCORDTOKEN = temp[1]
    # BINGAPIKEY = temp[2]

OPENAIAPIKEY += input("Extend the OPENAIAPIKEY: ")
DISCORDTOKEN += input("Extend the DISCORDTOKEN: ")
# BINGAPIKEY += input("Extend the BINGAPIKEY: ")


openai.api_key = OPENAIAPIKEY
ostatia_wiadomosc = datetime.datetime.now()

users = [
    "indy (also known as indyrefentyzm or Natalka) should be depicted as a young woman with black long hair. She always dresses in black, wears tights, and a coat. Her main color scheme is black. Draw her in a realistic style.",
    "Ryż (also known as Ola) is a cute girl that is really into anime. She wears skirts, knee-socks, and a cute top. Her favorite color is pink. Draw her in a colorful anime style.",
    "Eryk (also known as Eryk Roch, or Eryk Groch) is an investor from Warsaw. Draw him as a rich, handsome, confident male in a realistic style. He likes money and investments. His theme color is brown.",

]

historia = []


def remove_non_latin_letters(string: str):
    # Define the valid characters as a set
    valid_chars = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_")
    # Initialize an empty list to store the filtered characters
    filtered_chars = []
    # Loop through each character in the string
    for char in string:
        # If the character is in the valid set, append it to the filtered list
        if char in valid_chars:
            filtered_chars.append(char)
    # Join the filtered list into a new string and return it
    return "".join(filtered_chars)


def remove_tag(string: str) -> str:
    # define the tag to be removed
    tag = "<@1103314100848697395>"
    # replace the tag with an empty string
    new_string = string.replace(tag, "")
    # return the new string
    return new_string


def get_user_data(user_id, token):
    headers = {
        "Authorization": token,
        "Content-Type": "application/json"
    }
    response = requests.get(f"https://discord.com/api/users/{user_id}", headers=headers)
    user = response.json()
    return user


def replace_tag_with_username(message):
    message = message.replace("<@664865606654230569>", "indy")
    message = message.replace("<@563811714420834307>", "Ryż")
    message = message.replace("<@489526607573286943>", "Eryk Groch")
    message = message.replace("<@1030361935373418548>", "Bożydar")
    message = message.replace("<@664902875301806117>", "cyryl")
    # Tworzymy wzorzec regularny do wyszukiwania tagów discorda
    pattern = r"<@(\d+)>"
    # Szukamy wszystkich tagów w wiadomości
    matches = re.findall(pattern, message)
    # Dla każdego znalezionego tagu
    for match in matches:
        # Pobieramy dane użytkownika na podstawie jego ID
        user_data = get_user_data(match, AUTHKEYOPERIONA)
        # Jeśli dane są dostępne
        if user_data and (user_data.get("username") or user_data.get("global_name")):
            # Pobieramy nazwę użytkownika z danych
            username = user_data.get("username")
            if user_data.get("global_name"):
                username = user_data.get("global_name")
            # Zamieniamy tag na nazwę użytkownika w wiadomości plus dajemy nowy tag oznaczania
            message = message.replace(f"<@{match}>", username)
    # Zwracamy zmodyfikowaną wiadomość
    return message


def completion_api(prompt, engine="gpt-3.5-turbo-instruct", temperature=0.0, max_new_tokens=1024, stop=None):
    try:
        komplicja = openai.Completion.create(
            engine=engine,
            prompt=prompt,
            max_tokens=max_new_tokens,
            temperature=temperature,
            stop=stop
        ).choices[0].text
    except:
        print("There was a problem. Waiting for 1 second")
        time.sleep(1)
        try:
            komplicja = openai.Completion.create(
                engine=engine,
                prompt=prompt,
                max_tokens=max_new_tokens,
                temperature=temperature,
                stop=stop
            ).choices[0].text
        except:
            print("There was a problem. Waiting for 12 second")
            time.sleep(12)
            komplicja = openai.Completion.create(
                engine=engine,
                prompt=prompt,
                max_tokens=max_new_tokens,
                temperature=temperature,
                stop=stop
            ).choices[0].text
    return komplicja

# assistant nazywa się Output
# dzienniki zawierają name i content
def prompt_generation(historia: dict, temperature=0.8) -> str:
    print("Historia, której używamy:")
    print(historia)
    try:
        with open("turbo_prompt.txt", "r", encoding="utf-8") as f:
            prompt = f.read()
    except:
        print("Nie udało się otworzyć pliku turbo_prompt.txt")
        raise FileNotFoundError("Nie udało się otworzyć pliku turbo_prompt.txt")
    while historia[-1]['name'] == "Output":
        historia.pop(-1)
    for wiadomosc in historia:
        prompt += "\n" + wiadomosc['name'] + ": " + wiadomosc['content']
    prompt += "\nOutput:"
    komplicja = completion_api(prompt, temperature=temperature, stop=["\n"])[1:]
    historia.append({"name": "Output", "content": komplicja})
    print("Wygenerowana komplicja:")
    print(komplicja)
    return komplicja


def is_it_hugging(user_message):
    prompt = f"""You are going to be given a sentence. If a sentence is in form of "do something (in English) to something / someone" you have to output a sentence in form of "Narysuj jak <A VERB IN FIRST PERSON PRESENT TENSE IN POLISH> <A THING/PERSON>. Otherwise you output None. Here are examples and a task:

openai.com/playground?mode=complete -> None
 pat indy -> Narysuj jak głaszczę indy
 fast and furious -> None
dobrze. Teraz zrób podobny plakat, ale dla filmu "caust" -> None
 kick Marek -> Narysuj jak kopię Marka
kiss Eryk -> Narysuj jak całuję Eryka
narysuj mi plakat filmu animowanego disney pixar o nazwie Ryż m -> None
Napisz słowo kapusta: -> None
 hug openai -> Narysuj jak przytulam openai
{user_message} ->"""
    komplicja = completion_api(prompt, temperature=0.1, stop=["\n"])[1:]
    print("Komplicja wewnątrz is_it_hugging:")
    print(komplicja)
    return komplicja


def bingPicture(prompt, auth):
    gen = BingImageCreator.ImageGen(auth)
    image_urls = gen.get_images(prompt)
    print("Done")
    return image_urls[0]



def openAI_picture(prompt):
    response = openai.Image.create(
        model="dall-e-3",
        prompt=prompt,
        size="1024x1024",
        quality="standard",
        n=1,
    )
    image_url = response.data[0].url
    return image_url


def handle_response(historia: dict) -> str:
    temp = "url"
    dlugosc = len(BINGAPIKEYLIST)
    for i in range(dlugosc):
        print("Próbuję. auth numer to: " + str(dlugosc - i - 1))
        try:
            temp = bingPicture(prompt_generation(historia), BINGAPIKEYLIST[dlugosc - i - 1])
            # w przyszłości spróbuj znaleść "Due to high demand, we're unable to process new requests. Please try again later." w tekście
            return temp
        except:
            pass
    try:
        temp = openAI_picture(prompt_generation(historia))
        return temp
    except:
        try:
            temp = openAI_picture(prompt_generation(historia))
            return temp
        except:
            pass
    return "url"


def is_difference_greater_than_12_hours(current_datetime, defined_datetime):
    time_difference = current_datetime - defined_datetime
    return abs(time_difference) > datetime.timedelta(hours=12)


# Send messages
async def send_message(message, name, user_message, is_private):
    global ostatia_wiadomosc, AUTHKEYOPERIONA
    if not "<@1103314100848697395>" in user_message: # wtedy komenda
        dane = user_message.split(" ")
        if dane[0] == "help":
            await message.channel.send(f"BagnoBot wersja {VERSION}\nCommands are:\n- help\n- send_the_history\n- add_the_bing_token\n- change_the_AUTHKEYOPERIONA")
        elif dane[0] == "list":
            pass
        elif dane[0] == "send_the_history":
            for wiadomosc in historia:
                await message.channel.send(str(wiadomosc))
        elif dane[0] == "add_the_bing_token":
            await message.channel.send(f"Adding the following bing token {dane[1]}")
            BINGAPIKEYLIST.append(dane[1])
            await message.channel.send(f"There are now {len(BINGAPIKEYLIST)} bing tokens")
        elif dane[0] == "change_the_AUTHKEYOPERIONA":
            AUTHKEYOPERIONA = dane[1]
            await message.channel.send(f"AUTHKEYOPERIONA is now equal to {AUTHKEYOPERIONA}")
        return
    if is_difference_greater_than_12_hours(datetime.datetime.now(), ostatia_wiadomosc):
        historia.clear()
    while len(historia) > 6:
        historia.pop(0)
    user_message = remove_tag(user_message)
    user_message = replace_tag_with_username(user_message)
    try:
        a_hug = is_it_hugging(user_message)
        if a_hug != "None":
            url = handle_response([{'name': name, 'content': a_hug}])
        else:
            historia.append({"name": name, "content": user_message})
            url = handle_response(historia)
        if url == "url":
            await message.channel.send("Nie udało się wybingować ani jednego linku. Najpewniej serwery Microsoftu są przeciążone lub wszystkie tokeny zostały zablokowane. Spróbuj ponownie później")
            return
        if len(url) > 1000:
            await message.channel.send("Link jest jakiś pojebany. Prawdopodobnie nie jest nawet linkiem tylko całą stroną internetową. Spróbuj ponownie czy coś")
    except:
        await message.channel.send("Coś się spierdoliło podczas generowania obrazka. Spróbuj ponownie czy coś")
        return
    # Get the response from the url
    try:
        response = requests.get(url)
    except:
        await message.channel.send("Coś się spierdoliło podczas pobierania obrazka. Link pewnie nie jest linkiem. Spróbuj ponownie czy coś")
        return
    try:
        temp = response.status_code
    except:
        await message.channel.send('Nie ma czegoś takiego jak "response.status_code"')
        return
    if response.status_code == 200:
        # Get the file name from the url
        # file_name = url.split("/")[-1]
        # file_name = remove_non_latin_letters(file_name)
        file_name = "temp.png"
        # Save the response content as a file
        with open(file_name, "wb") as file:
            file.write(response.content)
        # Get the channel object from the channel id
        channel = message.channel
        # Check if the channel is valid
        if channel:
            # Create a discord file object from the file name
            discord_file = discord.File(file_name)
        # Send the file to the channel
            await channel.send(file=discord_file)
        else:
            print("Invalid channel id")
            return
    else:
        await message.channel.send("Invalid URL. The response code something is " + str(response.status_code) + ". You're truly gonna do something with this and not just try again until it works")
        return
    ostatia_wiadomosc = datetime.datetime.now()
    return


def run_discord_bot():
    TOKEN = DISCORDTOKEN
    #client = discord.Client()

    intents = discord.Intents.default()
    #intents.message_content = True
    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        print(f'{client.user} is now running!')

    @client.event
    async def on_message(message):
        # Make sure bot doesn't get stuck in an infinite loop
        if message.author == client.user:
            return
        # Make sure he doesn't respond to messages not directed to him
        if message.content == "":
            return
        # Get data about the user
        username = str(message.author)
        name = str(message.author.display_name) 
        user_message = str(message.content)
        channel = str(message.channel)

        # Debug printing
        print(f"{username} said: '{user_message}' ({channel})")

        # If the user message contains a '?' in front of the text, it becomes a private message
        if user_message[0] == '?':
            user_message = user_message[1:]  # [1:] Removes the '?'
            await send_message(message, name, user_message, is_private=True)
        else:
            await send_message(message, name, user_message, is_private=False)

    # Remember to run your bot with your personal TOKEN
    client.run(TOKEN)


if __name__ == "__main__":
    run_discord_bot()
