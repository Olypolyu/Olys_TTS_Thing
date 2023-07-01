import os
import subprocess
import PySimpleGUI as sg
from pynput import keyboard
from pynput.keyboard import Key

# since it takes a while the tts to boot up
print("loading...")

# this actually runs an innit on import that takes a little while to load, so we have to break convention for this one.
from TTS.api import TTS

# initialize TTS
model_name = "tts_models/en/jenny/jenny"
tts = TTS(model_name)

# check if we can use kdialog, if we can, use that.
if os.name != 'nt':
    try:
        subprocess.run(['which', 'kdialog'], check=True, stdout=subprocess.PIPE)
        Kdialog = True
    except subprocess.CalledProcessError:
        Kdialog = False

else:
    Kdialog = False


def speak(string):
    tts.tts_to_file(text=string, file_path="workFolder/output.wav")

    # Output audio file to microphone
    if os.name == 'nt':
        subprocess.run(
            'mpv.exe ./workFolder/output.wav --vo=drm --audio-device="wasapi/{278afc5c-10c1-44d8-b590-37e0f97e5692}"',
            shell=True)
    else:
        subprocess.run(
            'mpv ./workFolder/output.wav --vo=drm --audio-device="pipewire/audiorelay-virtual-mic-sink"',
            shell=True)

    os.remove("./workFolder/output.wav")
    return


# set theme for our windows
sg.theme("LightBrown13")


def promptWindow():
    if Kdialog:
        messageBox = subprocess.run('kdialog --title "TTS" --inputbox "Enter Text:"', shell=True,
                                    stdout=subprocess.PIPE)
        return messageBox.stdout.decode()

    layout = [
        [sg.Text("Enter Text:")],
        [sg.InputText(key="-TEXT-")],
        [sg.Button("Send", bind_return_key=True)]
    ]

    # Create the window and set focus to it.
    window = sg.Window("TTS", layout, grab_anywhere=True, finalize=True)
    window.TKroot.focus_force()
    window.Element("-TEXT-").SetFocus()

    # Create an event loop
    while True:
        event, values = window.read()  # Read an event and values from the window

        if event == "Send":  # If the user clicks OK
            window.close()
            toSend = values['-TEXT-']
            break

        if event == sg.WIN_CLOSED:  # If the user closes the window
            toSend = ""
            break

    window.close()
    return toSend


if Kdialog:
    subprocess.run('kdialog --title "TTS Ready!" --passivepopup "Press Shift + Left CTRL To Run" 5', shell=True)

print("listening to key presses. type shift + left ctrl")
SHIFT_STATE = False


def on_press(key):
    global SHIFT_STATE
    if key == keyboard.Key.shift:
        SHIFT_STATE = True
    else:
        try:
            if SHIFT_STATE and key == Key.ctrl_l:
                text = promptWindow()
                SHIFT_STATE = False

                if text.strip() != "":
                    speak(text)

        except Exception as e:
            print(e)


def on_release(key):
    global SHIFT_STATE

    if key == keyboard.Key.shift:
        SHIFT_STATE = False


# Collect events until released
with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
