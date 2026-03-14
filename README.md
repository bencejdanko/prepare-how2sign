# how2sign-rgb-front-clips

The HuggingFace dataset can be collected from [bdanko/how2sign-rgb-front-clips](https://huggingface.co/datasets/bdanko/how2sign-rgb-front-clips).

The full How2Sign dataset is hosted on Google Drive, which has currently run out of Google download "quota", making community access difficult. This repository contains some preparation scripts for uploading front-view clips to HuggingFace in a structured way.

Data sourced from [How2Sign](https://how2sign.github.io/).

![alt text](image.png)

| Split | Count |
| :--- | :--- |
| Train | 31047 |
| Val | 1739 |
| Test | 2343 |

> [!IMPORTANT]
> There is a known mismatch in the official release where several videos listed in the .csv annotations are physically missing from the raw video directories.
>
> The dataset omits text annotation that lacked a corresponding .mp4 file.
>
> Total Omitted: Train (118), Val (2), Test (14)
>
> See the generated missing_{split}.txt files for the exact list of omitted filenames.

# Approach

We read the standard dataset splits (train, val, test) from CSV metadata and cross-references them against raw .mp4 files. Each relevant CSV row data for each video in converted into an individualized JSON object. We tar shard video files (.mp4) alongside their corresponding metadata (.json) into sequentially numbered .tar archives, batching them into structured shards of 1,000 samples each.

# Instructions

Make sure you have your data sourced to a single folder

```
# data located in /mnt/c/Users/bence/Downloads/How2Sign

# translations and mappings
how2sign_test.csv
how2sign_val.csv
how2sign_train.csv

# all videos
test_rgb_front_clips/raw_videos
train_rgb_front_clips/raw_videos
val_rgb_front_clips/raw_videos
```

# Commands

```bash
# embed json metadata && create tar shards
python3 prepare.py
```


```bash
# upload to huggingface
hf upload bdanko/how2sign /mnt/c/Users/bence/Downloads/How2Sign/hf_tar_shards --repo-type dataset
```