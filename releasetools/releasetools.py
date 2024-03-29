# Copyright (C) 2019 LineageOS Project
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import subprocess

ANDROID_BUILD_TOP = os.getenv('ANDROID_BUILD_TOP')
DEVICE_VENDOR_DIR = os.path.join(ANDROID_BUILD_TOP, 'vendor', 'samsung', 'serranovexx', 'dtimages')
INSTALL_MY_PATH = os.path.join('install', 'dtimage')

def FullOTA_InstallEnd(self):
  AddFirmwareFlash(self, self.input_zip)

def IncrementalOTA_InstallEnd(self):
  AddFirmwareFlash(self, self.target_zip)

def AddFirmwareFlash(self, input_zip):
  """Include required binaries to the output zip"""
  self.output_zip.write(os.path.join(DEVICE_VENDOR_DIR, 'dtlte.img'), os.path.join(INSTALL_MY_PATH, 'dtlte.img'))
  self.output_zip.write(os.path.join(DEVICE_VENDOR_DIR, 'dt3g.img'), os.path.join(INSTALL_MY_PATH, 'dt3g.img'))
  self.output_zip.write(os.path.join(DEVICE_VENDOR_DIR, 'kernel_make.sh'), os.path.join(INSTALL_MY_PATH, 'kernel_make.sh'))
  self.output_zip.write(os.path.join(DEVICE_VENDOR_DIR, 'kernel_unpack.sh'), os.path.join(INSTALL_MY_PATH, 'kernel_unpack.sh'))
  self.output_zip.write(os.path.join(DEVICE_VENDOR_DIR, 'mkbootimg'), os.path.join(INSTALL_MY_PATH, 'mkbootimg'))
  self.output_zip.write(os.path.join(DEVICE_VENDOR_DIR, 'unpackbootimg'), os.path.join(INSTALL_MY_PATH, 'unpackbootimg'))
  """Core script to flash dt images"""
  self.script.AppendExtra('if is_substring("I9192I", getprop("ro.bootloader")) || is_substring("I9195I", getprop("ro.bootloader")) then')
  self.script.AppendExtra('ui_print("Hardware is not default, tuning kernel...");')

  self.script.AppendExtra('package_extract_dir("install/dtimage", "/tmp/dtimage");')
  self.script.AppendExtra('set_metadata_recursive("/tmp/dtimage/", "uid", 0, "gid", 0, "fmode", 0777);')
  self.script.AppendExtra('run_program("/tmp/dtimage/kernel_unpack.sh");')

  self.script.AppendExtra('ifelse(is_substring("I9195I", getprop("ro.bootloader")), ui_print("Hardware detected: I9195I"));')
  self.script.AppendExtra('ifelse(is_substring("I9195I", getprop("ro.bootloader")), run_program("/sbin/sh", "-c", "busybox cp -f /tmp/dtimage/dtlte.img /tmp/dtimage/out/boot.img-dt"));')

  self.script.AppendExtra('if is_substring("I9192I", getprop("ro.bootloader")) then')
  self.script.AppendExtra('ui_print("Hardware detected: I9192I");')
  self.script.AppendExtra('run_program("/sbin/sh", "-c", "busybox cp -f /tmp/dtimage/dt3g.img /tmp/dtimage/out/boot.img-dt");')
  self.script.Mount("/system")
  self.script.AppendExtra('run_program("/sbin/sh", "-c", "busybox rm -f /system/vendor/etc/permissions/*nfc*");')
  self.script.Unmount("/system")
  self.script.AppendExtra('endif;')

  self.script.AppendExtra('run_program("/tmp/dtimage/kernel_make.sh");')
  self.script.AppendExtra('ui_print("Kernel successfully adapted to the new hardware");')
  self.script.AppendExtra('endif;')

