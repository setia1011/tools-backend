from fastapi import APIRouter, File, UploadFile, Form, Request
from fastapi.responses import FileResponse
from app.v1.schemas import home as home_schema

router = APIRouter()


@router.get("/", response_model=home_schema.Home)
async def home():
    data = {"data": "tools API version 1.0.1"}
    return data


@router.post("/qr", response_model=home_schema.QrCodeOut)
async def qrcode(qr_schema: home_schema.QrCodeIn):
    if qr_schema.text:
        import qrcode
        from io import BytesIO
        from base64 import b64encode
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=1,
        )
        qr.add_data(qr_schema.text)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        buffer = BytesIO()
        img.save(buffer)
        encoded_img = b64encode(buffer.getvalue()).decode()
        data_uri = "data:image/png;base64,{}".format(encoded_img)
        return {"qrcode": data_uri}
    else:
        return {"qrcode": ""}


@router.post('/translate', response_model=home_schema.TranslateOut)
async def translate(t: home_schema.TranslateIn):
    SPECIAL_CASES = {
        'ee': 'et',
    }
    LANGUAGES = {
        'af': 'afrikaans',
        'sq': 'albanian',
        'am': 'amharic',
        'ar': 'arabic',
        'hy': 'armenian',
        'az': 'azerbaijani',
        'eu': 'basque',
        'be': 'belarusian',
        'bn': 'bengali',
        'bs': 'bosnian',
        'bg': 'bulgarian',
        'ca': 'catalan',
        'ceb': 'cebuano',
        'ny': 'chichewa',
        'zh-cn': 'chinese (simplified)',
        'zh-tw': 'chinese (traditional)',
        'co': 'corsican',
        'hr': 'croatian',
        'cs': 'czech',
        'da': 'danish',
        'nl': 'dutch',
        'en': 'english',
        'eo': 'esperanto',
        'et': 'estonian',
        'tl': 'filipino',
        'fi': 'finnish',
        'fr': 'french',
        'fy': 'frisian',
        'gl': 'galician',
        'ka': 'georgian',
        'de': 'german',
        'el': 'greek',
        'gu': 'gujarati',
        'ht': 'haitian creole',
        'ha': 'hausa',
        'haw': 'hawaiian',
        'iw': 'hebrew',
        'he': 'hebrew',
        'hi': 'hindi',
        'hmn': 'hmong',
        'hu': 'hungarian',
        'is': 'icelandic',
        'ig': 'igbo',
        'id': 'indonesian',
        'ga': 'irish',
        'it': 'italian',
        'ja': 'japanese',
        'jw': 'javanese',
        'kn': 'kannada',
        'kk': 'kazakh',
        'km': 'khmer',
        'ko': 'korean',
        'ku': 'kurdish (kurmanji)',
        'ky': 'kyrgyz',
        'lo': 'lao',
        'la': 'latin',
        'lv': 'latvian',
        'lt': 'lithuanian',
        'lb': 'luxembourgish',
        'mk': 'macedonian',
        'mg': 'malagasy',
        'ms': 'malay',
        'ml': 'malayalam',
        'mt': 'maltese',
        'mi': 'maori',
        'mr': 'marathi',
        'mn': 'mongolian',
        'my': 'myanmar (burmese)',
        'ne': 'nepali',
        'no': 'norwegian',
        'or': 'odia',
        'ps': 'pashto',
        'fa': 'persian',
        'pl': 'polish',
        'pt': 'portuguese',
        'pa': 'punjabi',
        'ro': 'romanian',
        'ru': 'russian',
        'sm': 'samoan',
        'gd': 'scots gaelic',
        'sr': 'serbian',
        'st': 'sesotho',
        'sn': 'shona',
        'sd': 'sindhi',
        'si': 'sinhala',
        'sk': 'slovak',
        'sl': 'slovenian',
        'so': 'somali',
        'es': 'spanish',
        'su': 'sundanese',
        'sw': 'swahili',
        'sv': 'swedish',
        'tg': 'tajik',
        'ta': 'tamil',
        'te': 'telugu',
        'th': 'thai',
        'tr': 'turkish',
        'uk': 'ukrainian',
        'ur': 'urdu',
        'ug': 'uyghur',
        'uz': 'uzbek',
        'vi': 'vietnamese',
        'cy': 'welsh',
        'xh': 'xhosa',
        'yi': 'yiddish',
        'yo': 'yoruba',
        'zu': 'zulu'
    }

    from googletrans import Translator
    translator = Translator(service_urls=['translate.google.com'])
    r = translator.translate(text=t.text, src='id', dest='en')
    part = ''
    part_ = ''
    if len(r.extra_data['parsed']) > 3:
        part = r.extra_data['parsed'][3][5][0][0][0]
        part_ = r.extra_data['parsed'][3][5][0][0][1][0][0]
    return {
        'from_': LANGUAGES[r.src],
        'to': LANGUAGES[r.dest],
        'origin': r.origin,
        'translated': r.text,
        'part': [part, part_]
    }


