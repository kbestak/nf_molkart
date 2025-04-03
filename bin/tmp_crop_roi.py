#!/usr/bin/env python3
## Written by Kresimir Bestak and Florian Wuennemann and released under the MIT license
import tifffile
import numpy as np
import h5py
import pathlib
import os
import random
from skimage import filters
import argparse
import time
import matplotlib.pyplot as plt

os.environ["MPLCONFIGDIR"] = "./tmp"

def generate_overview(image, indices, output_dir, tiff_path, name):
    overview_path = os.path.join(output_dir, f"{name}_crop_overview.png")

    # Create maximum projection of channels
    max_proj = np.max(image, axis=0) if image.ndim == 4 else image
    plt.imshow(np.max(max_proj, axis=0), cmap="gray")

    # Draw crop boxes
    for index, (crop_name, ((h_up, h_down), (w_lt, w_rt))) in enumerate(indices.items(), start=1):
        plt.plot([w_lt, w_rt, w_rt, w_lt, w_lt],
                 [h_up, h_up, h_down, h_down, h_up],
                 "r", linewidth=1)
        plt.text(w_lt, h_up, str(index), color="white", fontsize=8)

    plt.savefig(overview_path, dpi=300)
    print(f"Overview saved: {overview_path}")

def generate_crops(tiff_path, output_dir, crop_size, crop_amount, nonzero_fraction, name, nuclei_channel=0):
    # Load TIFF file
    with tifffile.TiffFile(tiff_path) as tif:
        image = tif.asarray()

    # Select the channel used for thresholding
    im_nuc = image[nuclei_channel]

    # Compute Otsu threshold
    thresh = filters.threshold_otsu(im_nuc)
    print(image.shape)

    # Track previous crops to avoid overlaps
    previous_crops = []
    indices = {}
    count = 1
    height, width = image.shape[1], image.shape[2]  # Get spatial dimensions

    while count <= crop_amount:
        # Compute crop boundaries
        extension_h = crop_size[0] // 2
        extension_w = crop_size[1] // 2
        h = random.randint(extension_h, height - extension_h)
        w = random.randint(extension_w, width - extension_w)
        h_up, h_down = h - extension_h, h + extension_h
        w_lt, w_rt = w - extension_w, w + extension_w

        # Check for overlap
        overlap = any(not (h_down <= prev_h_up or h_up >= prev_h_down or w_rt <= prev_w_lt or w_lt >= prev_w_rt)
                      for prev_h_up, prev_h_down, prev_w_lt, prev_w_rt in previous_crops)
        if overlap:
            continue

        # Extract crop
        crop = im_nuc[..., h_up:h_down, w_lt:w_rt]
        if (crop > thresh).sum() / crop.size >= nonzero_fraction:
            crop_name = pathlib.Path(os.path.join(output_dir, f"crop_{count}.tif"))

            # Save the crop including all channels
            #crop_data = image[..., h_up:h_down, w_lt:w_rt, :]
            #tifffile.imwrite(crop_name, crop_data, photometric='minisblack')
            #print(f"Saved: {crop_name}")

            # Track crop coordinates
            previous_crops.append((h_up, h_down, w_lt, w_rt))
            indices[crop_name.stem] = [(h_up, h_down), (w_lt, w_rt)]
            count += 1

    # Save crop summary
    summary_path = os.path.join(output_dir, f"{name}_CropSummary.txt")
    with open(summary_path, "w") as summary_file:
        summary_file.write(str(indices))
    print(f"Summary saved: {summary_path}")

    generate_overview(image, indices, output_dir, tiff_path, name)

if __name__ == "__main__":
    st = time.time()
    parser = argparse.ArgumentParser(description="Crop non-overlapping regions from a TIFF image based on Otsu thresholding.")
    parser.add_argument("-i", "--input", required=True, help="Path to input TIFF file.")
    parser.add_argument("-o", "--output", required=True, help="Directory to save crops and overview.")
    parser.add_argument("-s", "--crop_size", type=int, nargs=2, default=[128, 128], help="Size of the crops (height width).")
    parser.add_argument("-n", "--num_crops", type=int, default=10, help="Number of crops to generate.")
    parser.add_argument("-f", "--fraction", type=float, default=0.5, help="Minimum fraction of pixels above Otsu threshold.")
    parser.add_argument("--name", type=str, help="Prefix of output file names.")
    parser.add_argument("-c", "--channel", type=int, default=0, help="Index of the channel to threshold.")
    args = parser.parse_args()

    os.makedirs(args.output, exist_ok=True)
    generate_crops(args.input, args.output, tuple(args.crop_size), args.num_crops, args.fraction, args.name, args.channel)

    rt = time.time() - st
    print(f"Script finished in {rt // 60:.0f}m {rt % 60:.0f}s")
