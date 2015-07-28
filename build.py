#!/usr/bin/python
import sys
import os
import subprocess
from subprocess import Popen, PIPE, STDOUT, DEVNULL

print("N64 compiler system 1.0, written in python")

if len(sys.argv) < 2:
	raise ValueError('Need to provide valid path to project directory')
	
if os.path.isdir(sys.argv[1]) != True:
	raise ValueError('Provided project path is not a valid directory')

# Get the project folder path
projectPath = sys.argv[1]
projectConfigPath = projectPath + '\\_N64_CONFIG.py'

if os.path.isfile(projectConfigPath) != True:
	raise ValueError('Project directory does not contain a build config')
	
# Get working directory
workingDir = os.path.dirname(os.path.realpath(__file__))

# Setup environment variables
os.environ["Path"] = workingDir + '\\cygwin'

# Setup paths
toolRoot = workingDir + "\\mips64-elf"
toolGNUPrefix = "\\mips64-elf-"
toolSuffix = ".exe"
toolBin  = toolRoot + "\\bin"
toolGCC = toolBin + toolGNUPrefix + "gcc" + toolSuffix
toolLD = toolBin + toolGNUPrefix + "ld" + toolSuffix
toolObj = toolBin + toolGNUPrefix + "objcopy" + toolSuffix
toolSum = toolBin + "\\chksum64" + toolSuffix
toolMkdfs = toolBin + "\\mkdfs" + toolSuffix
toolSprite = toolBin + "\\mksprite" + toolSuffix
toolN64 = toolBin + "\\n64tool" + toolSuffix
romHeaderFile = toolRoot + "\\lib\\header"

def run_tool(command, args):
	print("Execute: " + command + ' ' + args)
	p = Popen(command + ' ' + args, stdout = PIPE, stderr = STDOUT, shell = True)
	out = p.communicate()
	if len(out[0]) > 0:
		print(out[0].decode())
		
def makeRom(target, romName):
	run_tool(toolObj, target + '.elf' + ' ' + target + '.bin -O binary')
	
	try : 
		os.remove(target)
	except :
		pass
		
	run_tool(toolN64, '-b -l 2M -t \"' + romName + '\" -h ' + romHeaderFile + ' -o ' + target + '.v64 ' + target + '.bin')
	run_tool(toolSum, target + '.v64')

# ---- Where the build system begins -----

# Load the build config
exec(open(projectConfigPath).read(), globals())

# Change working directory to project path
os.chdir(projectPath)

if not 'TARGETS' in globals():
	raise ValueError('TARGETS was not defined in config')
	
# Interate through each target and build them
for target in globals()['TARGETS']:
	targetData = globals()['TARGETS'][target]
	romName = ""
	print('building target: ' + target)
	
	# Get the ROM name
	if 'NAME' in targetData:
		romName = targetData['NAME']
	else:
		romName = 'Unknown'
		
	print('ROM Name: ' + romName)
	
	# Build a space delimited list input files and output files
	if not 'SOURCES' in targetData:
		raise ValueError('SOURCES was not defined in target')
	else:
		ifiles = ""
		ofiles = ""
		for source in targetData['SOURCES']:
			ifiles += ' ' + source
			ofiles += ' ' + source.replace('.c', '.o')
	
	# Execute the C Compiler
	GCCPreArgs = '-std=gnu99 -march=vr4300 -mtune=vr4300 -G0 -Wall -Werror -I(ROOTDIR)/include -I(ROOTDIR)/mips64-elf/include -c'
	GCCPreArgs = GCCPreArgs.replace('(ROOTDIR)', toolRoot)
	run_tool(toolGCC, GCCPreArgs + ifiles)
	
	# Link objects into elf executable
	LDPreArgs = '-G0 -L(ROOTDIR)/lib -L(ROOTDIR)/mips64-elf/lib'
	LDPreArgs = LDPreArgs.replace('(ROOTDIR)', toolRoot)
	linkLibs = '-ldragon -lc -lm -ldragonsys -Tn64ld.x'
	run_tool(toolLD, LDPreArgs + ofiles + ' -o ' + target + '.elf ' + linkLibs)
	
	# Build the rom
	makeRom(target, romName)
	
	# Remove immediate files
	filelist = [ f for f in os.listdir(".") if f.endswith(".o") or f.endswith(".bin") or f.endswith(".elf")]
	for f in filelist:
		os.remove(f)
	

