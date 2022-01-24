import os
import time

tag = '[SCE-TTS-REPAIR-MERGE] '
		
def log(txt, level="Info"):
	print('['+str(level)+'] '+tag+str(txt))

log("SCE-TTS-Repair-Merge has been started!")

upward_file_list = os.listdir('..')
not_founded = True
detected_version = "None"
for upward_file in upward_file_list:
	if upward_file == 'server.exe' or upward_file == 'run-server.bat':
		detected_version = "V2"
		not_founded = False
		break
	if upward_file == 'start-windows.bat' or upward_file == 'docker-compose.yml' \
		or upward_file == 'Dockerfile' or upward_file == 'generate_ljs_audio_text.py':
		detected_version = "V1"
		not_founded = False
		break

log(f"SCE-TTS `{detected_version}` Version Detected.")
if detected_version == "None" or not_founded:
	log("Is this script located in the 'audio_files' folder?", "Error")
	os._exit(1)

folder_list = os.listdir('.')
if (len(folder_list) - 1) == 0:
	log("The path could not be found.", "Warning")

i = 0
new_folder_list = []

for folder in folder_list:
	if folder == os.path.basename(__file__):
		continue

	if os.path.isdir(folder):
		i += 1
		new_folder_list.append(folder)
		log(f"`{i}` - `{folder}`")

a = input("Please Select to merge metadata: ")
while not (a.isdigit() and int(a)-1 < len(new_folder_list)):
	a = input("Please Select to merge metadata: ")

folder = new_folder_list[int(a)-1]

if os.path.exists(folder):
	abs_folder = os.path.abspath(folder)
	current = os.path.join(abs_folder, f'{folder}-current.txt')
	merge_metadata = os.path.join(abs_folder, f'{folder}-metadata.txt')

	if os.path.exists(current):
		f = open(current, "r", encoding="utf-8")
		i = f.read()
		f.close()

		f = open(merge_metadata, "w", encoding="utf-8")
		data = ""
		
		for x in range(int(i)-1):
			x += 1
			metadata = f'{folder}-metadata_{str(x)}.txt'
			metadata_file = open(os.path.join(abs_folder, metadata), "r", encoding="utf-8")
			data += metadata_file.read()
			log(f"`{metadata}` file readed and data writed.")
			metadata_file.close()

		f.write(data)
		log(f"Data was writed at file.")
		f.close()
	else:
		log("Current State File isn't Exists.", "Error")
		os._exit(1)
else:
	log("Folder isn't Exists.", "Error")
	os._exit(1)

log("Merge Done.")
