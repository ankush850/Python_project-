import os
from pytube import YouTube
from pytube.exceptions import PytubeError, VideoUnavailable, AgeRestrictedError

def download_youtube_video(url, output_path=None):
    """
    Downloads a YouTube video using pytube library.
    
    Args:
    url (str): The URL of the YouTube video.
    output_path (str, optional): The directory path to save the video. Defaults to current directory.
    
    Returns:
    bool: True if download successful, False otherwise.
    """
    try:
        # Initialize the YouTube object
        print("Initializing YouTube video...")
        yt = YouTube(url)
        
        # Display video metadata
        print("\nVideo Information:")
        print(f"Title: {yt.title}")
        print(f"Thumbnail URL: {yt.thumbnail_url}")
        print(f"Views: {yt.views:,}")
        print(f"Length: {yt.length} seconds")
        print(f"Author: {yt.author}")
        print(f"Description: {yt.description[:200]}...")  # Truncate description for brevity
        
        # List available streams
        print("\nAvailable streams:")
        for stream in yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc():
            print(f"  - Resolution: {stream.resolution}, Filesize: {stream.filesize_mb:.2f} MB")
        
        # Get the highest resolution stream
        print("\nSelecting highest resolution stream...")
        stream = yt.streams.get_highest_resolution()
        
        if not stream:
            print("No suitable stream found.")
            return False
        
        print(f"Downloading: {stream.resolution} - {stream.filesize_mb:.2f} MB")
        
        # Set output path if provided
        if output_path:
            if not os.path.exists(output_path):
                os.makedirs(output_path)
            download_path = output_path
        else:
            download_path = os.getcwd()
        
        # Download the video
        print("Starting download...")
        filename = stream.download(output_path=download_path)
        print(f"Download completed! Saved as: {filename}")
        
        return True
        
    except VideoUnavailable:
        print("Error: The video is unavailable or private.")
        return False
    except AgeRestrictedError:
        print("Error: The video is age-restricted and requires login.")
        return False
    except PytubeError as e:
        print(f"Error: Pytube encountered an issue - {str(e)}")
        return False
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        return False

def main():
    """
    Main function to run the YouTube downloader.
    Prompts user for URL and optional output path.
    """
    print("YouTube Video Downloader")
    print("=" * 30)
    
    # Get URL from user
    url = input("Enter the YouTube video URL: ").strip()
    if not url:
        print("No URL provided. Exiting.")
        return
    
    # Validate URL (basic check)
    if "youtube.com" not in url and "youtu.be" not in url:
        print("Invalid URL. Please provide a valid YouTube URL.")
        return
    
    # Get optional output path
    output_path = input("Enter output directory (press Enter for current directory): ").strip()
    if not output_path:
        output_path = None
    
    # Download the video
    success = download_youtube_video(url, output_path)
    
    if success:
        print("\nDownload finished successfully!")
    else:
        print("\nDownload failed. Please check the error message above.")

if __name__ == "__main__":
    main()
