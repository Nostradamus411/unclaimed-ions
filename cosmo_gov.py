import os
import json
import subprocess

def main():
    max_num = 37
    ion_cosmos_gov={}
    api = os.environ['ATOM_API']
    # ion_drop_dict = {"cosmos1x5wgh6vwye60wv3dtshs9dmqggwfx2ldnqvev0": 42}
    ion_drop_dict = open_drop_file()

    # Loop through all the addresses and pull gov activity through proposal 37
    try:
        for atom_addr in ion_drop_dict:
            prop_num = 1
            if ion_cosmos_gov is None:
                ion_cosmos_gov = {}
            ions = {"ions":ion_drop_dict[atom_addr]}
            ion_cosmos_gov[atom_addr] = ions
            while prop_num <= max_num:
                this_prop = {}
                propose = proposal(prop_num,atom_addr,api)
                this_prop.update(propose)
                dep_amt = deposit(prop_num,atom_addr,api)
                this_prop.update(dep_amt)
                voted = vote(prop_num,atom_addr,api)
                this_prop.update(voted)
                ion_cosmos_gov[atom_addr][f"prop{prop_num}"] = this_prop
                prop_num += 1
        write(ion_cosmos_gov)
    except:
        write(ion_cosmos_gov)

def write(dict):
    with open('ion_cosmos_gov.json', 'x') as gov:
        json.dump(dict,gov)  

def vote(num,addr,api):
    cmd = f'curl https://stargate-final--lcd--archive.datahub.figment.io/apikey/{api}/gov/proposals/{num}/votes/{addr}'
    output = subprocess.check_output(cmd, shell=True)
    output_dict = json.loads(output.decode('utf-8'))
    try:
        ret = {"voted":output_dict['result']['option']}
    except:
        ret = {"voted":{}}
    return ret

def deposit(num,addr,api):
    cmd = f'curl https://stargate-final--lcd--archive.datahub.figment.io/apikey/{api}/gov/proposals/{num}/deposits/{addr}'
    output = subprocess.check_output(cmd, shell=True)
    output_dict = json.loads(output.decode('utf-8'))
    try:
        ret = {"deposited":output_dict['result']['amount']}
    except:
        ret = {"deposited":{}}
    return ret

def proposal(num,addr,api):
    cmd = f'curl https://stargate-final--lcd--archive.datahub.figment.io/apikey/{api}/gov/proposals/{num}/proposer'
    output = subprocess.check_output(cmd, shell=True)
    output_dict = json.loads(output.decode('utf-8'))
    try:
        if output_dict['result']['proposer'] == addr:
            ret = {"proposer":True}
        else:
            ret = {"proposer":False}
    except:
        ret = {"proposer":False}
    return ret

# Open ion airdrop json file
def open_drop_file():
    with open("ions.json","r") as file:
        file_py_obj = json.load(file)      
    return file_py_obj


if __name__ == "__main__":
    main()