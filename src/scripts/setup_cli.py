import os
import platform
import requests
import shutil
import subprocess

def map_arch(arch):
    arch = arch.lower()
    mappings = {
        'x32': '386',
        'x64': 'amd64',
        'x86_64': 'amd64'
    }
    return mappings[arch]


def map_platform(os_name):
    os_name = os_name.lower()
    mappings = {
        'darwin': 'darwin',
        'windows': 'windows',
        'linux': 'linux'
    }
    return mappings[os_name]


def get_platform_arch():
    """
    Returns the (name, arch) of current os
    """
    return platform.system(), platform.machine()


def get_filename_to_download(version):
    """
    Construct file name based on current os information
    """
    platform_data = get_platform_arch()
    platform, arch = map_platform(platform_data[0]), map_arch(platform_data[1])
    raw_filename = f"okareo-cli_{version}_{platform}_{arch}"
    extension = 'tar.gz'
    file_name = f'{raw_filename}.{extension}'
    return file_name


def get_download_url(version):
    """
    Return (url, filename) pair for downloading
    """
    filename = get_filename_to_download(version)
    return f"https://github.com/okareo-ai/okareo-cli/releases/download/v{version}/{filename}"


def download_and_extract(url, output_dir="."):
    """
    Download a tar.gz file from the specified URL and extract its contents.
    Args:
        url (str): The URL of the tar.gz file to download.
        output_dir (str): The directory where the contents will be extracted. Default is the current directory.
    """
    # Download the file
    response = requests.get(url)
    
    # Save the file
    filename = url.split("/")[-1]
    file_path = f"{output_dir}/{filename}"
    with open(file_path, "wb") as f:
        f.write(response.content)
    
    # Extract the file
    shutil.unpack_archive(file_path, extract_dir=output_dir)


def main():
    version = os.getenv('OKAREO_CLI_VERSION', '0.0.5')
    url = get_download_url(version)
    download_and_extract(url)

if __name__ == "__main__":
    main()