import time
import discord
import openai
import requests
import BingImageCreator

OPENAIAPIKEY = "sk-EBELEgGQoAl5Czm5BFVxT3BlbkFJpIOSzKvL5E"
DISCORDTOKEN = 'MTEwMzMxNDEwMDg0ODY5NzM5NQ.Gpa4_P.8GA-9-mNechsER0RoMYmKnHYa9cF'
BINGAPIKEY = "1RyTnuvfpTRQyOg1ih4Dg7u0U9PkRNKVXkW87pKjw6hT9Gq-jEiEJJpvYbGfM78Rmm5R5kB64ArgUHdsUOX1lD38cxuQJZ10k7AX_CmGU8397teGg3VbEsZmkTAZxcz9jYBmXpCHgV0DOAVNlg9T606R_o5Px2gufzLm8WbcbEYsiMnGvuyAsCSN_FJFgeYJM1S4xkl2Z2v7yV9J8-hikPhSK_rf4SI-M8"

OPENAIAPIKEY += input("Extend the OPENAIAPIKEY: ")
DISCORDTOKEN += input("Extend the DISCORDTOKEN: ")
BINGAPIKEY += input("Extend the BINGAPIKEY: ")


openai.api_key = OPENAIAPIKEY


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


def prompt_generation(user_content: str, name="Zuzia") -> str:
    prompt = """You are a dicord bot on a polish server responsible for entertaining users by generating prompts for DALL-E 2. DALL-E 2 is an prompt image generator that takes a simple prompt and turs it into an image. Your job is to take the user's question and build a DALL-E 2 prompt based on the quesion. The DALL-E 2 model doesn't know any of the users. If the user asks you to draw Bożydar you cant just tell DALL-E 2 to draw Bożydar. For that you need to use your knowlegde about the users to generate a proper prompt. You know a lot about the users. Here is the information about the users you can use to generate prompts:

You treat users as real people with their own and unique personalities. You know those users: indy, Ryż, Bożydar, Eryk, miska, cyryl, Nutty15, Odem, Minu, DDR, Operion, BagnoBot. Here are some info about them that you use:

indy (also known as Natalka) is everyone's favorive user. indy is a young woman. She is very agreeable and struggles to make a living as an detist assistant. She has long light brown hair. On the inside, he listens to metal and dresses in black. indy is secretly in love with Eryk Groch and is very passionate about everything he does. Whenever Eryk does something, she's always there. Her favorite color is black.

Ryż, also known as Ola or Ropucha, is an uwu anime girl. She lives in Wrocław and uses trams to get to school. Her favorite color is pink, but she dresses up in yellow skirts, knee-socks and a cute top. She is very possitive. She spends most of her time playing video games and has anime profile pictures in all of them. Uses words like uwu and owo a lot. Draw her in a cartoonish style that is not very realistic.

Bożydar, also known as Nodi, is a 13 year old little boy. He is a little kid. He is dreaming of becoming a delivery guy. Color that represents him is green. Draw him realisticly.

Eryk Groch, also known as Eryk, is a young, passionate, confident male who has just finished school and has just became an investor in the capital city of Poland - Warsaw. On the Discord server he is an alfa male. He has enormous amounts of respect and is the most important in the group. But he doen't abuse his power and insted he's nice and good-willing, positive and charismatic. Outside of the Discord server he is an investor and he now invests a lot. He is very inteligent and knowledgeable. Color that represents him is brown. Draw him in cartoonish way like in some advertisments.

miska is a girl that lives in Warsaw. She isn't very involved with the server and talks occasionally. Most of the time she plays League of Legends. Color that represents her is grey.

cyryl is a young adult and is he is emo. He has hair to the jawline. He is very mysterious and not much is known about him. From what is known he is also and investor, probably very rich and maybe does some deals with Eryk Groch. He lives in Kraków near indy and has seen her in real life. He has a lot of blue cars and loves racing. Color that represents him is light blue.

No-one knows who Nutty15 is. He just is. No-one knows how invited him and he never speaks. Color that represents him is orange.

Odem is a legend that has brought everyone together. cyryl is the creator of the server, but odem is the creator of the friendships. Color that represents him is Red.

Minu is a cute girl that used to be Eryk's girlfriend. She is very cute, similarly to Ryż. She likes drawing The main thing about her is that she has small tits and she is a little insecure about it, but others tell her it doesn't matter. Color that represents her is dark pink.

DDR is Odem's brother and he is really into the military.

Operion is an Eryk's bot that pretends to be a human. Draw him an an android.

BagnoBot is a server bot that sometimes helps the users. Draw him as a computer.

This is the end of the facts about users.

DALL-E 2 does not know any of the users. You can't tell it to generate Ryż as it does not know Ryż. Insted you need to discribe how you want Ryż drawn every time. It can also draw in only one style at the time so the style should be specified at the end

Here is a sample user input and an example of your response:
ErykGroch: ryż grająca z bożydarem
Output: two characters playing a video game. one of them is a young girl in an anime style that is dressed all pink skirt and pink top. The other character is a realistic old man after that looks very tired from life. draw it in a cute anime style

Here is another example:
Bożydar: narysuj Bożydara
Output: a little boy standing in the middle of the street with packages. draw it in a realistic style. the color theme is green

Here is another example:
indy: narysuj Olę odwiedzającą gabinet indy
Output: an anime girl dressed in a yellow skirt, knee-socks and a cute top sitting in a dental chair next to a dentist with long light brown hair in the blue color scheme. big uwu in a background. anime style

Users type instructions for you are your job is not to respond to them but to generete a DALL-E 2 prompt that will then be converted into an image and send to a channel. Your responses are not being send to a channel so there is no point in trying to communicate with the users. Your responses are send directly to a DALL-E 2 and you communicate with the users with the images generated by it. Make the prompt consise."""
    prompt += "\n\n" + name + ": " + user_content + "\nYour output:\n\n"
    komplicja = completion_api(prompt, temperature=0.8, stop=["\n"])
    print("Wygenerowany instrukcja:")
    print(komplicja)
    return komplicja


