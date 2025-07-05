import sys
import zipfile
import pathlib
import requests


SCRIPT_DIR = (
    pathlib.Path(sys.executable).parent
    if getattr(sys, "frozen", False)
    else pathlib.Path(__file__).resolve().parent
)


def download_file(url, destination_path):
    try:
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            with open(destination_path, "wb") as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
        print(f"Downloaded: {destination_path}")
    except Exception as e:
        print(f"Failed to download {url} -> {e}")


def unzip_zip(zip_file: pathlib.Path, output_directory: pathlib.Path):
    with zipfile.ZipFile(zip_file, "r") as zip_ref:
        zip_ref.extractall(output_directory)


def ensure_path_quoted(path: str) -> str:
    return f'"{path}"' if not path.startswith('"') and not path.endswith('"') else path
