# 🍈 MelonYoutubeDL - Your Fresh Video Downloader

A user-friendly Python script for downloading YouTube videos in high resolution, featuring a beautiful and interactive command-line interface.

<img src="demo.png" alt="MelonYoutubeDL Demo" />

---

## ✨ Features

- **High-Resolution Downloads**: Supports video resolutions from 320p up to 8K.
- **Interactive UI**: A rich, melon-themed console interface for easy operation.
- **Resolution Selection**: Interactively choose your desired video quality from a list of available resolutions and file sizes.
- **Audio & Video Merging**: Automatically downloads the best audio and selected video streams and merges them using FFmpeg.
- **Thumbnail Downloader**: Option to download the video's thumbnail image.
- **Organized Output**: All downloaded files are saved neatly into an `output` directory.

---

## 📋 Requirements

Before you begin, ensure you have the following installed:

1.  **Python 3.x**
2.  **FFmpeg**: The script relies on FFmpeg for merging video and audio files.
    -   **Windows**: Download from [ffmpeg.org](https://ffmpeg.org/download.html) and add the `bin` directory to your system's PATH.
    -   **macOS**: `brew install ffmpeg`
    -   **Linux**: `sudo apt update && sudo apt install ffmpeg`
3.  **Python Libraries**: The necessary libraries are listed in `requirements.txt`.

---

## 🚀 Installation

1.  **Clone the repository (optional):**
    ```sh
    git clone <repository-url>
    cd MelonYoutubeDL
    ```

2.  **Install Python dependencies:**
    Open your terminal and run the following command to install the required libraries:
    ```sh
    pip install -r requirements.txt
    ```

---

## ▶️ How to Run

1.  Execute the script from your terminal:
    ```sh
    python MelonYoutubeDL.py
    ```

2.  Follow the on-screen prompts:
    -   Enter the YouTube video URL.
    -   Decide if you want to download the thumbnail.
    -   Choose the desired video resolution from the generated table.

The script will handle the download and merging process, and the final video will be saved in the `output` folder.

---

## ⚠️ Known Issues

1.  **Download Failed**:
    -   Sometimes, the download may fail due to network issues or changes in YouTube's backend. Simply re-running the script often resolves the issue.
    -   Using a proxy might be necessary in some regions.

2.  **8K Video Downloads**:
    -   Downloading 8K videos may require authentication tokens. This feature is supported by the underlying `pytubefix` library but may require code modifications.
    -   For more details, refer to the [pytubefix documentation](https://pytubefix.readthedocs.io/en/latest/user/po_token.html).

---

## 📄 License

This project is licensed under the **MIT License**.

You can use this code for other projects, but you **Must provide it is forked by THIS PROJECT**.

---

## 📧 Contact

For any questions or feedback, feel free to reach out:

-   **Email**: kbs.programmer@gmail.com
