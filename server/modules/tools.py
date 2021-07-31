class tool:
    def data_loader(file_path_to_read_and_write):
        arr = []
        file = open(file_path_to_read_and_write,"r")
        for i in file.readlines():
            i = i.replace("\n","")
            if i=="\n":
                pass
            else:
                arr.append(i)
        file.close()
        del file
        return arr[0],arr[1],arr[2]