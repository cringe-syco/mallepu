# pip install yt-dlp
import subprocess

def download_youtube_playlist(playlist_url, download=True):
    if not playlist_url.startswith("http"):
        print("Invalid playlist URL.")
        return

    # Base yt-dlp command
    base_cmd = ["yt-dlp", playlist_url]

    if not download:
        # Just print video titles and URLs
        base_cmd += ["--flat-playlist", "-J"]

        try:
            import json
            result = subprocess.run(base_cmd, capture_output=True, text=True, check=True)
            data = json.loads(result.stdout)
            print(f"\nPlaylist: {data.get('title')}")
            for entry in data.get('entries', []):
                print(f"https://www.youtube.com/watch?v={entry['id']} - {entry.get('title', '')}")
        except Exception as e:
            print("Failed to fetch playlist data:", e)
        return

    # Download the full playlist
    try:
        subprocess.run(base_cmd, check=True)
        print("Download complete.")
    except subprocess.CalledProcessError as e:
        print("Download failed:", e)

if __name__ == "__main__":
    print("Enter YouTube playlist URL:")
    # playlist = input("Playlist URL: ").strip()
    playlist = r"https://youtube.com/playlist?list=PLoROMvodv4rPP6braWoRt5UCXYZ71GZIQ&si=zi5m4EyqIX94K7XK"
    print("Do you want to (1) download or (2) just list the videos?")
    choice = "2"
    
    download = choice == "1"
    download_youtube_playlist(playlist, download=download)


# https://www.youtube.com/watch?v=_NLHFoVNlbg AndrewNG Deeplearning
# https://youtube.com/playlist?list=PLoROMvodv4rMiGQp3WXShtMGgzqpfVfbU&si=va087M4uu7RW9JFz AndrewNG MachineLearning

# base_cmd = ["yt-dlp", "-f", "bestaudio", "--extract-audio", "--audio-format", "mp3", playlist_url]
# available formats: yt-dlp -F <video_url>
