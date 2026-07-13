[app]

# (str) Title of your application
title = Shahram-downloader

# (str) Package name
package.name = shahramdownloader

# (str) Package domain (needed for android packaging)
package.domain = org.test

# (str) Source code directory
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas

# (list) List of inclusions using pattern matching
#source.include_patterns = assets/*,images/*.png

# (list) Source files to exclude (let empty to not exclude any file)
#source.exclude_exts = spec

# (list) List of directory to exclude (let empty to not exclude any dir)
#source.exclude_dirs = tests, bin, venv

# (list) List of exclusions using pattern matching
#source.exclude_patterns = license,images/*/*_code.png

# (html) Path to custom html template
#html.template = 

# (str) Application versioning (method 1)
version = 0.1

# (str) Application versioning (method 2)
# version.regex = __version__ = ['"](.*)['"]
# version.filename = %(source.dir)s/main.py

# (list) Application requirements
# comma separated e.g. requirements = sqlite3,kivy
requirements = python3,hostpython3,kivy,pyjnius,yt-dlp,arabic_reshaper,python-bidi,certifi,six,urllib3,charset-normalizer,idna,mutagen,brotli,websockets

# (str) Custom source folders for requirements
# It should be all the folders you want to include with source
# This is equivalent to add the paths to sys.path at startup.
#source.custom_libs =

# (str) Presplash of the application
#presplash.filename = %(source.dir)s/data/presplash.png

# (str) Icon of the application
#icon.filename = %(source.dir)s/data/icon.png

# (str) Supported orientations (one of landscape, sensorLandscape, portrait or all)
orientation = portrait

# (list) List of service to declare
#services = MyService:%(source.dir)s/service.py

#
# Android specific
#

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (string) Presplash background color (for android toolchain)
# Supported formats are: #RRGGBB #AARRGGBB or a registered color name (eg: lightblue)
#android.presplash_color = #FFFFFF

# (string) Presplash animation using Lottie format.
# android.presplash_lottie = %s/dir/to/lottie.json

# (list) Permissions
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE,MANAGE_EXTERNAL_STORAGE

# (list) features (for android toolchain)
#android.features = android.hardware.usb.host

# (int) Target Android API, should be as high as possible.
android.api = 33

# (int) Minimum API your APK will support.
android.minapi = 24

# (int) Android SDK version to use
#android.sdk = 20

# (str) Android NDK version to use
android.ndk = 25c

# (int) Android NDK API to use. This is the minimum API your app will support, it should usually match android.minapi.
#android.ndk_api = 21

# (bool) Use --private data directory (True, default) or --dir public storage directory (False)
#android.private_storage = True

# (str) Android NDK directory (if empty, it will be automatically downloaded.)
#android.ndk_path =

# (str) Android SDK directory (if empty, it will be automatically downloaded.)
#android.sdk_path =

# (str) ANT directory (if empty, it will be automatically downloaded.)
#android.ant_path =

# (str) pimpl version to use (if empty, the latest version will be used.)
#android.pimpl_version =

# (list) Python recipes to add
#android.add_recipes =

# (list) The Android archs to build for.
android.archs = arm64-v8a, armeabi-v7a

# (bool) Allow google to backup your app data
android.allow_backup = True

# (list) List of extra libraries to copy into the apk
#android.add_libs_armeabi_v7a = libs/armeabi-v7a/libgpg.so
#android.add_libs_arm64_v8a = libs/arm64-v8a/libgpg.so

# (list) List of Java .jar files to add to the libs so that pyjnius can access
#android.add_jars = foo.jar:bar.jar

# (list) List of Java .jar files to add to the classpath (for compilation)
#android.add_javaclasspath = foo.jar:bar.jar

# (list) Java sources to compile
#android.add_src =

# (list) Android AAR archives to add
#android.add_aars =

# (list) Gradle dependencies to add
#android.add_gradle_deps =

# (list) Packaging rules to apply
#android.packaging_rules =

# (list) Java compiler arguments
#android.javac_args =

# (list) Gradle arguments
#android.gradle_args =

# (list) Android extra arguments
android.extra_args = --envCF="-Wno-error=format-security"

# (list) Assets to add
#android.add_assets = 

#-----------------------------------------------------------------------------
# Harfbuzz sections for fixing compile error
#-----------------------------------------------------------------------------

# (int) Log level (0 = error only, 1 = info, 2 = debug and up)
log_level = 2

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 1
