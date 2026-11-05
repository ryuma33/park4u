"""
extract_frames.py: pull the app screens out of the old park4u demo video.

The original screenshots were lost, so this script watches the video and saves
a picture every time the phone screen changes noticeably. Those pictures were
used to rebuild every screen of the prototype.

Usage:
    pip install opencv-python numpy
    python tools/extract_frames.py park4u.mp4 screens

Options:
    --left / --right   which part of the 1920px-wide video is the phone (pixels)
    --threshold        how different a frame must be to count as a new screen
"""
import argparse
import os

import cv2
import numpy as np


def main():
    p = argparse.ArgumentParser(description="Save a frame whenever the phone screen changes.")
    p.add_argument("video", help="path to the demo video, e.g. park4u.mp4")
    p.add_argument("out", help="folder to save the pictures into")
    p.add_argument("--left", type=int, default=690, help="left edge of the phone in the video (px)")
    p.add_argument("--right", type=int, default=1226, help="right edge of the phone in the video (px)")
    p.add_argument("--threshold", type=float, default=2.5, help="change needed to save a new frame")
    p.add_argument("--every", type=int, default=15, help="check every Nth frame (15 = twice a second at 30fps)")
    args = p.parse_args()

    os.makedirs(args.out, exist_ok=True)
    cap = cv2.VideoCapture(args.video)
    fps = cap.get(cv2.CAP_PROP_FPS) or 30

    index, saved, previous = 0, 0, None
    while True:
        ok, frame = cap.read()
        if not ok:
            break  # end of the video
        if index % args.every == 0:
            phone = frame[:, args.left:args.right]  # crop to just the phone
            # Shrink + greyscale so small changes (noise) don't count
            small = cv2.resize(cv2.cvtColor(phone, cv2.COLOR_BGR2GRAY), (67, 135)).astype(np.float32)
            if previous is None or np.mean(np.abs(small - previous)) > args.threshold:
                saved += 1
                name = f"{saved:03d}_t{index / fps:06.2f}.png"  # number + time in seconds
                cv2.imwrite(os.path.join(args.out, name), phone)
                previous = small
        index += 1

    print(f"Saved {saved} screens to {args.out}/")


if __name__ == "__main__":
    main()
