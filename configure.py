from Crypto.PublicKey import RSA
from requests import get


ip = input("Do you want to use your ip address for client connection[Y/N]:")
if 'y' in ip.lower():
    ip = get('https://api.ipify.org').text
else:
    ip = input("Enter custom ip address: ")
    
def key_changer_server(public_key_server,private_key,recv_password,file_path_to_read_and_write):
            file=open(file_path_to_read_and_write,"wb")
            file.write(public_key_server)
            file.write("\n")
            file.write(private_key)
            file.write("\n")
            file.write(recv_password)
            file.close()
            del file

def key_changer_clients(public_key_server,host,recv_password,file_path_to_read_and_write):
    
            file=open(file_path_to_read_and_write,"wb")
            file.write(public_key_server)
            file.write("\n")
            file.write(host)
            file.write("\n")
            file.write(recv_password)
            file.close()
            del file
def create_password():
    import random
    import array

    # maximum length of password needed
    # this can be changed to suit your password length
    MAX_LEN = 32

    # declare arrays of the character that we need in out password
    # Represented as chars to enable easy string concatenation
    DIGITS = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    LOCASE_CHARACTERS = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h',
                        'i', 'j', 'k', 'm', 'n', 'o', 'p', 'q',
                        'r', 's', 't', 'u', 'v', 'w', 'x', 'y',
                        'z']

    UPCASE_CHARACTERS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H',
                        'I', 'J', 'K', 'M', 'N', 'O', 'p', 'Q',
                        'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y',
                        'Z']

    SYMBOLS = ['@', '#', '$', '%', '=', ':', '?', '.', '|', '~', '>',
            '*', '(', ')', '<']

    # combines all the character arrays above to form one array
    COMBINED_LIST = DIGITS + UPCASE_CHARACTERS + LOCASE_CHARACTERS + SYMBOLS

    # randomly select at least one character from each character set above
    rand_digit = random.choice(DIGITS)
    rand_upper = random.choice(UPCASE_CHARACTERS)
    rand_lower = random.choice(LOCASE_CHARACTERS)
    rand_symbol = random.choice(SYMBOLS)

    # combine the character randomly selected above
    # at this stage, the password contains only 4 characters but
    # we want a 12-character password
    temp_pass = rand_digit + rand_upper + rand_lower + rand_symbol


    # now that we are sure we have at least one character from each
    # set of characters, we fill the rest of
    # the password length by selecting randomly from the combined
    # list of character above.
    for x in range(MAX_LEN - 4):
        temp_pass = temp_pass + random.choice(COMBINED_LIST)

        # convert temporary password into array and shuffle to
        # prevent it from having a consistent pattern
        # where the beginning of the password is predictable
        temp_pass_list = array.array('u', temp_pass)
        random.shuffle(temp_pass_list)

    # traverse the temporary password array and append the chars
    # to form the password
    password = ""
    for x in temp_pass_list:
            password = password + x
    return password
    # print out password


rrecv_password = create_password()

print("Creating rsa keys ...This takes some time")
key = RSA.generate(2048)
private_key = key.export_key()
file_out = open("server/temp/private.pem", "wb")
file_out.write(private_key)
file_out.close()

public_key = key.publickey().export_key()
file_out = open("server/temp/receiver.pem", "wb")
file_out.write(public_key)
file_out.close()

print("Writing changes ....")

key_changer_server(rrecv_password,"server/temp/data.DAT")
key_changer_clients(ip,rrecv_password,"client/.data.one")
key_changer_clients(ip,rrecv_password,"sudo_controller/data.DAT")

input("...Setup Done...")
