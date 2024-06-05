
from PIL import Image, ImageDraw, ImageFont
import os
from django.conf import settings

def generate_certificate(achievement):
    template_path = os.path.join(settings.BASE_DIR, 'static/certificate_template.png')
    font_path = os.path.join(settings.BASE_DIR, 'static/fonts/arial.ttf')

    image = Image.open(template_path)
    draw = ImageDraw.Draw(image)

    font = ImageFont.truetype(font_path, 40)
    user_text = f"Certificate of Achievement\n\nAwarded to {achievement.user.username}"
    achievement_text = f"For {achievement.title}"

    image_width, image_height = image.size
    user_text_width, user_text_height = draw.textsize(user_text, font=font)
    user_text_x = (image_width - user_text_width) // 2
    user_text_y = image_height // 3

    achievement_text_width, achievement_text_height = draw.textsize(achievement_text, font=font)
    achievement_text_x = (image_width - achievement_text_width) // 2
    achievement_text_y = user_text_y + user_text_height + 50

    draw.text((user_text_x, user_text_y), user_text, font=font, fill='black')
    draw.text((achievement_text_x, achievement_text_y), achievement_text, font=font, fill='black')

    certificate_path = os.path.join(settings.MEDIA_ROOT, 'certificates', f'{achievement.user.username}_{achievement.id}.png')
    image.save(certificate_path)

    achievement.certificate_image = f'certificates/{achievement.user.username}_{achievement.id}.png'
    achievement.save()