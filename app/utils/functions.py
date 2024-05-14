import os
import re

from PIL import Image, ImageFilter, ImageOps, ImageEnhance
import numpy

dr = 'C:/Users/motyh/PycharmProjects/sticker_bot/app'


badwords_file = open("C:/Users/motyh/PycharmProjects/sticker_bot/app/utils/badwords.txt", "r", encoding='UTF-8')
badwords = set(badwords_file.read().split(' '))
reg = re.compile('[^а-я А-Я a-z A-Z]')
reg1 = re.compile('\s{2,}')

def check_badwords(line: str) -> bool:
    line = reg.sub('', line)
    line = reg1.sub(' ', line).lower()
    for elem in line.split(" "):
        if elem in badwords:
            return True
    return False

async def find_coeffs(pa, pb):
    matrix = []
    for p1, p2 in zip(pa, pb):
        matrix.append([p1[0], p1[1], 1, 0, 0, 0, -p2[0]*p1[0], -p2[0]*p1[1]])
        matrix.append([0, 0, 0, p1[0], p1[1], 1, -p2[1]*p1[0], -p2[1]*p1[1]])

    A = numpy.matrix(matrix, dtype=float)
    B = numpy.array(pb).reshape(8)

    res = numpy.dot(numpy.linalg.inv(A.T * A) * A.T, B)
    return numpy.array(res).reshape(8)

async def remove_files(photo_name):
    pass
    # os.remove(f'C:/Users/motyh/PycharmProjects/sticker_bot/app/users_photos/{photo_name}.png')
    # os.remove(f'C:/Users/motyh/PycharmProjects/sticker_bot/app/generated_stickers/{photo_name}_1.png')
    # os.remove(f'C:/Users/motyh/PycharmProjects/sticker_bot/app/generated_stickers/{photo_name}_5.png')


async def generate_sticker_pack(photo_name):
    try:
        avatar = Image.open(f'C:/Users/motyh/PycharmProjects/sticker_bot/app/users_photos/{photo_name}.png')
        sticker = Image.open(f'{dr}/stickers/sticker_1.png')
        mask = Image.open(f'{dr}/stickers/mask_1.png')

        # Стикер 1
        mask = mask.convert("L")
        mask = mask.filter(ImageFilter.GaussianBlur(0.85))

        scaler = 148 / avatar.height
        width = int(scaler * avatar.width)
        height = int(scaler * avatar.height)
        avatar = avatar.resize((width, height))

        if avatar.width > avatar.height:
            cut = (avatar.width - 254) // 2
            avatar = ImageOps.expand(avatar, border=(-cut, 0), fill=(255, 255, 255))
        else:
            avatar = ImageOps.expand(avatar, border=(53, 0), fill=(255, 255, 255))

        coeffs = await find_coeffs(
            [(21, -1), (278, 40), (235, 210), (-3, 153)],
            [(0, 0), (avatar.width, 0), (avatar.width, avatar.height), (0, avatar.height)])

        avatar = avatar.transform((270, 204), Image.PERSPECTIVE, coeffs)
        avatar = avatar.filter(ImageFilter.SMOOTH)

        sticker.paste(avatar, (242, 96), mask)
        sticker.save(f'{dr}/generated_stickers/{photo_name}_1.png')

        # Стикер 5
        sticker = Image.open(f'{dr}/stickers/sticker_5.png')
        mask = Image.open(f'{dr}/stickers/mask_5.png')
        avatar = Image.open(f'{dr}/users_photos/{photo_name}.png')

        mask = mask.convert("L")

        scaler = 246 / avatar.height
        width = int(scaler * avatar.width)
        height = int(scaler * avatar.height)
        avatar = avatar.resize((width, height))
        cut = abs(avatar.width - 156) // 2
        avatar = avatar.crop(
            (cut, 0, avatar.width - cut, avatar.height)
        )
        avatar = avatar.resize((156, 246))
        mask = mask.resize((156, 246))
        sticker.paste(avatar, (343, 9), mask)
        sticker.save(f'{dr}/generated_stickers/{photo_name}_5.png')

        return True
    except Exception as e:
        print(e)

        return False

