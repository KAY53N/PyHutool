class File:
    @staticmethod
    def tail(self, file_path, lines=10):
        with open(file_path, 'rb') as f:
            total_lines_wanted = lines
            block_size = 1024
            f.seek(0, 2)
            block_end_byte = f.tell()
            lines_to_go = total_lines_wanted
            block_number = -1
            blocks = []
            while lines_to_go > 0 and block_end_byte > 0:
                if block_end_byte - block_size > 0:
                    f.seek(block_number * block_size, 2)
                    block = f.read(block_size)
                else:
                    f.seek(0, 0)
                    block = f.read(block_end_byte)
                lines_found = block.count(b'\n')
                lines_to_go -= lines_found
                block_end_byte -= block_size
                block_number -= 1
                blocks.append(block)
            all_read_text = b''.join(blocks)
            lines_found = all_read_text.count(b'\n')
            if lines_found > total_lines_wanted:
                return all_read_text.split(b'\n')[-total_lines_wanted:][:-1]
            else:
                return all_read_text.split(b'\n')[-lines_found:]