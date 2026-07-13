.# SHAHRAM V2

[app]

title = Shahram Downloader

package.name = shahramdownloader

package.domain = org.shahram

source.dir = .

source.include_exts = py,png,jpg,kv,atlas,html,ttf

version = 1.0

requirements = python3,kivy,pyjnius,yt-dlp,arabic_reshaper,python-bidi==0.4.2,requests,certifi,six,urllib3,charset-normalizer,idna,mutagen,brotli,websockets

orientation = portrait

fullscreen = 0

android.permissions = INTERNET, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE, MANAGE_EXTERNAL_STORAGE

android.api = 33

android.minapi = 24

android.archs = arm64-v8a, armeabi-v7a

android.allow_backup = True

android.add_assets = webapp

[buildozer]

log_level = 2

warn_on_root = 1
