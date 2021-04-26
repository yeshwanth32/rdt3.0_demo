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

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('gaia.cs.umass.edu', 20000)
print("connecting to ", server_address)
sock.connect(server_address)
try:
    message = b'HELLO R 0.0 0.0 3 6718'
    sock.sendall(message)
    while (True):
        response = sock.recv(50)
        print(response)
        if (response.decode('utf-8') != "WAITING"):
            break
    expected_seq = "0"
    ack = "1"
    message = ""
    while True:
        response = sock.recv(30)
        response = response.decode("utf-8")
        # if (response == ""):
        #     range("server closed connection")
        checksum_verification = checksum_verifier(response)
        response_seq, response_ack, response_msg, response_checksum = unpack_response(response)
        if (checksum_verification == False or response_seq != expected_seq):
            data = make_packet(ack_number= ack)
            sock.sendall(data)            
            #print("response 1 ", response_seq ," " , response , " ,", checksum_verification)
        else:           
            ack = expected_seq
            message += response_msg
            data = make_packet(ack_number= ack)
            print("response 2 ", response)
            sock.sendall(data)
            if (expected_seq == "0"):
                expected_seq = "1"
            else:
                expected_seq = "0"

except Exception as e:
    print(message)
    print(checksum(message))
    print("error!!!!!", datetime.now(), ", ", e)
    sock.close()

finally:
    # print(message)
    # print('closing socket 2')
    sock.close()




# message = ""
# expected_seq = 0
# ack = 1
# while (True):
#     response = sock.recv(30)
#     response = response.decode('utf-8')
#     if (response == ""):
#         raise Exception("sender closed!")
#     checksum_verification = checksum_verifier(response)
#     response_seq, response_ack, response_msg, response_checksum = unpack_response(response)        
#     if (checksum_verification == False or int(response_seq) != expected_seq):
#         nothing = 0
#         #print("recieved wrong resonse,")
#     else:
#         ack = expected_seq
#         if (expected_seq == 0): 
#             expected_seq = 1
#         else:
#             expected_seq = 0 
#         message += response_msg        
#     #print(response ,",", str(response_seq),",", str(expected_seq), ",", str(ack), ",", str(checksum_verification))
#     payload = "                    "
#     seq = " "
#     data_without_checksum = str(seq) + " " + str(ack) + " " + str(payload) + " "
#     payload_checksum = checksum(data_without_checksum)
#     data = data_without_checksum + str(payload_checksum)
#     #print("expected_seq : ", expected_seq, "r:", response_seq, " - ", ack)
#     print(data)
#     sock.sendall(data.encode('utf-8'))
    
    
# except Exception as e:
# print(message)
# print(checksum(message))
# print("closed at 1:", datetime.now())
# sock.close()
# print("error!!!!!", datetime.now(), ", ", e)

# finally:
# print('closing socket 2')
# sock.close()
