import subprocess
import xmltodict
import argparse
import sys

parser = argparse.ArgumentParser(description='Get GPU process info')
parser.add_argument("-n", type=int, default=1,
                    	help='nth process to query from top GPU processes')
parser.add_argument("--name", default=False, action="store_true",
                    	help='print only the name of the process')
parser.add_argument("--memory", default=False, action="store_true",
                    	help='print only the name of the process')
args = parser.parse_args()

output = subprocess.check_output(['nvidia-smi', '-q','-x']).decode()
parsed = xmltodict.parse(output)

processes = parsed['nvidia_smi_log']['gpu']['processes']['process_info']
totalProcesses = len(processes)

if args.n > totalProcesses:
	print("Can only see upto {} processes".format(totalProcesses))
	sys.exit()

process = processes[args.n-1]
processName = process['process_name']
processName = processName.split(' ')[0].split('/')[-1]
processMemory = process['used_memory']

if args.name is True and args.memory is False: print(processName)
elif args.name is False and args.memory is True: print(processMemory)
else: print((processName, processMemory))