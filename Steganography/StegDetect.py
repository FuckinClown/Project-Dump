import shutil, os

choice = input("|1| Hide Files |2| Detect Hidden File\n~> ")
match choice:
    case "1":
        fweahPath = input("Path to Folder to hide\n~> ")
        fienPath = input("Path to Img\n~> ")
        shutil.make_archive("output", 'zip', fweahPath) # gotta be a .zip file
        os.system(f"copy /b {fienPath}+output.zip output.png") # downloading rat...
        os.system("del output.zip") # Some clean up
        print("Done! Files hidden in output.png")
    case "2":
        filename = input("Suspected file: ")
        try:
            RawBytes = open(filename, "rb").read()
            if str(RawBytes).endswith("IEND\\xaeB`\\x82'"):
                print("No hidden files (probably)")
            else:
                try:
                    print("Hidden files, extracting...")
                    os.system(f"tar -xf \"{filename}\"")
                    print("Extracted to: "+os.getcwd())
                except Exception as e:
                    print(f"Error: {e}")
        except Exception as e:
            print(f"Error: {e}")
input("\nPress enter to continue...")