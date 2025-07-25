import yt_dlp
import traceback

"""
Fetches trending videos from YouTube.
"""

from typing import List, Dict

def get_trending_videos() -> List[Dict[str, object]]:
    ydl_opts = {
        'extract_flat': True,
        'playlistend': 30, 
        'quiet': False,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            list_trending = ydl.extract_info('https://www.youtube.com/feed/trending', download=False)
            return [{k: el[k] for k in ("url", "title", "description", "duration", "thumbnails","channel", "channel_url", "view_count")} for el in list_trending['entries']]

        except Exception as e:
            print(f"Error fetching trending videos: ")
            traceback.print_exc()
            return []
