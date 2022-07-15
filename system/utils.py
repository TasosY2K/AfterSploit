from subprocess import Popen, PIPE, check_output
def shell_timeout(command: str, exec_time=10, output_cap=2000)->str:
    '''
    RUN SHELL COMMAND WITH COMMAND TIMEOUT
    for output in run_shell_timeout('whoami && dir',30,4000): # FORMAT: (COMMAND, EXECUTION_TIME_SECONDS, MAX_OUTPUT_CHARACTERS)
        print(output)
        print('========================================')
    '''
    c = Popen(str(command), shell=True, stdout=PIPE, stderr=PIPE, stdin=PIPE).communicate(timeout=int(exec_time))
    if c[0]:
        o = "{}".format(c[0].decode("utf-8"))
    if c[1]:
        o = "{}".format(c[1].decode("utf-8"))
    for d in [o[i:i+int(output_cap)] for i in range(0, len(o), int(output_cap))]:
        yield d

def shell_supress(command: str, exec_time=10, repeat_cap=2000)->str:
    '''
    RUN SHELL COMMAND WITH COMMAND TIMEOUT AND SUPRESS REPEATING OUTPUT
    for output in run_shell_supress('whoami && dir',30,4000): # FORMAT: (COMMAND, EXECUTION_TIME_SECONDS, REPEAT_CHARACTER CAP)
        print(output)
        print('========================================')
    '''
    def repeats(string):
        for x in range(1, len(string)):
            substring = string[:x]
            if substring * (len(string)//len(substring))+(substring[:len(string)%len(substring)]) == string:
                return substring
        return string
    c = Popen(command, shell=True, stdout=PIPE, stderr=PIPE, stdin=PIPE).communicate(timeout=int(exec_time))
    if c[0]:
        o = "{}".format(c[0].decode("utf-8"))
    if c[1]:
        o = "{}".format(c[1].decode("utf-8"))
    if(len(o) > int(repeat_cap)):
        o = repeats(o)
    for d in [o[i:i+2000] for i in range(0, len(o), 2000)]:
        yield d

def shell(command: str)->str:
    '''
    RUN STANDARD SHELL COMMAND WITHOUT PROCESS TIMEOUTS
    cmd = shell('whoami')
    '''
    out = check_output(str(command)).decode('utf-8')
    return out

def copy_file(source: str, destination: str):
    '''
    COPY FILE SOURCE TO DESTINATION WITH NO ENVIRONMENT VARIABLE SUPPORT
    copy = copy_file('C:\\Windows\\System32\\cmd.exe', 'C:\\Users\\Public\\Downloads\\cmd.exe')
    '''
    source = str(source)
    destination = str(destination)
    with open(source, 'rb') as fb:
        bak = fb.read()
        try:
            with open(destination, 'wb') as fd:
                fd.write(bak)
                fd.close()
            fb.close()
        except:
            return False
    return destination
