class RomBuffer:
    def __init__(self, file_contents):
        self.data = []
        buffer = file_contents

        for i in range(0, len(buffer), 2):
            self.data.push((buffer[i] << 8) | (buffer[i+1] << 0))
