#!/usr/bin/python
import sys
import os
import subprocess
from subprocess import Popen, PIPE, STDOUT, DEVNULL

print("N64 compiler system 1.0, written in python")

# Setup environment variables
os.environ["Path"] = 'cygwin'

# Setup paths
toolRoot = ".\\mips64-elf"
toolGNUPrefix = "\\mips64-elf-"
toolSuffix = ".exe"
toolBin  = toolRoot + "\\bin"
toolLib  = toolRoot + "\\lib"
toolInclude = toolRoot + "\\include"
toolCLib = toolRoot + "\\mips64-elf\\lib"
toolGCC = toolBin + toolGNUPrefix + "gcc" + toolSuffix
toolLD = toolBin + toolGNUPrefix + "ld" + toolSuffix
toolObj = toolBin + toolGNUPrefix + "objcopy" + toolSuffix
toolSum = toolBin + "\\chksum64" + toolSuffix
toolMkdfs = toolBin + "\\mkdfs" + toolSuffix
toolSprite = toolBin + "\\mksprite" + toolSuffix
toolN64 = toolBin + "\\n64tool" + toolSuffix
romHeaderFile = toolLib + "\\header"

def run_tool(command, args):
	print("Execute: " + command + ' ' + args)
	p = Popen(command + ' ' + args, stdout = PIPE, stderr = STDOUT, shell = True)
	out = p.communicate()
	if len(out[0]) > 0:
		print(out[0].decode())
		
def makeRom(target):
	run_tool(toolObj, target + '.elf' + ' ' + target + '.bin -O binary')
	
	try : 
		os.remove(target)
	except :
		pass
		
	run_tool(toolN64, '-b -l 2M -t ' + os.path.splitext(target + '.elf')[0] + ' h' + ' -o ' + target + '.v64 ' + target + '.bin ')
	run_tool(toolSum, target + '.v64')

# ---- Where the build system begins -----
