import os
import time
import numpy as np
import paramiko


ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy)
ssh.connect("10.211.55.6", username="parallels", password="")


def make_psaia_dict(filename):
    psaia = dict()
    stnxt = 0
    ln = 0
    try:
        for l in open(filename, "r"):
            ln = ln + 1
            ls = l.split()
            if stnxt:
                cid = ls[0]
                if cid == '*':
                    cid = ' '
                resid = (cid, ls[6])
                casa = np.array(ls[1:6], dtype=np.float)
                rasa = np.array(ls[8:13], dtype=np.float)
                rrasa = np.array(ls[13:18], dtype=np.float)
                rdpx = np.array(ls[18:24], dtype=np.float)
                rcx = np.array(ls[24:30], dtype=np.float)
                rhph = float(ls[-1])
                psaia[resid] = (casa, rasa, rrasa, rdpx, rcx, rhph)
            elif len(ls) != 0 and ls[0] == 'chain':
                stnxt = 1

    except Exception as e:
        print('Error Processing psaia file: ', filename)
        print('Error occured while processing line:', ln)
        print(e)
        raise e
    return psaia


def run_psaia(fname: str, ofname: str = None):
    
    cmdstr = f"python3 /home/parallels/Downloads/course_project/script.py {fname}"
    _, stdout, stderr = ssh.exec_command(cmdstr)

    def touch(path):
        with open(path, 'a'):
            os.utime(path, None)

    os.system(": > psaia.tbl")
    time.sleep(3)
    file_loader = ssh.open_sftp()
    file_loader.get("/home/parallels/Downloads/course_project/psaia.tbl", os.getcwd() + '/psaia.tbl')
    file_loader.close()
    pdict = make_psaia_dict("psaia.tbl")
    if stdout.channel.recv_exit_status() == 0:
        print(f'PSAIA Successful : {cmdstr}')
    else:
        print('PSAIA wasn\'t finished with exit code 0')
    os.system('rm -rf psaia.tbl')
    return pdict


if __name__ == "__main__":
    pass
#     print(os.getcwd())
#     psaia = run_psaia('1a220A0B_1.pdb')
