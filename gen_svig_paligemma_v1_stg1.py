import os
from transformers import AutoProcessor, PaliGemmaForConditionalGeneration, BitsAndBytesConfig
from PIL import Image
import requests
import torch

HF_TOKEN = "OBSCURED"

model_id = "google/paligemma-3b-mix-224"
device = "cuda:0"
dtype = torch.bfloat16

url = "https://huggingface.co/datasets/huggingface/documentation-images/resolve/main/transformers/tasks/car.jpg?download=true"
image = Image.open(requests.get(url, stream=True).raw)

quantization_config = BitsAndBytesConfig(load_in_8bit=True)

model = PaliGemmaForConditionalGeneration.from_pretrained(
    model_id, quantization_config=quantization_config,
    token=HF_TOKEN
).eval()
processor = AutoProcessor.from_pretrained(model_id, token=HF_TOKEN)

def prompt(prompt, image):
    # Instruct the model to create a caption in English
    model_inputs = processor(text=prompt, images=image, return_tensors="pt").to(model.device)
    input_len = model_inputs["input_ids"].shape[-1]

    with torch.inference_mode():
        generation = model.generate(**model_inputs, max_new_tokens=384, do_sample=False)
        generation = generation[0][input_len:]
        decoded = processor.decode(generation, skip_special_tokens=True)
        print(decoded)
        return decoded

import cairosvg
import time
import json
import os
from PIL import Image
import hashlib
from datasets import Dataset, load_dataset
import pandas as pd
import argparse

zf = zipfile.ZipFile("archive.zip", "r")

ap = argparse.ArgumentParser()
ap.add_argument("-d", "--debug", type=bool, required=False, default=False)
apr = ap.parse_args()
DEBUG_ON = False
if apr.debug == True:
    print("Debug mode on!")
    DEBUG_ON = True

svgcaps = []
images_dict = []
idx = 0
start = 0
failed = 0
chk_idx = 0
for name in zf.namelist():
    if name.startswith(".") or not name.endswith(".svg"):
        continue
    with zf.open(name, "r") as fp:
        svg = ""
        pngname = ""
        svg = fp.read().decode("utf-8")
        fp.seek(0)
        with open(f"tmp.png", "wb") as f:
            try:
                res = cairosvg.svg2png(fp.read(), unsafe=True, file_obj=f, output_width=224, output_height=224, write_to="tmp2.png", background_color="#ffffff")
            except Exception as e:
                print("Error! " + str(e))
                idx += 1
                failed += 1
                continue
        print(res)
        img = Image.open("tmp2.png")
        with open("tmp2.png", "rb") as f:
            res = f.read()
        capt = prompt("caption en", img)
        cap = prompt("cap en", img)
        desc = prompt("describe en", img)
        
        print(cap)
        print(capt)
        print(desc)
        if not os.path.exists("svg"):
            os.makedirs("svg")
        #with open(f"svg/{idx}.2.json", "w") as f:
        hsh = hashlib.sha256(res).hexdigest()                
        img.save(os.path.join(".", "svg", hsh + ".png"), "PNG")
        images_dict.append({
            "cap": cap,
            "caption": capt,
            "description": desc,
            "svg": svg,
            "sha256": hsh,
            "image": img.tobytes()
        })

        if len(images_dict) >= 25600 or (len(images_dict) == 3 and DEBUG_ON):
            captions = []
            description = []
            svg = []
            hashes = []
            images_ = []
            for img_ in images_dict:
                 captions.append(img_['caption'])
                 description.append(img_['image'])
                 svg.append(img_['svg'])
                 hashes.append(img_['sha256'])
                 images_.append(img_['image'])
            df = pd.DataFrame(
                {
                    'captions': captions,
                    'descriptions': description,
                    'svgs': svg,
                    'hashes': hashes,
                    'images': images_
                    })
            ds = Dataset.from_pandas(df)
            ds.save_to_disk(f"chk{chk_idx}.hf")
            chk_idx += 1
        idx += 1
