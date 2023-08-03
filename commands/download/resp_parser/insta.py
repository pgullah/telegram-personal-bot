from common.models import Media, MediaMetadata


def parse(info) -> MediaMetadata:
    entries = info.get("entries")
    
    if entries and len(entries) > 0:
        ## parse playlist
        formats = entries
    else:
        # assume its a single video
        formats = info.get("formats")
    
    media = [Media(url=f.get('url'), thumbnail=f.get('thumbnail'), title=f.get('title'), description=f.get('description')) for f in formats]
    return MediaMetadata(items= media, title=info.get('title'), description=info.get('description'))