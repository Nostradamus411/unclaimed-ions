import os
import json
import subprocess

def main():
    hub=1
    hub1_props = range(1,6)
    hub1_votes_dict = {}
    ion_drop_dict = open_drop_file()

    for atom_addr in ion_drop_dict:
        if hub1_votes_dict is None:
            hub1_votes_dict = {}
        ions = {"ions":ion_drop_dict[atom_addr]}
        hub1_votes_dict[atom_addr] = ions        
        for prop in hub1_props:
            this_prop = {}
            hub1_vote_ret = hub1_vote(prop,atom_addr)
            vote = {'vote':hub1_vote_ret['option']}
            this_prop.update(vote)
            hub1_votes_dict[atom_addr][f"prop{prop}"] = this_prop

    frmt_out = json.dumps(hub1_votes_dict, indent=4)
    write_json(frmt_out,hub)

# Output txt file of the total amount of unclaimed ions
def write_json(dict,hub):
    with open(f'hub{hub}_votes_dict.json', 'w') as out:
        out.write(dict)

def hub1_vote(prop,addr):
    cmd = f'~/cosmos/hub1/gaiacli query gov vote {prop} {addr} -o json  --trust-node'
    try:
        output = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT)
        output_dict = json.loads(output.decode('utf-8'))
        ret = output_dict.pop('voter')
        return output_dict
    except subprocess.CalledProcessError as e:
        return {'proposal_id': prop, 'option': 'DidNotVote'}

# Open ion airdrop json file
def open_drop_file():
    with open("ion_test.json","r") as file:
        file_py_obj = json.load(file)      
    return file_py_obj


if __name__ == "__main__":
    main()