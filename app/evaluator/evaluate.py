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
    def run(q):
        submission_output = subprocess.check_output('echo -e "' + z.open(infiles[i]).read().decode() +
                                                    '" | ./selector.sh "'+language+'" '+program,
                                                    shell=True).decode()
        q.put(submission_output)
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
        q = multiprocessing.Queue()
        p = multiprocessing.Process(target=run, name="task"+str(i), args=(q,))
        p.start()
        p.join(1)       #TODO make this the time limit constraint
        try:
            submission_output = q.get(False)
        except:
            result.append((infiles[i].split('/')[1], False))
            if p.is_alive():
                p.terminate()
            continue
        if p.is_alive():
            p.terminate()
            p.join()

        correct_output = z.open(outfiles[i]).read().decode()
        result.append((infiles[i].split('/')[1], submission_output.strip(' \n\t') == correct_output.strip(' \n\t')))
        #TODO change first element to zip file path

    return result
