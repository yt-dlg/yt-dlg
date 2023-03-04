To install **FFmpeg**, you need to download the installer or the static build from [ffmpeg.org](https://ffmpeg.org/download.html) [¹][1] [³][3]. Then, you need to run the installer or extract the static build to a folder on your computer[²][2] [³][3] [⁴][4] [⁵][5]. You also need to add the FFmpeg bin folder to the `PATH` environment variable, so that you can use FFmpeg from any terminal[³][3] [⁴][4] [⁵][5]. Here are the steps to add FFmpeg to the PATH on Windows[⁵][5]:

1. Open the Start menu and type "`environment variables`".
2. Click **Edit the system environment variables**.
3. Click **Environment Variables** at the bottom of the window.
4. Double-click the **Path** variable in the upper portion of the window.
5. Click the **New button** to open a new blank line below the bottom-most path.
6. Type `C:\ffmpeg\bin` or the path to the **FFmpeg** bin folder on your computer.
7. Click **OK** to save the changes.

## Video Youtube
[![Install FFmpeg Windows](https://img.youtube.com/vi/7HbfBwehGV4/mqdefault.jpg)](https://youtu.be/7HbfBwehGV4)

## Configure FFmpeg on yt-dlg
Another option to configure `ffmpeg` on **yt-dlg** is go,

`Setting -> Options -> Extra` tab and set `--ffmpeg-location <PathToFFmpegBinFolder>` for example:

```txt
--ffmpeg-location "C:\ffmpeg\bin"
```

Read more: Post-Processing[⁶][6]

[1]: <https://bing.com/search?q=install+FFmpeg> "Accessed 2/13/2023."
[2]: <https://www.videoproc.com/resource/how-to-install-ffmpeg.htm> "How to Install FFmpeg on Windows, Mac, Linux Ubuntu and Debian - VideoProc. Accessed 2/13/2023."
[3]: <https://support.audacityteam.org/basics/saving-and-exporting-projects/installing-ffmpeg> "Installing FFmpeg - Audacity Support. Accessed 2/13/2023."
[4]: <https://phoenixnap.com/kb/ffmpeg-windows> "Installing FFmpeg on Windows {Step-by-Step}. Accessed 2/13/2023."
[5]: <https://www.wikihow.com/Install-FFmpeg-on-Windows> "How to Install FFmpeg on Windows: 15 Steps (with Pictures) - wikiHow. Accessed 2/13/2023."
[6]: <https://github.com/yt-dlp/yt-dlp#post-processing-options> "yt-dlp: Post-processing Options. Accessed 3/4/2023."
