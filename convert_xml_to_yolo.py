import os
import xml.etree.ElementTree as ET
from PIL import Image
from tqdm import tqdm
import shutil

# -----------------------------
# Final class mapping
# -----------------------------
CLASS_MAP = {
    "D00": 0,  # Longitudinal Crack
    "D10": 1,  # Transverse Crack
    "D20": 2,  # Alligator Crack
    "D40": 3,  # Pothole
    "D43": 4,  # Other corruption → merged
    "D44": 4,
    "D50": 4
}

DATA_DIR = "Data"
OUTPUT_DIR = "dataset"


# -----------------------------
# Convert bounding boxes
# -----------------------------
def convert_box(size, box):
    dw = 1.0 / size[0]
    dh = 1.0 / size[1]

    xmin, xmax, ymin, ymax = box

    x = (xmin + xmax) / 2.0
    y = (ymin + ymax) / 2.0
    w = xmax - xmin
    h = ymax - ymin

    return (x * dw, y * dh, w * dw, h * dh)


# -----------------------------
# Convert TRAIN
# -----------------------------
def convert_train():

    img_dir = os.path.join(DATA_DIR, "train", "images")
    ann_root = os.path.join(DATA_DIR, "train", "annotations")

    out_img_dir = os.path.join(OUTPUT_DIR, "images", "train")
    out_lbl_dir = os.path.join(OUTPUT_DIR, "labels", "train")

    os.makedirs(out_img_dir, exist_ok=True)
    os.makedirs(out_lbl_dir, exist_ok=True)

    # 🔥 Walk through all subfolders
    xml_files = []

    for root_dir, _, files in os.walk(ann_root):
        for file in files:
            if file.endswith(".xml"):
                xml_files.append(os.path.join(root_dir, file))

    print(f"Found {len(xml_files)} XML files")

    for xml_path in tqdm(xml_files, desc="Converting TRAIN"):

        tree = ET.parse(xml_path)
        root = tree.getroot()

        img_name = root.find("filename").text
        img_path = os.path.join(img_dir, img_name)

        if not os.path.exists(img_path):
            print("❌ Missing image:", img_name)
            continue

        img = Image.open(img_path)
        w, h = img.size

        label_name = os.path.basename(xml_path).replace(".xml", ".txt")
        label_path = os.path.join(out_lbl_dir, label_name)

        with open(label_path, "w") as f:

            for obj in root.findall("object"):

                cls_name = obj.find("name").text

                if cls_name not in CLASS_MAP:
                    print("⚠️ Unknown class:", cls_name)
                    continue

                cls_id = CLASS_MAP[cls_name]

                xmlbox = obj.find("bndbox")

                xmin = float(xmlbox.find("xmin").text)
                xmax = float(xmlbox.find("xmax").text)
                ymin = float(xmlbox.find("ymin").text)
                ymax = float(xmlbox.find("ymax").text)

                bb = convert_box((w, h), (xmin, xmax, ymin, ymax))

                f.write(
                    f"{cls_id} {bb[0]} {bb[1]} {bb[2]} {bb[3]}\n"
                )

        # Copy image
        shutil.copy(img_path, out_img_dir)


# -----------------------------
# Convert TEST (images only)
# -----------------------------
def convert_test():

    img_dir = os.path.join(DATA_DIR, "test", "images")
    out_img_dir = os.path.join(OUTPUT_DIR, "images", "test")

    os.makedirs(out_img_dir, exist_ok=True)

    if not os.path.exists(img_dir):
        print("❌ Test images folder not found")
        return

    for img_file in tqdm(os.listdir(img_dir), desc="Copying TEST images"):

        img_path = os.path.join(img_dir, img_file)
        shutil.copy(img_path, out_img_dir)


# -----------------------------
# Main
# -----------------------------
if __name__ == "__main__":

    print("🚀 Converting TRAIN (XML → YOLO)...")
    convert_train()

    print("🚀 Preparing TEST images...")
    convert_test()

    print("✅ Dataset conversion complete!")

