# Import the torch module to interact with the GPU
import torch

# If statement to confirm that the GPU node is accessible
if torch.cuda.is_available():
    # Get all the properties about the available GPU
    device_props = torch.cuda.get_device_properties(0)
    # Print the device name
    print(f"GPU Name: {device_props.name}")
    # Print the capability specs
    print(f"Compute Capability: {device_props.major}.{device_props.minor}")
    # Print the allocated memory size
    print(f"Total Memory: {device_props.total_memory / 1e9} GB")

# These printed statements are included in the final output to specify the GPU specs
