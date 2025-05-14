import os
import shutil
import stat


def handle_remove_readonly(func, path, _):
    os.chmod(path, stat.S_IWRITE)
    func(path)


def safe_rmdir(path):
    if os.path.exists(path):
        print(f"Removing {path}")
        shutil.rmtree(path, onerror=handle_remove_readonly)


def safe_remove(path):
    if os.path.isfile(path):
        print(f"Removing {path}")
        os.remove(path)


if __name__ == "__main__":
    safe_rmdir("build")
    safe_rmdir("dist")

    # Remove all *.egg-info folders
    for folder in os.listdir("."):
        if folder.endswith(".egg-info"):
            safe_rmdir(folder)

    print("✅ Build folders cleaned.")
