import os
import gdown
import zipfile
import requests

class LiverDataset:
    '''
    This class is for the liver segmentation dataset from the total segmentator dataset.
    You can get more information about it using `info()` function.

    ### Example usage

    ```Python
    from pycad.dataset.segmentation.decathlon import LiverDataset
    
    liver_dataset = LiverDataset()
    liver_dataset.info()  # Print dataset information
    liver_dataset.download('100')  # Download and extract subgroup 100
    ```
    '''
    def __init__(self, dataset_size=1225):
        self.dataset_size = dataset_size
        self.dataset_subgroups = {
            '100': 'https://drive.google.com/uc?id=1RiZ8hNIYVFmJ1rltfPX3AiYt5s37c8hj',
            '200': 'https://drive.google.com/uc?id=1mHb2z3IVpHGNlzxGnLdV1rqiki2oLcrD',
            '400': 'https://drive.google.com/uc?id=15G11RYvOXoIF5rm-ya5rC4394-0hVxA6',
            'all': 'https://drive.google.com/uc?id=1XDrEXtVqdmLVoiSznlz3ATNRbIyE5ps0'
        }
        self.base_path = 'datasets/'

    def info(self):
        print(f"Liver Dataset from Total Segmentator dataset. This is a collection of CT scans with means these are 3D volumes.")
        print(f"Total Cases: {self.dataset_size}")
        print(f"Subgroups: 100, 200, 400, {self.dataset_size}")
        print("Source: https://zenodo.org/records/10047292")

    def download(self, subgroup, path=None):
        if subgroup not in self.dataset_subgroups:
            print(f"No subgroup {subgroup} available.")
            return

        if subgroup.isdigit() and int(subgroup) > self.dataset_size:
            print(f"Subgroup {subgroup} exceeds dataset size.")
            return

        download_url = self.dataset_subgroups[subgroup]
        save_path = path if path else self.base_path
        self._download_and_extract(download_url, save_path, subgroup)

    def _download_and_extract(self, url, path, subgroup):
        if not os.path.exists(path):
            os.makedirs(path)

        try:
            file_path = os.path.join(path, f'liver{subgroup}.zip')
            gdown.download(url, file_path, quiet=False)

            # Check file size after download
            if os.path.getsize(file_path) < 1024:  # Example size threshold (1KB)
                print("Downloaded file is too small, might be an error.")
                return

            with zipfile.ZipFile(file_path, 'r') as zip_ref:
                zip_ref.extractall(path)
            print(f"Downloaded and extracted at {path}")

            # Delete the zip file after extraction
            os.remove(file_path)
            print(f"Deleted zip file: {file_path}")

        except requests.exceptions.RequestException as e:
            print("Error in downloading the file: ", e)
        except zipfile.BadZipFile:
            print("Error in extracting the file: File may be corrupted or not a zip file.")
        except Exception as e:
            print("An unexpected error occurred: ", e)
            if os.path.exists(file_path):
                os.remove(file_path)
                print(f"Deleted incomplete zip file: {file_path}")