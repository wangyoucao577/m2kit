# rtc-core
Mono repo for RTC development.

## Building 

### Prerequisites
- latest `cmake`, `ninja`
- latest `conan`
- latest `gcc`/`clang`/`MSVC` depends on your OS

### Update submodules
```bash
$ git submodule update --init
```

### Building on Linux
```bash
$ python build.py
```

### Building for Android
```bash
$ # set your android ndk
$ export ANDROID_NDK_HOME=/usr/local/android-ndk-r21e
$ 
$ python build.py -s arch=armv8 -s os=Android -s os.api_level=21 -s compiler=clang -s compiler.version=9 -s compiler.libcxx=c++_static
```

### Building for iOS
TODO: 