[app]

# (str) Title of your application
title = Shahram Downloader

# (str) Package name
package.name = shahramdownloader

# (str) Package domain (needed for android packaging)
package.domain = org.shahram

# (str) Source code directory
source.dir = .

# (list) Source files to include (let's keep it clean)
source.include_exts = py,png,jpg,kv,atlas,html,ttf

# (str) Application versioning
version = 1.0

# (list) Application requirements
# Added hostpython3 to make compiling process smoother
requirements = python3,hostpython3,kivy,pyjnius,yt-dlp,arabic_reshaper,python-bidi==0.4.2,requests,certifi,six,urllib3,charset-normalizer,idna,mutagen,brotli,websockets

# (str) Supported orientations
orientation = portrait

# (bool) Use fullscreen or not
fullscreen = 0

# (list) Permissions
android.permissions = INTERNET, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE, MANAGE_EXTERNAL_STORAGE

# (int) Target Android API, should be as high as possible.
android.api = 33

# (int) Minimum API your APK will support.
android.minapi = 24

# (list) The Android archs to build for.
android.archs = arm64-v8a, armeabi-v7a

# (bool) Allow Google to back up your app's data
android.allow_backup = True

# (list) Assets to add
android.add_assets = webapp

# ---------------------------------------------------------
# بخش‌های نجات‌بخش برای حل خطای کامپایل Harfbuzz:
# ---------------------------------------------------------

# ۱. استفاده از یک نسخه کاملاً پایدار و تست‌شده از NDK که با کیوی سازگار است
android.ndk = 23b

# ۲. غیرفعال کردن خطاهای سخت‌گیرانه فرمت امنیتی در زمان کامپایل کدهای C/C++
android.extra_arguments = --env CFLAGS="-Wno-error=format-security" --env CXXFLAGS="-Wno-error=format-security"

# ---------------------------------------------------------

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 1
