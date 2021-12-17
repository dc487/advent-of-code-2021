import pathlib
from functools import reduce
import operator

class _Packet:
    def __init__(self, bytes):
        self.child_packets = []
        self.version = int(bytes.pop(0) + bytes.pop(0) + bytes.pop(0), 2)
        self.type_id = int(bytes.pop(0) + bytes.pop(0) + bytes.pop(0), 2)

        if self.type_id == 4:
            value = ''
            while (bytes.pop(0) == '1'):
                value += bytes.pop(0) + bytes.pop(0) + bytes.pop(0) + bytes.pop(0)
            value += bytes.pop(0) + bytes.pop(0) + bytes.pop(0) + bytes.pop(0)
            self.literal_value = int(value, 2)
        else:
            self.length_type_id = bytes.pop(0)
            if self.length_type_id == '0':
                length_string = ''
                for i in range(15):
                    length_string += bytes.pop(0)
                length = int(length_string, 2)
                initial_byte_length = len(bytes)
                while (initial_byte_length - len(bytes) < length):
                    self.child_packets.append(_Packet(bytes))
            else:
                packet_number_string = ''
                for i in range(11):
                    packet_number_string += bytes.pop(0)
                packet_number = int(packet_number_string, 2)
                for i in range(packet_number):
                    self.child_packets.append(_Packet(bytes))

    def get_version_count(self):
        version_count = self.version
        for packet in self.child_packets:
            version_count += packet.get_version_count()

        return version_count

    def get_value(self):
        if self.type_id == 4:
            return self.literal_value

        child_packet_values = [x.get_value() for x in self.child_packets]
        if self.type_id == 0:
            return sum(child_packet_values)
        elif self.type_id == 1:
            return reduce(operator.mul, child_packet_values, 1)
        elif self.type_id == 2:
            return min(child_packet_values)
        elif self.type_id == 3:
            return max(child_packet_values)
        elif self.type_id == 5:
            return 1 if child_packet_values[0] > child_packet_values[1] else 0
        elif self.type_id == 6:
            return 1 if child_packet_values[0] < child_packet_values[1] else 0
        elif self.type_id == 7:
            return 1 if child_packet_values[0] == child_packet_values[1] else 0



def load_input():
    return pathlib.Path("./input.txt").read_text().strip("\n").splitlines()

if __name__ == "__main__":
    input = load_input()

    input_bits = []
    for character in input[0]:
        for bit in bin(int(character, 16))[2:].zfill(4):
            input_bits.append(bit)

    packet = _Packet(input_bits)
    print(packet.get_version_count())
    print(packet.get_value())
    
    
