import os, sys
import platform
import time
from conans import tools

def system(command):
    retcode = os.system(command)
    if retcode != 0:
        raise Exception("Error while executing:\n\t %s" % command)

if __name__ == "__main__":
    params = " ".join(sys.argv[1:])

    submodules = ["third-party/boringssl", "third-party/ffmpeg"]

    if platform.system() == "Linux":
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
