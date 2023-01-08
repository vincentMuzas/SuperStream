import sys, os, subprocess, json

if (len(sys.argv) < 4):
    print("Invalid argument number, exiting.")
    sys.exit(0)

search_path = sys.argv[1]
export_path = sys.argv[2]
include_subfolders = sys.argv[3] in ["yes", "1", "on"]

def export_file(path):
    target_path = export_path + "\\" + path[len(search_path) + 1: len(path)]

    """
        target_folder_path  = path to write the new files
        file_name           = name of the unmodified file
    """
    target_folder_path = target_path.split("\\")
    file_name = target_folder_path.pop()
    file_name = file_name[0:-4]
    target_folder_path = "\\".join(target_folder_path) + "\\"

    #SUBTITLES
    result = subprocess.check_output(["ffprobe", "-v", "error", "-of", "json", path, "-of", "json", "-show_entries","stream=index:stream_tags", "-select_streams", "s"])
    jsondata = json.loads(result)#.replace("\\r\\n", "\n"))
    for stream in jsondata["streams"]:
        print(stream["index"], stream["tags"]["title"])
        print("PROCESSING VIDEO", file_name)
        output_tag_title = stream["tags"]["title"]
        try:
            output_tag_lang = stream["tags"]["language"]
        except:
            output_tag_lang = "na"
        output_index = str(stream["index"])
        new_file_name = "{}.{}({}).vtt".format(file_name, output_tag_title, output_tag_lang)
        if (not os.path.exists(target_folder_path)):
            os.mkdir(target_folder_path)
        output_path = target_folder_path + new_file_name
        if (os.path.exists(output_path)):
            print("OUTPUT FILE ALREADY EXIST!")
            break
        subprocess.call(["ffmpeg", "-i", path, "-map", "0:{}".format(output_index), output_path])
    
    #AUDIO
    result = subprocess.check_output(["ffprobe", "-v", "error", "-of", "json", path, "-of", "json", "-show_entries","stream=index:stream_tags", "-select_streams", "a"])
    jsondata = json.loads(result)#.replace("\\r\\n", "\n"))
    for stream in jsondata["streams"]:
        print(stream["index"], stream["tags"]["title"])
        print("PROCESSING VIDEO", file_name)
        output_tag_title = stream["tags"]["title"]
        try:
            output_tag_lang = stream["tags"]["language"]
        except:
            output_tag_lang = "na"
        output_index = str(stream["index"])
        new_file_name = "{}.{}({}).mp3".format(file_name, output_tag_title, output_tag_lang)
        output_path = target_folder_path + new_file_name
        if (os.path.exists(output_path)):
            print("OUTPUT FILE ALREADY EXIST!")
            break
        subprocess.call(["ffmpeg", "-i", path, "-map", "0:{}".format(output_index), output_path])

    #VIDEO
    result = subprocess.check_output(["ffprobe", "-v", "error", "-of", "json", path, "-of", "json", "-show_entries","stream=index:stream_tags", "-select_streams", "v"])
    jsondata = json.loads(result)
    for stream in jsondata["streams"]:
        print(stream["index"], stream["tags"]["title"])
        print("PROCESSING VIDEO", file_name)
        output_index = str(stream["index"])
        new_file_name = "{}.mp4".format(file_name)
        output_path = target_folder_path + new_file_name
        if (os.path.exists(output_path)):
            print("OUTPUT FILE ALREADY EXIST!")
            break
        subprocess.call(["ffmpeg", "-i", path, "-map", "0:{}".format(output_index), output_path, "-c:v", "copy"])


def search_dir(path):
    dir_content = os.listdir(path)
    for elem in dir_content:
        local_path = path + '\\' + elem
        if os.path.isdir(local_path):
            search_dir(local_path)
        elif (local_path.endswith(".mkv")):
            export_file(local_path)



if __name__ == "__main__":
    search_dir(search_path)