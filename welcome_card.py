from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import aiohttp

WIDTH = 1600
HEIGHT = 900

AVATAR_X = 1180
AVATAR_Y = 180
AVATAR_SIZE = 300


async def create_card(member):

    bg = Image.open("assets/background.png").convert("RGBA")
    bg = bg.resize((WIDTH, HEIGHT))

    draw = ImageDraw.Draw(bg)

    title_font = ImageFont.truetype("assets/font.ttf", 70)
    name_font = ImageFont.truetype("assets/font.ttf", 55)

    # Download avatar
    async with aiohttp.ClientSession() as session:
        async with session.get(member.display_avatar.url) as resp:
            avatar_data = await resp.read()

    avatar = Image.open(BytesIO(avatar_data)).convert("RGBA")
    avatar = avatar.resize((AVATAR_SIZE, AVATAR_SIZE))

    # Circle mask
    mask = Image.new("L", (AVATAR_SIZE, AVATAR_SIZE), 0)
    ImageDraw.Draw(mask).ellipse((0, 0, AVATAR_SIZE, AVATAR_SIZE), fill=255)

    avatar.putalpha(mask)

    bg.paste(
        avatar,
        (AVATAR_X, AVATAR_Y),
        avatar
    )

    username = member.display_name

    # Center username under avatar
    bbox = draw.textbbox((0, 0), username, font=name_font)
    text_width = bbox[2] - bbox[0]

    draw.text(
        (
            AVATAR_X + AVATAR_SIZE//2 - text_width//2,
            AVATAR_Y + AVATAR_SIZE + 35
        ),
        username,
        font=name_font,
        fill="white"
    )

    output = BytesIO()
    bg.save(output, "PNG")
    output.seek(0)

    return output