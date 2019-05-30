from zipfile import ZipFile
import subprocess
import os

def evaluate(program, tests):
    #program: name of the program file
    #test: zip archive with the tests
    z = ZipFile(tests)
    infiles = []
    outfiles = []
    result = []
    files = z.namelist()
    files.sort()
    for file in files:
        if not file.endswith('/'):
            if file.startswith('in'):
                infiles.append(z.open(file))
            if file.startswith('out'):
                outfiles.append(z.open(file))

    for i in range(len(infiles)):
        submission_output = subprocess.check_output('echo -e "' + infiles[i].read().decode() + '" | python prog.py', shell=True).decode()
        correct_output = outfiles[i].read().decode()
        result.append((os.path.join(os.getcwd(), tests), submission_output.strip(' \n\t') == correct_output.strip(' \n\t')))

    return result
