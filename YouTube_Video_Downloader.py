import os
from pytube import YouTube
from pytube.exceptions import PytubeError, VideoUnavailable, AgeRestrictedError

def download_youtube_video(url, output_path=None):
    """
    Downloads a YouTube video using pytube.
    
    Args:
        url (str): YouTube video URL.
        output_path (str, optional): Output directory. Defaults to current.
    
    Returns:
        bool: True if successful, False otherwise.
    """
    try:
        print("Initializing YouTube video...")
        yt = YouTube(url)
        
        # Display metadata
        print("\nVideo Information:")
        print(f"Title: {yt.title}")
        print(f"Thumbnail URL: {yt.thumbnail_url}")
        print(f"Views: {yt.views:,}")
        print(f"Length: {yt.length} seconds")
        print(f"Author: {yt.author}")
        print(f"Description: {yt.description[:150]}...")  # Truncated
        
        # Get highest resolution stream
        print("\nSelecting highest resolution stream...")
        stream = yt.streams.get_highest_resolution()
        
        if not stream:
            print("No suitable stream found.")
            return False
        
        print(f"Downloading: {stream.resolution} - {stream.filesize_mb:.2f} MB")
        
        # Set output path
        if output_path:
            if not os.path.exists(output_path):
                os.makedirs(output_path)
            download_path = output_path
        else:
            download_path = os.getcwd()
        
        # Download
        print("Starting download...")
        filename = stream.download(output_path=download_path)
        print(f"Download completed! Saved as: {filename}")
        
        return True
        
    except VideoUnavailable:
        print("Error: Video unavailable or private.")
        return False
    except AgeRestrictedError:
        print("Error: Video age-restricted (requires login).")
        return False
    except PytubeError as e:
        print(f"Error: Pytube issue - {str(e)}")
        return False
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        return False

# Main execution
if __name__ == "__main__":
    url = "https://www.youtube.com/watch?v=1MBR39rTEs8"
    output_path = None  # Change to custom path if needed, e.g., "./downloads"
    
    success = download_youtube_video(url, output_path)
    if success:
        print("\nDownload finished successfully!")
    else:
        print("\nDownload failed.")
