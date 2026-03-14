import os
import pandas as pd
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor

BASE_DIR = "/mnt/c/Users/bence/Downloads/How2Sign"
OUTPUT_DIR = os.path.join(BASE_DIR, "hf_ready")
SPLITS = ["train", "val", "test"]
ID_COLUMN = "SENTENCE_NAME" 

def create_link(paths):
    src, dst = paths
    try:
        if not os.path.exists(dst):
            os.link(src, dst)
    except OSError:
        pass

for split in SPLITS:
    csv_path = os.path.join(BASE_DIR, f"how2sign_{split}.csv")
    df = pd.read_csv(csv_path, sep='\t')
    
    video_dir = os.path.join(BASE_DIR, f"{split}_rgb_front_clips", "raw_videos")
    split_out_dir = os.path.join(OUTPUT_DIR, split)
    os.makedirs(split_out_dir, exist_ok=True)
    
    existing_files = set(os.listdir(video_dir))
    
    df['file_name'] = df[ID_COLUMN].astype(str) + '.mp4'
    valid_df = df[df['file_name'].isin(existing_files)].copy()
    
    link_tasks = [
        (os.path.join(video_dir, f), os.path.join(split_out_dir, f)) 
        for f in valid_df['file_name']
    ]
    
    print(f"\nInitialized {split} split: {len(link_tasks)} valid bijections mapped.")
    
    with ThreadPoolExecutor(max_workers=os.cpu_count() * 4) as executor:
        list(tqdm(executor.map(create_link, link_tasks), total=len(link_tasks), desc=f"Linking {split}", unit="file"))
        
    valid_df.to_csv(os.path.join(split_out_dir, "metadata.csv"), index=False)