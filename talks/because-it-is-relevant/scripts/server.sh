#!/usr/bin/sh
socat -ddd tcp-listen:7777,reuseaddr system:"python3 upper.py"
