[app]

title = SMS Sender
package.name = smssender
package.domain = com.goldenboyi
source.dir = .
source.include_exts = py,kv,png,jpg,atlas
version = 0.1.0
requirements = python3,kivy,pyjnius
orientation = portrait
fullscreen = 0

android.permissions = SEND_SMS
android.api = 35
android.minapi = 24
android.ndk = 27b
android.archs = arm64-v8a, armeabi-v7a
p4a.branch = develop
android.accept_sdk_license = True

[buildozer]
log_level = 2
warn_on_root = 1