@router.post('/polaroid')
async def polaroid(file: UploadFile = File(None), caption: str = Form(...)):
    if file:
        ext = file.filename.replace(" ", "").rsplit(".", 1)[1]
        if ext not in ['png','PNG','JPG','jpg','JPEG','jpeg']:
            return {'original': "", 'thumbnail': ""}
        
        ext = ext.lower()
        if ext == 'JPG' or ext == 'jpg':
            ext = 'jpeg'

        import random
        import string
        import io
        from base64 import b64encode
        from PIL import Image, ImageOps, ImageDraw, ImageFont

        letters = string.digits
        filenamex = ''.join(random.choice(letters) for i in range(15))
        filename = filenamex + '.' + ext

        request_object_content = await file.read()
        img = Image.open(io.BytesIO(request_object_content))

        
        fill = "white"
        border = (30, 30, 30, 80)
        imagex = ImageOps.expand(image=img, border=border, fill=fill)
        font = ImageFont.truetype('../assets/fonts/Caveat-Regular.ttf', size=50)
        draw = ImageDraw.Draw(imagex)
        textsize = draw.textsize(text=caption, font=font)
        w, h = textsize
        location = (((imagex.width/2) - (w/2)), ((imagex.height-h) - 17))
        draw.text(location, caption.title(), fill=fill, font=font, stroke_width=1, stroke_fill='black')
        
        imagey = imagex.copy()
        buffer1 = io.BytesIO()
        imagey.save(buffer1, ext)
        encoded_imagey = b64encode(buffer1.getvalue()).decode()
        original = "data:image/"+ext+";base64,{}".format(encoded_imagey)

        size = (450, 450)
        imagex.thumbnail(size, Image.ANTIALIAS)

        buffer = io.BytesIO()
        imagex.save(buffer, ext)
        encoded_img = b64encode(buffer.getvalue()).decode()
        thumbnail = "data:image/"+ext+";base64,{}".format(encoded_img)

        return {'original': original, 'thumbnail': thumbnail, 'filename': filename}


@router.post('/text2speech')
def convert(request: Request, message: str = Form(...), language: str = Form(...)):
    import os
    # do some processing here
    filepath = './temp/welcome.mp3'
    filename = os.path.basename(filepath)
    headers = {'Content-Disposition': f'attachment; filename="{filename}"'}
    return FileResponse(filepath, headers=headers, media_type="audio/mp3")


@router.post('/upload-video')
async def upload_video(file: UploadFile = File(...)):
    if file:
        import moviepy.editor as mp
        import os
        import string
        import random

        ext = file.filename.replace(" ", "").rsplit(".", 1)[1]
        letters = string.digits
        filenamex = ''.join(random.choice(letters) for i in range(15))
        filename = filenamex + '.' + ext

        contents = await file.read()
        with open(os.path.join("./app/assets/videos/", filename), "wb") as fp:
            fp.write(contents)

        import mimetypes
        mime = mimetypes.guess_type("./app/assets/videos/"+filename)[0]

        return {'video': filename, 'mime': mime}
    else:
        return {'video': '', 'type': ''}


@router.post('/video-to-audio-wav')
async def video_to_audio_wav(video: str = Form(...)):
    if video:
        import moviepy.editor as mp
        import string
        import random

        filename = video.split(".")[0] + ".wav"

        # ext = file.filename.replace(" ", "").rsplit(".", 1)[1]
        # letters = string.digits
        # filenamex = ''.join(random.choice(letters) for i in range(15))
        # filename = filenamex + '.wav'

        my_clip = mp.VideoFileClip(r"{}".format("./app/assets/videos/" + video))
        my_clip.audio.write_audiofile(r"{}".format("./app/assets/audios/" + filename))

        import mimetypes
        mime = mimetypes.guess_type("./app/assets/audios/"+filename)[0]

        return {'audio': filename, 'mime': mime}
    else:
        return {'audio': '', 'mime': ''}


@router.post("/transcribe")
async def test(audio: str = Form(...)):
    import whisper
    from datetime import timedelta
    import os

    srtname = audio.split(".")[0] + ".srt"

    model = whisper.load_model("tiny")
    result = model.transcribe("./app/assets/audios/" + audio, fp16=False)
    transcript = " ".join(result['text'].split())

    segments = result['segments']

    for segment in segments:
        startTime = str(0)+str(timedelta(seconds=int(segment['start'])))+',000'
        endTime = str(0)+str(timedelta(seconds=int(segment['end'])))+',000'
        text = segment['text']
        segmentId = segment['id']+1
        segment = f"{segmentId}\n{startTime} --> {endTime}\n{text[1:] if text[0] == ' ' else text}\n\n"

        srtFilename = os.path.join(r"./app/assets/subtitles/", srtname)
        with open(srtFilename, 'a', encoding='utf-8') as srtFile:
            srtFile.write(segment)

    return {"transcript": transcript, "subtitle": srtname}

        