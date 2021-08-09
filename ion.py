import json
import bech32
import subprocess
from datetime import datetime

def main():
    # Variable inits
    unclaimed_ions = 0
    unclaimed_ions_dict = {}
    # Open ion airdrop file sourced from https://github.com/osmosis-labs/networks/blob/main/osmosis-1/ions.json
    ion_drop_dict = open_drop_file()

    # Loop through all the addresses checking for activity to sum up the unclaimed ion and output json of addresses with unclaimed amount
    for atom_addr in ion_drop_dict:
        osmo_addr = str(atom_to_osmo(atom_addr))
        if chain_action(osmo_addr) is False:
            unclaimed_ions_dict[osmo_addr] = ion_drop_dict[atom_addr]
            unclaimed_ions += ion_drop_dict[atom_addr]
        else:
            unclaimed_ions = unclaimed_ions
 
    # Output files with details
    write_total_amt(str(unclaimed_ions))
    write_unclaimed(unclaimed_ions_dict)


# Output txt file of the total amount of unclaimed ions
def write_total_amt(amt):
    with open('total_unclaimed_ion_' + str(datetime.now().strftime('%Y_%m_%d_%H_%M_%S')) + '.txt', 'x') as tot:
        tot.write(amt)


# Output json of all osmo addresses with their amount of unclaimed ion(s)
def write_unclaimed(dict):
    with open('unclaimed_ions_' + str(datetime.now().strftime('%Y_%m_%d_%H_%M_%S')) + '.json', 'x') as unclaimed:
        json.dump(dict,unclaimed)   


# Call remote public node to check if Osmo address has performed any actions
# Sequence number of 0 means no tx have happened from the account ==> inferred unclaimed ion
def chain_action(addr):
    cmd = f'osmosisd query auth account {addr} -o json'
    output = subprocess.check_output(cmd, shell=True)
    output_dict = json.loads(output.decode('utf-8'))
    if int(output_dict['sequence']) > 0:
        return True
    else:
        return False


# Open ion airdrop json file
def open_drop_file():
    with open("unclaimed_ions_2021_07_25_21_54_13.json","r") as file:
        file_py_obj = json.load(file)      
    return file_py_obj


# Function to convert a bech32 address from a Cosmos to Osmosis variant 
def atom_to_osmo(atom_addr):
    atom_tuple = bech32.bech32_decode(atom_addr)
    data = atom_tuple[1]
    osmo_addr = bech32.bech32_encode('osmo',data)    
    return osmo_addr


if __name__ == "__main__":
    main()
