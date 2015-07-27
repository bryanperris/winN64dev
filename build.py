#!/usr/bin/python
import sys
import os
import subprocess
from subprocess import Popen, PIPE, STDOUT

print("N64 compiler system 1.0, written in python")

# Setup environment variables
#os.environ["PATH"] += ";cygwin;"

# Setup paths
toolRoot = "mips64-elf"
toolGNUPrefix = "/mips64-elf-"
toolSuffix = ".exe"
toolBin  = toolRoot + "/bin"
toolLib  = toolRoot + "/lib"
toolInclude = toolRoot + "/include"
toolCLib = toolRoot + "/mips64-elf/lib"
toolGCC = toolBin + toolGNUPrefix + "gcc" + toolSuffix
toolLD = toolBin + toolGNUPrefix + "ld" + toolSuffix
toolObj = toolBin + toolGNUPrefix + "objcopy" + toolSuffix
toolSum = toolBin + "/chksum64" + toolSuffix
toolMkdfs = toolBin + "/mkdfs" + toolSuffix
toolSprite = toolBin + "/mksprite" + toolSuffix
toolN64 = toolBin + "/n64tool" + toolSuffix
romHeaderFile = toolLib + "/header"

def run_tool(command, args):
        print("Execute: " + command + " " + args)
        p = Popen(
            [command, args],
            stdout = PIPE,
            stdin = PIPE,
            stderr = STDOUT,
            shell = True)
        out, err = p.communicate()
        print(out[0].decode())


# ---- Where the build system begins -----
run_tool(toolN64, '')
