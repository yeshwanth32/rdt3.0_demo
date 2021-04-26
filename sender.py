import socket
import sys
from datetime import datetime

def checksum(msg):
    """
     This function calculates checksum of an input string
     Note that this checksum is not Internet checksum.

     Input: msg - String
     Output: String with length of five
     Example Input: "1 0 That was the time fo "
     Expected Output: "02018"
    """

    # step1: covert msg (string) to bytes
    msg = msg.encode("utf-8")
    s = 0
    # step2: sum all bytes
    for i in range(0, len(msg), 1):
        s += msg[i]
    # step3: return the checksum string with fixed length of five
    #        (zero-padding in front if needed)
    return format(s, '05d')

def checksum_verifier(msg):
    """
     This function compares packet checksum with expected checksum

     Input: msg - String
     Output: Boolean - True if they are the same, Otherwise False.
     Example Input: "1 0 That was the time fo 02018"
     Expected Output: True
    """

    expected_packet_length = 30
    # step 1: make sure the checksum range is 30
    if len(msg) < expected_packet_length:
        return False
    # step 2: calculate the packet checksum
    content = msg[:-5]
    calc_checksum = checksum(content)
    expected_checksum = msg[-5:]
    # step 3: compare with expected checksum
    if calc_checksum == expected_checksum:
        return True
    return False

def get_first_200_characters(filename):
    file = open(filename, 'r')
    i = 0
    message = ""
    while 1:
        char = file.read(1)
        if not char or i == 200:
            break
        message += char
        i += 1
    file.close()
    return message

def unpack_response(response):
    seq_number = response[0:1]
    ack_number = response[2:3]
    message = response[4:-6]
    checksum = response[-5:]
    return (seq_number, ack_number, message, checksum)


def make_packet(sequence_number = " ", ack_number = " ", payload = "                    "):
    packet_without_checksum = str(sequence_number) + " " + str(ack_number) + " " + str(payload) + " "
    packet_checksum = checksum(packet_without_checksum)
    packet = packet_without_checksum + str(packet_checksum)
    if (len(packet) != 30):
        print("Error!!")
    return packet.encode("utf-8")

text = get_first_200_characters("declaration.txt")
text_array = []
text_copy = text
for i in range(0, 10):
    text_array.append(text[0:20])
    text = text[20:]



# client. Do not erase !!!!

# fialed when both delays are equal

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('gaia.cs.umass.edu', 20000) 
print("connecting to ", server_address)
sock.connect(server_address)
time_out = 1
default_timeout = sock.gettimeout()
try:
    message = b'HELLO S 0.0 0.0 0 6718'
    sock.sendall(message)
    while (True):
        response = sock.recv(50)
        print(response)
        if (response.decode('utf-8') != "WAITING"):
            break
    
    seq = "0"
    for payload in text_array:
        # confused about wait for call 0 from above meaning
        send_packet = make_packet(sequence_number= seq, payload= payload)
        retransmit = True
        while retransmit == True:
            sock.sendall(send_packet)
            sock.settimeout(time_out)
            try:
                while True:
                    response = sock.recv(30)
                    response = response.decode("utf-8")
                    print(response)
                    checksum_verification = checksum_verifier(response)
                    response_seq, response_ack, response_msg, response_checksum = unpack_response(response)
                    if (checksum_verification == True and response_ack == seq):
                        print("here")
                        sock.settimeout(default_timeout)
                        retransmit = False
                        break
            except socket.timeout as e:
                retransmit = True
                print("retransmitted: ", e)

        if (seq == "0"):
            seq = "1"
        else:
            seq = "0"
    
    print(checksum(text_copy))
except Exception as e:
    print("error!!!!!", datetime.now(), ", ", e)
    sock.close()

finally:
    print('closing socket ', datetime.now())
    sock.close()


# seq = 0
# ack = 0
# default_timeout = sock.gettimeout()
# for k in range(0, 10):
#     payload = text_array[k] 
#     data_without_checksum = str(seq) + " " + str(ack) + " " + str(payload) + " "
#     payload_checksum = checksum(data_without_checksum)
#     data = data_without_checksum + str(payload_checksum)
    
#     retransmit = True
#     while (retransmit == True):
#         try:                
#             right_response = False
#             print(data)
#             sock.sendall(data.encode('utf-8'))
#             sock.settimeout(1)
#             while (right_response == False):
#                 response = sock.recv(30)
#                 response = response.decode('utf-8')                    
#                 checksum_verification = checksum_verifier(response)
#                 response_seq, response_ack, response_msg, response_checksum = unpack_response(response)
#                 #print(response + " : " + str(checksum_verification) + "," + str(response_ack), ", expected: ", seq)
#                 if (checksum_verification == True and int(response_ack) == seq):
#                     sock.settimeout(default_timeout)                        
#                     retransmit = False
#                     right_response = True
#         except socket.timeout as e:
#             retransmit = True
#     print("exited, retransmission loop")
#     if (seq == 0):
#         seq = 1
#     else:
#         seq = 0
# print(text_copy)
# print(checksum(text_copy))

# except Exception as e:
# sock.close()
# print("error!!!!!", datetime.now(), ", ", e)

# finally:
# print('closing socket ', datetime.now())
# sock.close()
