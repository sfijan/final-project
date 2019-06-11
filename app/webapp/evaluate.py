from zipfile import ZipFile
import time
from multiprocessing import Queue, Process
import subprocess
import os
from webapp.models import Test, TestResult, Submission, Language


def run(q, test, submission, z):
    command = 'printf "' + z.open('in/' + test.test_name).read().decode().replace('\n', '\\n') + '" | ./webapp/selector.sh "' + submission.language.name + '" webapp/' + submission.code
    print(command)
    q.put(subprocess.check_output(command, shell=True).decode())



def evaluate_submission(submission_id):        #evaluate a single submission
    print('evaluating submission', submission_id)

    submission = Submission.get(submission_id)
    tests = Test.select().where(Test.task == submission.task_id)
    z = ZipFile(tests[0].zip_file)
    correct = []


    for test in tests:
        #run and get output
        q = Queue()
        p = Process(target=run, name='test', args=(q, test, submission, z))
        #raise Exception
        p.start()
        p.join(1)
        try:
            submission_output = q.get(False)
        except:
            if p.is_alive():
                p.terminate()
            return False
        if p.is_alive():
            p.terminate()
            p.join()
        #compare output
        correct_output = z.open('out/'+test.test_name).read().decode()
        #create etst_result
        test_result = TestResult(test_id=test.id,
                   submission_id=submission.id,
                   correct=submission_output==correct_output)
        #if TestResult.select().where(TestResult.submission_id == submission_id).exists():
        #    test_result.save(only=[TestResult.correct])
        #else:
        #    test_result.save()
        test_result.save()
        correct.append(submission_output==correct_output)

    return correct

