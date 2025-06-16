import os, random, json, requests, subprocess, zipfile, platform, threading, time
import tkinter as tk
# CONFIG
VERSION = "1.21.1"
FAST_DOWNLOAD = True # DOSENT INSTALL ASSETS (USE FOR DEBUG)
BASE_DIR = os.path.join(os.getcwd(), "instances", VERSION)

LIB_DIR = os.path.join(BASE_DIR, "libraries")
NATIVES_DIR = os.path.join(BASE_DIR, "natives")
GAME_DIR = os.path.join(BASE_DIR, "game")
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
CLIENT_JAR = os.path.join(BASE_DIR, "client.jar")

USERNAME = 'Player'
UUID = "00000000-0000-0000-0000-000000000000"
ACCESSTOKEN = "0"
USERTYPE = "mojang"

SYSTEM = platform.system().lower()
IS_WINDOWS = SYSTEM == "windows"
IS_LINUX = SYSTEM == "linux"

def log(text, text_box):
    text_box.insert(tk.END, f'{text}\n')
    text_box.see(tk.END)

def download_file(url, dest):
    if not os.path.isfile(dest):
        log(f"Downloading {url} -> {dest}", text_box)
        r = requests.get(url, stream=True)
        r.raise_for_status()
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        with open(dest, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)

def extract_natives(zip_path, extract_to):
    log(f"Extracting natives from {zip_path}", text_box)
    os.makedirs(extract_to, exist_ok=True)
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)

def get_version_json_url(version_id):
    manifest_url = "https://launchermeta.mojang.com/mc/game/version_manifest.json"
    log(f"manifest: {manifest_url}", text_box)
    resp = requests.get(manifest_url)
    resp.raise_for_status()
    manifest = resp.json()
    for version in manifest["versions"]:
        if version["id"] == version_id:
            return version["url"]
    raise ValueError(f"Version '{version_id}' not found in manifest")

def download_assets(index_url, asset_index_id):
    index_path = os.path.join(ASSETS_DIR, "indexes", f"{asset_index_id}.json")
    download_file(index_url, index_path)

    with open(index_path, "r") as f:
        index_data = json.load(f)

    for asset_name, asset_info in index_data["objects"].items():
        hash_val = asset_info["hash"]
        subdir = hash_val[:2]
        object_url = f"https://resources.download.minecraft.net/{subdir}/{hash_val}"
        object_path = os.path.join(ASSETS_DIR, "objects", subdir, hash_val)
        download_file(object_url, object_path)

def main():
    if os.path.exists(CLIENT_JAR):
        log(f"Instance for version {VERSION} already exists. Skipping installation.", text_box)
    else:
        os.makedirs(BASE_DIR, exist_ok=True)

        # get version metadata
        version_url = get_version_json_url(VERSION)
        version_data = requests.get(version_url).json()

        # downloads client.jar
        client_info = version_data["downloads"]["client"]
        download_file(client_info["url"], CLIENT_JAR)

        # download libraries and natives
        for lib in version_data["libraries"]:
            artifact = lib.get("downloads", {}).get("artifact")
            if artifact:
                lib_path = os.path.join(LIB_DIR, artifact["path"])
                download_file(artifact["url"], lib_path)

            classifiers = lib.get("downloads", {}).get("classifiers")
            if classifiers:
                native_key = None
                if IS_WINDOWS and "natives-windows" in classifiers:
                    native_key = "natives-windows"
                elif IS_LINUX and "natives-linux" in classifiers:
                    native_key = "natives-linux"
                if native_key:
                    native_info = classifiers[native_key]
                    native_path = os.path.join(LIB_DIR, native_info["path"])
                    download_file(native_info["url"], native_path)
                    extract_natives(native_path, NATIVES_DIR)

    version_url = get_version_json_url(VERSION)
    version_data = requests.get(version_url).json()

    jars = []
    for root, _, files in os.walk(LIB_DIR):
        for file in files:
            if file.endswith(".jar"):
                jars.append(os.path.join(root, file))
    jars.append(CLIENT_JAR)
    classpath = (";" if IS_WINDOWS else ":").join(jars)

    main_class = version_data["mainClass"]
    asset_index = version_data["assetIndex"]["id"]

    if FAST_DOWNLOAD == False:
        asset_index_info = version_data["assetIndex"]
        asset_index_url = asset_index_info["url"]
        asset_index_id = asset_index_info["id"]
        download_assets(asset_index_url, asset_index_id)

    args = [
        "--username", USERNAME,
        "--version", VERSION,
        "--gameDir", GAME_DIR,
        "--assetsDir", ASSETS_DIR,
        "--assetIndex", asset_index,
        "--uuid", UUID,
        "--accessToken", ACCESSTOKEN,
        "--userType", USERTYPE,
        "--versionType", "release",
        "--userProperties", "{}"
    ]

    java_cmd = [
        "java",
        "-Xmx2G",
        f"-Djava.library.path={NATIVES_DIR}",
        "-cp", classpath,
        main_class,
    ] + args

    log("Launching Minecraft:", text_box)
    log(" ".join(java_cmd), text_box)
    proc = subprocess.Popen(
        java_cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1
    )

    for line in proc.stdout:
        log(line.rstrip(), text_box)

class App:
    def __init__(self, root):
        self.root = root
        root.title("MClaunch")

        root.rowconfigure(0, weight=1)
        root.columnconfigure(0, weight=1)

        self.text_box = tk.Text(root, wrap='word')
        global text_box
        text_box = self.text_box
        self.text_box.grid(row=0, column=0, sticky='nsew')

        threading.Thread(target=main, daemon=True).start()

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
