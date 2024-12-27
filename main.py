import subprocess
from argparse import ArgumentParser, Namespace
from pathlib import Path


def parse_args() -> Namespace:
    parser = ArgumentParser()
    parser.add_argument(
        "-i", "--dvd-folder", type=Path, required=True,
        help="Path to the DVD folder containing VOB files (e.g., VIDEO_TS)."
    )
    return parser.parse_args()


def run(dvd_folder: Path) -> None:
    if not dvd_folder.is_dir():
        print(f"Error: The specified folder '{dvd_folder}' does not exist or is not a directory.")
        return

    mp4_folder = dvd_folder.parent / f"{dvd_folder.name}_MP4"
    mp4_folder.mkdir(parents=True, exist_ok=True)

    vob_files = list(dvd_folder.rglob("*.vob"))
    if not vob_files:
        print("No VOB files found in the specified folder.")
        return

    for vob_file in vob_files:
        base_name = vob_file.stem
        output_file = mp4_folder / f"{base_name}.mp4"

        command = [
            "ffmpeg", "-i", str(vob_file),  # Input VOB file
            "-c:v", "libx264",  # Video codec
            "-c:a", "aac",  # Audio codec
            "-strict", "experimental",  # Allow experimental codecs
            str(output_file)  # Output MP4 file
        ]

        print(f"Converting {vob_file} to {output_file}...")
        try:
            subprocess.run(command, check=True)
            print(f"Successfully converted {vob_file} to {output_file}.")
        except subprocess.CalledProcessError as e:
            print(f"Failed to convert {vob_file}. Error: {e}")


if __name__ == "__main__":
    run(**vars(parse_args()))