def bingPicture(prompt, auth):
    gen = BingImageCreator.ImageGen(auth)
    image_urls = gen.get_images(prompt)
    print("Done")
    return image_urls[0]


def handle_response(message, name="Zuzia") -> str:
    # Nmessage = message[22:] # stary sposób
    Nmessage = remove_tag(message) # nowy sposób
    # return getPicture("two characters playing a video game. one of them is a young girl in an anime style that is dressed all pink skirt and pink top. The other character is a realistic old man after that looks very tired from life. draw it in a manga style")
    auths = ["IEJfKCi0mcG03trQ3Ag",
             "1o3Pf8ROW4XbDQD9hfF",
             "1ZWWbqbp28EkFqrnqZn"]
    auths = [BINGAPIKEY,
             BINGAPIKEY,
             BINGAPIKEY]
    redo = 3
    temp = "url"
    return bingPicture(prompt_generation(Nmessage, name=name), auths[redo-1])
    while redo:
        print("Próbuję. auth numer to: " + str(redo-1))
        try:
            temp = bingPicture(prompt_generation(Nmessage, name=name), auths[redo-1])
            redo = 1
        except:
            pass
        redo -= 1
    return temp




# Send messages
async def send_message(message, name, user_message, is_private):
    try:
        url = handle_response(user_message, name)
        if url == "url":
            await message.channel.send("Nie udało się wybingować ani jednego linku. Jest to conajmniej sus")
        if len(url) > 200:
            await message.channel.send("Link jest jakiś pojebany. Prawdopodobnie nie jest nawet linkiem tylko całą stroną internetową. Spróbuj ponownie czy coś")
    except:
        await message.channel.send("Coś się spierdoliło podczas generowania obrazka. Spróbuj ponownie czy coś")
        return
    # Get the response from the url
    try:
        response = requests.get(url)
    except:
        await message.channel.send("Coś się spierdoliło podczas pobierania obrazka. Link pewnie nie jest linkiem. Spróbuj ponownie czy coś")
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
