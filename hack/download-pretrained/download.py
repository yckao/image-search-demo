import argparse
import os
from transformers import CLIPProcessor, CLIPModel


def download_pretrained_model(name: str, path: str):
    # Check if model files already exist
    model_files_exist = os.path.exists(os.path.join(path, "pytorch_model.bin"))
    config_exists = os.path.exists(os.path.join(path, "config.json"))
    processor_exists = os.path.exists(os.path.join(path, "processor_config.json"))

    if model_files_exist and config_exists and processor_exists:
        print(f"Model already exists at {path}. Skipping download.")
        return

    model = CLIPModel.from_pretrained(name)
    model.save_pretrained(path)
    processor = CLIPProcessor.from_pretrained(name)
    processor.save_pretrained(path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser("Image Search Demo Pretrained Model Downloader")
    parser.add_argument(
        "--model_name",
        "-m",
        type=str,
        required=False,
        default=os.environ.get("MODEL_NAME"),
    )
    parser.add_argument(
        "--model_path",
        "-p",
        type=str,
        required=False,
        default=os.environ.get("MODEL_PATH"),
    )
    args = parser.parse_args()

    model_name = args.model_name
    model_path = args.model_path

    download_pretrained_model(model_name, model_path)
