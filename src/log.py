import json

class Log:

    def __init__(self, filepath):
        self.filepath = filepath

    def log(self, message):
        with open(self.filepath, 'w') as f:
            f.write(message + '\n')

    def append(self, message):
        with open(self.filepath, 'a+') as f:
            f.write(message + '\n')
    
    def append_dict(self, out_dict):
        with open(self.filepath, 'a+') as f:
            out = json.dumps(out_dict)
            f.write(out)

    def log_dict(self, out_dict):
        with open(self.filepath, 'w') as f:
            out = json.dumps(out_dict)
            f.write(out)

    def log_dict_second(self, out_dict, score):
        with open(self.filepath, 'a') as f:
            out = json.dumps(out_dict)
            f.write(out + " " + str(score) + '\n')

    def readlines(self):
        with open(self.filepath, 'r') as f:
            lines = f.readlines()
            return lines
        return None

    def readDict(self):
        
        with open(self.filepath, 'r') as f:
            in_dict = json.load(f)

        return in_dict

catan_log = Log("log.txt")
