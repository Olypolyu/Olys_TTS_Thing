# Olys_TTS_Thing

Uses a lot of python libraries to run a simple TTS when you press left ctrl + shift. You will need mpv installed and the current voice model was what i found to be best comprimese between quality and load on the system. 
I Use this to talk on discord without revealing my real voice. **No warranty will be provided.**

# On Windows:

If you are on windows you need to drop the binary inside this project's folder. Also, you need virtual audio cable as well.

*quick tip: run ```./mpv.exe -audio-device=help | echo``` inside the project folder to get a list of audio outputs, from there just edit ```def speak()``` to use the audio device of your choice*
