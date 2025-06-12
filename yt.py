import subprocess
import os
import sys
import re
from tqdm import tqdm
from typing import List, Callable

class YouTubeDownloader:
    def __init__(self):
        self.install_requirements()
    
    def install_requirements(self) -> None:
        """Ensure required tools (yt-dlp and ffmpeg) are installed."""
        try:
            subprocess.run(["yt-dlp", "--version"], check=True, 
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("yt-dlp is not installed. Installing now...")
            subprocess.run([sys.executable, "-m", "pip", "install", "yt-dlp"], check=True)

        try:
            subprocess.run(["ffmpeg", "-version"], check=True, 
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except FileNotFoundError:
            print("ffmpeg is not installed. Please install ffmpeg manually.")
            sys.exit(1)

    @staticmethod
    def show_menu() -> None:
        """Display the main menu options."""
        print("""
========= YouTube Downloader Tool =========
Combo:
 1. Download video with audio
 2. Download audio + description
 3. Download video/audio + comments
Single:
 4. Only title
 5. Only audio
 6. Only description
 7. Only comments
Multi:
 8. Multi-link video+audio download
 9. Multi-link only titles
10. Multi-link only descriptions
11. Multi-link only comments
12. Multi-link only audio
==========================================
""")

    @staticmethod
    def get_links() -> List[str]:
        """Get and validate YouTube links from user input."""
        while True:
            links = input("Enter link(s) separated by commas: ").split(',')
            valid_links = [link.strip() for link in links if re.match(r'https?://', link.strip())]
            
            if valid_links:
                return valid_links
            print("No valid links found. Please enter at least one valid URL starting with http:// or https://")

    @staticmethod
    def sanitize_filename(text: str, max_length: int = 50) -> str:
        """Sanitize text to be used as a filename."""
        return re.sub(r'[\\/*?:"<>|]', "_", text[:max_length])

    def download_video_audio(self, link: str) -> None:
        """Download video with audio in selected format."""
        print(f"\n[Downloading video with audio] => {link}")

        # Show available formats
        print("\nAvailable formats:\n")
        subprocess.run(["yt-dlp", "-F", link], check=True)

        selected_format = input("Enter the format code you want to download (e.g., 22 or 137+140): ").strip()
        output_template = "%(title).80s.%(ext)s"
        
        try:
            # Get filename before download to handle move operation
            info_cmd = ["yt-dlp", "--get-filename", "-f", selected_format, "-o", output_template, link]
            filename = subprocess.check_output(info_cmd).decode().strip()

            # Download the video
            subprocess.run(["yt-dlp", "-f", selected_format, "-o", output_template, link], check=True)

            # Handle file moving if requested
            move_choice = input("Move to SD card video folder? (y/n): ").lower()
            if move_choice == 'y':
                target_dir = "/sdcard/Movies/"
                os.makedirs(target_dir, exist_ok=True)
                target_path = os.path.join(target_dir, filename)
                
                if os.path.exists(filename):
                    os.rename(filename, target_path)
                    print(f"Video moved to: {target_path}")
                else:
                    print(f"Downloaded file not found: {filename}")
        except subprocess.CalledProcessError as e:
            print(f"Error during download: {e}")

    def download_audio_description(self, link: str) -> None:
        """Download audio (MP3) and description."""
        print(f"\n[Downloading audio + description] => {link}")
        
        try:
            # Download audio
            subprocess.run(["yt-dlp", "-x", "--audio-format", "mp3", link], check=True)
            
            # Get and save description
            description = subprocess.check_output(["yt-dlp", "--get-description", link]).decode().strip()
            safe_title = self.sanitize_filename(description)
            txt_file = f"{safe_title}_description.txt"
            
            with open(txt_file, "w", encoding="utf-8") as f:
                f.write(description)
            
            print(f"Description saved as: {txt_file}")
        except subprocess.CalledProcessError as e:
            print(f"Error during download: {e}")

    def download_with_comments(self, link: str) -> None:
        """Download video/audio with comments."""
        print(f"\n[Downloading video/audio + comments] => {link}")

        try:
            # Show formats and get selection
            subprocess.run(["yt-dlp", "-F", link], check=True)
            selected_format = input("Enter format code (e.g., 22 or 137+140): ").strip()

            # Download media
            output_template = "%(title).80s.%(ext)s"
            subprocess.run(["yt-dlp", "-f", selected_format, "-o", output_template, link], check=True)

            # Process comments
            self._download_and_process_comments(link)
        except subprocess.CalledProcessError as e:
            print(f"Error during download: {e}")

    def _download_and_process_comments(self, link: str) -> None:
        """Helper method to download and process comments."""
        title = subprocess.check_output(["yt-dlp", "--get-title", link]).decode().strip()
        safe_title = self.sanitize_filename(title)
        json_file = f"{safe_title}.info.json"

        try:
            # Download comments
            subprocess.run(["yt-dlp", "--write-comments", "--skip-download", "-o", safe_title, link], check=True)

            if os.path.exists(json_file):
                # Save comments to text file
                txt_file = f"{safe_title}_comments.txt"
                with open(txt_file, "w", encoding="utf-8") as f:
                    subprocess.run(["jq", "-r", ".comments[].text", json_file], stdout=f, check=True)
                
                print(f"Comments saved as: {txt_file}")
                os.remove(json_file)
                print(f"Removed JSON file: {json_file}")
            else:
                print("Comment JSON not found!")
        except subprocess.CalledProcessError as e:
            print(f"Error processing comments: {e}")

    def get_metadata(self, link: str, metadata_type: str) -> None:
        """Generic method to get different types of metadata."""
        print(f"\n[{metadata_type.capitalize()}] => {link}")
        
        try:
            # Get the requested metadata
            result = subprocess.check_output(["yt-dlp", f"--get-{metadata_type}", link]).decode().strip()
            
            # Save to file
            safe_title = self.sanitize_filename(result if metadata_type == "title" else result[:50])
            txt_file = f"{safe_title}_{metadata_type}.txt"
            
            with open(txt_file, "w", encoding="utf-8") as f:
                f.write(result)
            
            print(f"{metadata_type.capitalize()} saved as: {txt_file}")
        except subprocess.CalledProcessError as e:
            print(f"Error getting {metadata_type}: {e}")

    def download_audio(self, link: str) -> None:
        """Download audio only (MP3 format)."""
        print(f"\n[Downloading Audio Only] => {link}")
        try:
            subprocess.run(["yt-dlp", "-x", "--audio-format", "mp3", link], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error during audio download: {e}")

    def handle_multi(self, links: List[str], function: Callable) -> None:
        """Process multiple links with a given function."""
        for link in tqdm(links, desc="Processing"):
            try:
                function(link)
            except Exception as e:
                print(f"Error processing {link}: {e}")

    def run(self) -> None:
        """Main application loop."""
        while True:
            self.show_menu()
            try:
                choice = int(input("Enter your choice (1-12): "))
                if choice not in range(1, 13):
                    print("Invalid choice. Please choose between 1 and 12.")
                    continue
                
                links = self.get_links()
                if not links:
                    continue

                # Map choices to functions
                choice_map = {
                    1: self.download_video_audio,
                    2: self.download_audio_description,
                    3: self.download_with_comments,
                    4: lambda l: self.get_metadata(l, "title"),
                    5: self.download_audio,
                    6: lambda l: self.get_metadata(l, "description"),
                    7: lambda l: self._download_and_process_comments(l),
                    8: self.download_video_audio,
                    9: lambda l: self.get_metadata(l, "title"),
                    10: lambda l: self.get_metadata(l, "description"),
                    11: lambda l: self._download_and_process_comments(l),
                    12: self.download_audio
                }

                self.handle_multi(links, choice_map[choice])

            except ValueError:
                print("Please enter a number between 1 and 12.")
            except KeyboardInterrupt:
                print("\nExiting...")
                break

if __name__ == "__main__":
    downloader = YouTubeDownloader()
    downloader.run()
