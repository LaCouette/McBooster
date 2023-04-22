from flask import Flask, render_template, request, make_response
from PIL import Image, ImageDraw, ImageFont
import io
import base64

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Récupérer les informations du formulaire
        nom = request.form['nom'].upper()
        prenom = request.form['prenom'].upper()
        date_validite = request.form['date_validite']
        cropped_image_data = request.form['cropped_image']

        # Charger et traiter l'image rognée en base64
        img_data = base64.b64decode(cropped_image_data.split(',')[1])
        img = Image.open(io.BytesIO(img_data)).convert('RGBA')
        img = img.resize((210, 210), Image.ANTIALIAS)

        # Appliquer le border-radius de 50% pour rendre l'image parfaitement ronde
        mask = Image.new('L', (210, 210), 0)
        draw_mask = ImageDraw.Draw(mask)
        draw_mask.ellipse((0, 0, 210, 210), fill=255)
        img.putalpha(mask)


        # Charger l'image template
        base_image = Image.open("static/template.png")
        base_image.paste(img, (95, 760), img)

        # Ajouter du texte
        draw = ImageDraw.Draw(base_image)
        font = ImageFont.truetype("fonts/Between 3 W01 Heavy.ttf", 32)

        text_width, _ = draw.textsize(nom, font=font)
        draw.text((850 - text_width, 785), nom, font=font, fill="#31302F")

        text_width, _ = draw.textsize(prenom, font=font)
        draw.text((850 - text_width, 840), prenom, font=font, fill="#31302F")

        text_width, _ = draw.textsize(date_validite, font=font)
        draw.text((840 - text_width, 910), date_validite, font=font, fill="#FFFFFF")

        # Sauvegarder l'image en mémoire
        output = io.BytesIO()
        base_image.save(output, format='PNG')
        output.seek(0)

        # Créer une réponse avec le nom de fichier et envoyer l'image
        response = make_response(output.getvalue())
        response.headers.set('Content-Type', 'image/png')
        response.headers.set('Content-Disposition', 'attachment', filename='output.png')
        return response

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
