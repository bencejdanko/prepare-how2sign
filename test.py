from datasets import load_dataset

local_dataset = load_dataset(
    "videofolder", 
    data_dir="/mnt/c/Users/bence/Downloads/How2Sign/hf_ready", 
    split="test"
)

print(local_dataset.features)
print(local_dataset[0])