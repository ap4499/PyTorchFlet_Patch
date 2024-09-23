import platform
import shutil
from pathlib import Path
import os
import logging


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG) 

logger.debug("Starting log.")



class RuntimePatch:
    def __init__(self):
        self._get_subfolder()

    def _get_subfolder(self):
        bundle_dir = Path(__file__).parent
        # original_folder = Path.cwd() / bundle_dir / 'contents' #When using Flet Pack this is the right path.
        original_folder = Path.cwd() /bundle_dir
        # Path to the specific subfolder you want to copy
        subfolder_to_copy = original_folder / "RunTime_resources"
        self.subfolder = subfolder_to_copy

    def _get_app_cache_dir(self):
        """Returns the path to the application's cache directory."""

        user_home = os.path.expanduser("~")

        app_name = "APPNAME-VERSION"  # Replace with your actual app name. Sometimes Flet attaches the version number, and this is the location of the cache.
        cache_dir = os.path.join(user_home, "Library", "Caches", app_name)
        # This is the path to the user's app cache
        logger.debug(f"Path to cache is: {cache_dir}")

        # Create the directory if it doesn't exist
        if not os.path.exists(cache_dir):
            os.makedirs(cache_dir)

        return cache_dir
    
    def torch_bin_patch(self):
        """Copies the specified folder to the application's cache directory."""

        cache_dir = self._get_app_cache_dir()
        folder_path = os.path.join(self.subfolder,"bin_c")
        destination_path = os.path.join(cache_dir,"app","__pypackages__","torch", "bin")

         # Check if the destination path exists and is a file
        if os.path.exists(destination_path) and not os.path.isdir(destination_path):
            os.remove(destination_path)  # Remove the existing file

        logger.debug(("Folder_path: " + folder_path))
        logger.debug(('Destination_path: '+ destination_path))
        try:
            if os.path.exists(destination_path):
                shutil.rmtree(destination_path)

            shutil.copytree(folder_path, destination_path)
        except OSError as e:
            print(f"Error copying folder: {e}")
            logger.debug(f"Error copying folder: {e}")


    def _unzip_file(self):
        import os
        import zipfile

        def unzip_file(zip_filepath, extract_dir):
            """Unzips a file to the specified directory."""

            with zipfile.ZipFile(zip_filepath, 'r') as zip_ref:
                zip_ref.extractall(extract_dir)

        # Get the current script's directory
        script_dir = os.path.dirname(os.path.abspath(__file__))

        # Construct the zip file path
        zip_filepath = os.path.join(script_dir, "RunTime_resources", "torch.zip")

        # Extract to the same directory where the zip file is located
        extract_dir = os.path.join(script_dir, "RunTime_resources")

        # Unzip the file
        unzip_file(zip_filepath, extract_dir)

        logger.debug("Unzip complete")

    def patch_torch_optim(self):
        logger.debug("Unzip torch")
        self._unzip_file()
        logger.debug("Successfully unzipped.")
        def compare_and_copy(folder1, folder2):
            """
            Compares two folders, lists missing files, and copies them to the second folder.

            Args:
                folder1 (str): Path to the source folder (source).
                folder2 (str): Path to the destination folder (cache).
            """

            for root, dirs, files in os.walk(folder1):
                relative_path = os.path.relpath(root, folder1)
                corresponding_path = os.path.join(folder2, relative_path)

                for file in files:
                    file_path1 = os.path.join(root, file)
                    file_path2 = os.path.join(corresponding_path, file)

                    if not os.path.exists(file_path2):
                        # Create the corresponding directory in folder2 if it doesn't exist
                        os.makedirs(corresponding_path, exist_ok=True)

                        # Copy the file
                        shutil.copy2(file_path1, file_path2)
                        print(f"Copied: {os.path.relpath(file_path1, folder1)}")
        
        cache_dir = self._get_app_cache_dir()
        folder_path = os.path.join(self.subfolder,"torch")
        destination_path = os.path.join(cache_dir,"app","__pypackages__","torch")
        logger.debug("Copying torch files from source to destination.")
        logger.debug(f"Source: {folder_path}")
        logger.debug(f"Destination:{destination_path}")
        compare_and_copy(folder_path,destination_path)
        logger.debug("Finished copying files.")

