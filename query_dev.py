import sounddevice as sd

devices = sd.query_devices()
print('Audio Devices:')
for device in devices:
    dev_name = device['name']
    input_channels = device['max_input_channels']
    output_channels = device['max_output_channels']
    if input_channels > 0 and output_channels == 0:
        print(dev_name, ': mic with', input_channels, 'input channels.')
    elif output_channels > 0 and input_channels == 0:
        print(dev_name, ': speaker with', output_channels, 'output channels.')
    else:
        print(dev_name, 'is neither a mic or speaker.')
