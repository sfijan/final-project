import zipfile
import subprocess

def evaluate(program, tests):
    #program: name of the program file
    #test: zip archive with the tests
    z = zipfile.ZipFile(tests)
    infiles = []
    outfiles = []
    correct = []
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
        correct.append(submission_output.strip(' \n\t') == correct_output.strip(' \n\t'))

    return (correct.count(True), len(correct))
