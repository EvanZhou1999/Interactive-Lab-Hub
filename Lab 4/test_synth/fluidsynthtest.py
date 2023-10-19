# sudo apt-get install libsdl2-dev jackd
# sudo apt-get install fluidsynth
# python3 -m pip install pyFluidSynth
# Start the JACK server
#   jackd -d alsa
# Add your user to the audio group
#    sudo usermod -a -G audio pi
import time
import fluidsynth

fs = fluidsynth.Synth()
#fs.start(driver="alsa")  # Use a different driver (e.g., "alsa" for ALSA)
#fs.sample_rate = 48000 #44100  # Set the sample rate (adjust to your needs)
fs.start()

sfid = fs.sfload("example.sf2")
fs.program_select(0, sfid, 0, 0)

fs.noteon(0, 60, 30)
fs.noteon(0, 67, 30)
fs.noteon(0, 76, 30)

time.sleep(1.0)

fs.noteoff(0, 60)
fs.noteoff(0, 67)
fs.noteoff(0, 76)

time.sleep(1.0)

fs.delete()