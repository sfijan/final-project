from zipfile import ZipFile
import time
import multiprocessing
import subprocess
import os



def evaluate(program, tests, language):
    #program: name of the program file
    #test: zip archive with the tests
    #language: name of language from Language

    #function for running the programm
    def run():
        submission_output = subprocess.check_output('echo -e "' + z.open(infiles[i]).read().decode() +
                                                    '" | ./selector.sh "'+language+'" '+program,
                                                    shell=True).decode()
    z = ZipFile(tests)
    infiles = []
    outfiles = []
    result = []
    files = z.namelist()
    files.sort()

    for file in files:
        if not file.endswith('/'):
            if file.startswith('in'):
                infiles.append(file)
            if file.startswith('out'):
                outfiles.append(file)

    for i in range(len(infiles)):
        p = multiprocessing.Process(target=run, name="Foo", args=())
        p.start()
        p.join(1)       #TODO make this the time limit constraint
        if p.is_alive():
            p.terminate()
            p.join()

        correct_output = z.open(outfiles[i]).read().decode()
        result.append((infiles[i].split('/')[1], submission_output.strip(' \n\t') == correct_output.strip(' \n\t')))
        #TODO change first element to zip file path

    return result
