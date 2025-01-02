from flask import Flask, request, send_file
import os
import yt_dlp

app = Flask(__name__)

def download_video(url, output_path='downloads/'):
    # Asegúrate de que la carpeta 'downloads' exista
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    
    ydl_opts = {
        'format': 'best',
        'outtmpl': f'{output_path}%(title)s.%(ext)s',
        'quiet': False,
        'no_warnings': True,
        'noplaylist': True,
        'postprocessors': [{
            'key': 'FFmpegVideoConvertor',
            'preferedformat': 'mp4',
        }],
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info_dict)  # Ruta completa del archivo
    
    return filename

@app.route('/')
def index():
    return '''
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Descargador de Videos</title>
    </head>
    <body>
        <h1>Descargar Videos desde URL</h1>
        <form action="/download" method="POST">
            <label for="url">Ingresa la URL del video:</label>
            <input type="text" id="url" name="url" placeholder="URL del video" required>
            <button type="submit">Descargar Video</button>
        </form>
    </body>
    </html>
    '''

@app.route('/download', methods=['POST'])
def download():
    url = request.form['url']
    if not url:
        return "Por favor, ingresa una URL válida.", 400

    try:
        filename = download_video(url)
        return send_file(filename, as_attachment=True)
    except Exception as e:
        return f"Hubo un error al intentar descargar el video: {str(e)}", 500

if __name__ == '__main__':
    app.run(debug=True)
