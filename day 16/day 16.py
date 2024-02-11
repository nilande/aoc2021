import sys, os
sys.path.append(os.getcwd())
from aoc_utils import input_handling
from functools import reduce

#
# Classes
#
class Packet:
    OPERATOR_SUM = 0
    OPERATOR_PRODUCT = 1
    OPERATOR_MINIMUM = 2
    OPERATOR_MAXIMUM = 3
    LITERAL = 4
    OPERATOR_GREATER_THAN = 5
    OPERATOR_LESS_THAN = 6
    OPERATOR_EQUAL_TO = 7

    def __init__(self, bits: str) -> None:
        version = int(bits[0:3], 2)
        self.version_sum = version
        packet_type = int(bits[3:6], 2)
        match packet_type:
            case Packet.LITERAL:
                i = 6
                self.number = 0
                while True:
                    self.number |= int(bits[i+1:i+5], 2)
                    if bits[i] == '0': break
                    self.number <<= 4
                    i += 5
                self.remaining_bits = bits[i+5:]
            case _:         # Any kind of operator packet
                length_type_id = bits[6]
                numbers = []
                match length_type_id:
                    case '0':   # Total length in bits given
                        total_length = int(bits[7:7+15], 2)
                        remaining_bits = bits[7+15:7+15+total_length]
                        while len(remaining_bits) > 0:
                            packet = Packet(remaining_bits)
                            numbers.append(packet.number)
                            self.version_sum += packet.version_sum
                            remaining_bits = packet.remaining_bits
                        self.remaining_bits = bits[7+15+total_length:]
                    case '1':   # Number of sub packets given
                        number_of_sub_packets = int(bits[7:7+11], 2)
                        remaining_bits = bits[7+11:]
                        packets_count = 0
                        while packets_count < number_of_sub_packets:
                            packet = Packet(remaining_bits)
                            numbers.append(packet.number)
                            self.version_sum += packet.version_sum
                            remaining_bits = packet.remaining_bits
                            packets_count += 1
                        self.remaining_bits = remaining_bits

                match packet_type:
                    case Packet.OPERATOR_SUM: self.number = sum(numbers)
                    case Packet.OPERATOR_PRODUCT: self.number = reduce(lambda a, b: a * b, numbers)
                    case Packet.OPERATOR_MINIMUM: self.number = min(numbers)
                    case Packet.OPERATOR_MAXIMUM: self.number = max(numbers)
                    case Packet.OPERATOR_GREATER_THAN: self.number = int(numbers[0] > numbers[1])
                    case Packet.OPERATOR_LESS_THAN: self.number = int(numbers[0] < numbers[1])
                    case Packet.OPERATOR_EQUAL_TO: self.number = int(numbers[0] == numbers[1])

#
# Process input
#
packet_hex = input_handling.read_from_file('day 16/input.txt')
packet_bits = ''
for h in packet_hex.strip(): packet_bits += f'{int(h, 16):04b}'

packet = Packet(packet_bits)

print(f'Puzzle 1 solution is: {packet.version_sum}')
print(f'Puzzle 2 solution is: {packet.number}')