import os, sys
import platform
import time
from conans import tools

def system(command):
    retcode = os.system(command)
    if retcode != 0:
        raise Exception("Error while executing:\n\t %s" % command)

def sync_conan_profiles():
    conan_home_path = os.path.join(tools.get_env("HOME"), ".conan")
    if tools.get_env("CONAN_USER_HOME"):
        conan_home_path = os.path.join(tools.get_env("CONAN_USER_HOME"), ".conan")
    conan_profiles_path = os.path.join(conan_home_path, "profiles")

    # make sure conan profiles directory exist
    tools.mkdir(conan_profiles_path)

    for root, dirs, files in os.walk(os.path.abspath("buildtools/conan-profiles")):
        for f in files:
            src = os.path.join(root, f)
            dst = os.path.join(conan_profiles_path, f)
            if os.path.islink(dst) and os.path.realpath(dst) == src:
                # symlink already correct, nothing need to change
                continue
            if os.path.isfile(dst):
                os.remove(dst)    
            os.symlink(src, dst)
            print("created symlink: {} -> {}".format(dst, src))

if __name__ == "__main__":
    params = " ".join(sys.argv[1:])

    # sync project conan profiles on host 
    sync_conan_profiles()

    submodules = ["third-party/boringssl", "third-party/ffmpeg"]

    if platform.system() == "Linux" or platform.system() == "Darwin":
        for s in submodules:
            print("Start module building: " + s)
            start_time = time.time()

            build_path = s+"/build"
            tools.mkdir(build_path)
            with tools.chdir(build_path):
                system('conan create .. --build=missing ' + params)

            print("End module building: {0}, elapsed_time: {1} seconds".format(s, time.time() - start_time))
    else:
        pass
