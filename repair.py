import os
import time
import threading

tag = '[SCE-TTS-REPAIR] '

class Worker(threading.Thread):
	"""docstring for Worker"""
	def __init__(self, folder):
		super().__init__()
		self.folder = folder

	def run(self):
		abs_folder = os.path.abspath(self.folder)
		current = os.path.join(abs_folder, f'{self.folder}-current.txt')
		metadata = os.path.join(abs_folder, f'{self.folder}-metadata.txt')

		while True:
			while not os.path.exists(metadata):
   				time.sleep(2)
			if os.path.exists(metadata):
				log("A new metadata file has been founded.")
	
				i = 1
				f = open(current, "a+")
				f.seek(0)
				if os.path.getsize(current) > 0:
					i = f.read()
					log("Loaded current state file data.")
				else:
					log("Cureent state file is empty. Make a new file.")
	
				new_metadata = f'{self.folder}-metadata_{str(i)}.txt'
				new_metadata_file = os.path.join(abs_folder, new_metadata)
	
				try:
					os.rename(metadata, new_metadata_file)
				except FileExistsError as e:
					log("FileExistsError occured. Skipped", "Error")
				else:
					log(f"Renamed to `{new_metadata}`. Repaired Succesfully!")
				finally:
					f.seek(0)
					f.truncate()
					f.write(str(int(i) + 1))
					f.close()
					log("Saved current state file data.")
		

def log(txt, level="Info"):
	print('['+str(level)+'] '+tag+str(txt))

log("SCE-TTS-Repair has been started!")

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

for folder in folder_list:
	if folder == os.path.basename(__file__):
		continue

	if os.path.isdir(folder):
		log(f"Thread for folder `{folder}` was started.")
		t = Worker(folder)
		t.start()

log("All Thread was started.")
