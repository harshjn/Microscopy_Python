# After starting micro-manager and loading the Hardware configuration file, control it with python
from pycromanager import Core

# Initialize the core
core = Core()

# List all loaded devices
devices = core.get_loaded_devices()

# Convert mmcorej.StrVector to a Python list
device_list = [devices.get(i) for i in range(devices.size())]

# Print the list of devices
print("Connected devices:")
for device in device_list:
    print(device)

#%% Get com port for any device. In this case, Olympus Hub.

try:
    # Attempt to get the COM port property
    com_port = core.get_property('OlympusHub', "Port")
    print(f"  COM Port: {com_port}")
except:
    # Handle the case where the device does not have a "Port" property
    print(f"  COM Port: Not applicable")

#%% Set the shutter on or off
core.set_property('Shutter1', 'State', '1')
core.set_property('Shutter1', 'State', '0')


# Retrieve the far limit of the manual focus
far_limit = core.get_property('ManualFocus', 'FarLimit')
print(f"Far limit of the manual focus: {far_limit}")

# Move manual focus to the far point
core.set_property('ManualFocus', 'Position', far_limit)
print(f"Moved manual focus to the far point: {far_limit}")

# Set the z-position
new_focus_position = 3000  # Specify the desired focus position
core.set_property('ManualFocus', 'Position', str(new_focus_position))
print(f"Moved Z focus to position: {new_focus_position}")

#%%
# Example: Turn on the TransmittedLamp
core.set_property('TransmittedLamp', 'State', '1')
print("Transmitted lamp is turned on.")

# Example: Turn off the TransmittedLamp
core.set_property('TransmittedLamp', 'State', '0')
print("Transmitted lamp is turned off.")

# Example: Disconnect from the OlympusHub
core.unload_device('OlympusHub')
