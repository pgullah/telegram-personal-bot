from common.models import Media, MediaMetadata


def parse(info) -> MediaMetadata:
    entries = info.get("entries")
    if entries and len(entries) > 0:
        ## parse playlist
        formats = []
        for f in entries.get("formats"):
            formats = formats + f
    else:
        # assume its a single video
        formats = info.get("formats")
    
    media = [Media(url=f['url']) for f in formats if f['ext'] == 'mp4' and f.get('audio_channels')]
    return MediaMetadata(items= media)