#!/bin/bash
cp cloudhelper_*.py files_launcher/
tar -zcvf files_worker.tar.gz files_worker
cp files_worker.tar.gz ./files_launcher/
tar -zcvf files_launcher.tar.gz files_launcher
