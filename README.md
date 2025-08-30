# Able to Browse

## About

Able to Browse is a Max for Live device that helps you quickly load instruments, effects, and samples in Ableton Live without scrolling through the browser. It works alongside a companion web app which can be opened on your phone or iPad, letting you select and drop devices directly into your session with a single tap on your mobile device.

## Download

**GitHub Repository:** [https://github.com/ishaanjagyasi/Able_to_browse](https://github.com/ishaanjagyasi/Able_to_browse)

The download contains the folders as shown in the image.

### Installation Instructions

#### Main Folder Installation
The complete main folder called `able_to_browse` should be placed in:
- **WIN:** `~\Documents\Max 9\Library`
- **MAC:** `~/Documents/Max 9/Packages`

#### Device Caller Installation
You can subsequently copy and paste the `Device_caller.amxd` in Ableton Live's directory for Max MIDI Effects:
- **WIN:** `~Documents\Ableton\User Library\Presets\MIDI Effects\Max MIDI Effect`
- **MAC:** `/Users/user_name/Music/Ableton/User Library/Presets/MIDI Effects/Max MIDI Effect`

#### Remote Script Installation
The folder called `DeviceLoaderv2` should be placed in:
- **WIN:** `~\Documents\Ableton\User Library\Remote Scripts`
- **MAC:** `/Users/your_user_name/Music/Ableton/User Library/Remote Scripts`

## How to Use

### A) M4L Device

1. **Open Live and select "Device Loader v2" as a control surface:**
   - Go to: `Settings > Link,Tempo,MIDI > Control Surface`
   - Put it on a slot on which you are not using any other control surface

2. **Drop the `Device_caller.amxd`** in your Live session preferably on a MIDI track.

3. **Type the slot number** in which the `Device Loader v2` control surface exists (in the image, slot no. 1)

4. **Click on the 'Press to Start' button.**

### B) Web App

1. **Open the WebApp:**
   [https://ishaanjagyasi.github.io/ableton-deviceloader-website/](https://ishaanjagyasi.github.io/ableton-deviceloader-website/)

2. **On the top left corner** you will see a section called 'Session'. Here is where you will see your session ID which looks something like `"session_jkndf83sk"`.

3. **Type the string that follows 'session_'** in your Max for Live device and press enter. The two platforms are now connected!

### C) Customising

In the webapp we have created mappings for all the native Live devices. To create your own mappings:

1. **Find the device/plugin/sample/instrument** that you are looking for in your Live browser, check the exact way in which it is named. For example, if I want to create a mapping for 'Granulator III', the device name in Live's browser is 'Granulator III'. Type the exact name (without an extension if there is one like .adg, .wav etc) of the device under the 'Add Device Section' of the web app and press the 'Add' button to create a mapping for your desired device. You can also create your custom mapping under the 'Custom' section.

2. **You can Export your customised mappings** by pressing the "Export Preset" button under the 'Preset & Mode' section. This will save .json file in your machine. You can share this file to another device, open the web app in the new device and select the 'Import Preset' option to import the .json file to recall your customised preset that you have created on any device.

3. **Under the "Preset & Mode" section**, there is an option called "Edit Mode: OFF", which you can press on and turn on the edit mode. When Edit Mode is ON, you will see small crosses on the mapping rectangles. You can just remove the mappings that you already had with the Edit Mode.

---

*by Able to Devices*