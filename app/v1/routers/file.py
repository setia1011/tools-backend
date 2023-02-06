from fastapi import APIRouter
from fastapi.responses import FileResponse

router = APIRouter()


@router.get('/audio')
async def audio(f: str):
    import mimetypes
    mime = mimetypes.guess_type("./app/assets/audios/"+f)[0]
    headers = {'Content-Disposition': f'attachment; filename="{f}"'}
    return FileResponse("./app/assets/audios/" + f, headers=headers, media_type=mime)


@router.get('/video')
async def video(f: str):
    import mimetypes
    mime = mimetypes.guess_type("./app/assets/videos/"+f)[0]
    headers = {'Content-Disposition': f'attachment; filename="{f}"'}
    return FileResponse("./app/assets/videos/" + f, headers=headers, media_type=mime)


@router.get('/subtitle')
async def subtitle(f: str):
    import mimetypes
    mime = mimetypes.guess_type("./app/assets/subtitles/"+f)[0]
    headers = {'Content-Disposition': f'attachment; filename="{f}"'}
    return FileResponse("./app/assets/subtitles/" + f, headers=headers, media_type=mime)