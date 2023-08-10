import os 
import qrcode
from PIL import Image

def generate_dynamic_qr_with_logo(qr_value, logo_path, qr_color, background_color):
    try:
        border_padding = int(os.getenv("QR_PADDING", 1))
        qr_size = int(os.getenv("QR_SIZE", 15))

        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=qr_size,
            border=border_padding,
        )
        qr.add_data(qr_value)
        qr.make(fit=True)

        # # Create a QR code image
        qr_img = qr.make_image(fill_color=qr_color, back_color=background_color).convert('RGB')

        # # Open the logo image
        logo = Image.open(logo_path)

        basewidth = int(os.getenv("LOGO_WIDTH", 50))

        wpercent = (basewidth/float(logo.size[0]))
        hsize = int((float(logo.size[1])*float(wpercent)))
        logo = logo.resize((basewidth, hsize), Image.LANCZOS)

        # set size of QR code
        pos = ((qr_img.size[0] - logo.size[0]) // 2,
                (qr_img.size[1] - logo.size[1]) // 2)

        # # Paste the logo on the QR code
        qr_img.paste(logo, pos)

        # Save the final QR code with the logo
        qr_img.save("/app/output/qr_with_logo.png")
        print("QR code generated!")
    except Exception as E:
        print("Exception: ", E)

# Tomar valores de variables de entorno de docker-compose o asigna el default

QR_link_or_value = os.getenv("QR_VALUE", "https://bio.eml.run/")
logo_path = os.getenv("LOGO_FILE_NAME", "logo.jpg")
qr_color = os.getenv("QR_COLOR", "black")
background_color = os.getenv("QR_BACKGROUND_COLOR", "white")
generate_dynamic_qr_with_logo(QR_link_or_value, logo_path, qr_color, background_color)