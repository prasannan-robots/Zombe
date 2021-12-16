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

# Just to create a single object instead of whole array :)
class clients:
    def __init__(self,connection,address,public_key):
        self.connection = connection
        self.address = address
        self.public_key = public_key
    