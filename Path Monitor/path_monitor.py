# Orginal:
# http://timgolden.me.uk/python/win32_how_do_i/watch_directory_for_changes.
import tempfile
import threading
import win32file
import win32con
import os


dirs_to_monitor = ["C:\\WINDOWS\\Temp",f"C:\\Users\\{os.getlogin()}\\Desktop",tempfile.gettempdir()]

# file modification constants
FILE_CREATED = 1
FILE_DELETED = 2
FILE_MODIFIED = 3
FILE_RENAMED_FROM = 4
FILE_RENAMED_TO = 5

def observe(path):
    FILE_LIST_DIRECTORY = 0x0001
    h_directory = win32file.CreateFile(
        path,
        FILE_LIST_DIRECTORY,
        win32con.FILE_SHARE_READ | win32con.FILE_SHARE_WRITE | win32con.FILE_SHARE_DELETE,
        None,
        win32con.OPEN_EXISTING,
        win32con.FILE_FLAG_BACKUP_SEMANTICS,
        None)
    while 1:
        try:
            results = win32file.ReadDirectoryChangesW(
                h_directory,
                1024,
                True,
                win32con.FILE_NOTIFY_CHANGE_FILE_NAME |
                win32con.FILE_NOTIFY_CHANGE_DIR_NAME |
                win32con.FILE_NOTIFY_CHANGE_ATTRIBUTES |
                win32con.FILE_NOTIFY_CHANGE_SIZE |
                win32con.FILE_NOTIFY_CHANGE_LAST_WRITE |
                win32con.FILE_NOTIFY_CHANGE_SECURITY,
                None,
                None
                )
            for action,file_name in results:
                full_filename = os.path.join(path, file_name)
                if action == FILE_CREATED:
                    print (f"[ + ] Created {full_filename}")
                elif action == FILE_DELETED:
                    print (f"[ - ] Deleted {full_filename}")
                elif action == FILE_MODIFIED:
                    print (f"[ * ] Modified {full_filename}")
                # dump out the file contents
                    print ("[vvv] Dumping contents...")
                    try:
                        fd = open(full_filename,"rb")
                        contents = fd.read()
                        fd.close()
                        print (contents)
                        print ("[^^^] Dump complete.")
                    except:
                        print ("[!!!] Failed.")
                elif action == FILE_RENAMED_FROM:
                    print (f"[ > ] Renamed from: {full_filename}")
                elif action == FILE_RENAMED_TO:
                    print (f"[ < ] Renamed to: {full_filename}")
                else:
                    print (f"[???] Unknown: {full_filename}")
        except:
            pass

for path in dirs_to_monitor:
    monitor_thread = threading.Thread(target=observe,args=(path,))
    print (f"Spawning monitoring thread for path: {path}")
    monitor_thread.start()
