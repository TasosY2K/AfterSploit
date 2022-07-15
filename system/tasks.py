class Tasks:
    def yield_list(self):
        """List of all Windows processes installed and return generator object

        Yields:
            list: all Windows processes installed
            
        Examples:
            for service in processes_info():
                print(service)
        """
        try:
            for proc in process_iter():
                processName = proc.name()
                yield processName
        except:
            pass
        
        
    def kill(self, PROCNAME: str)-> int:
        """Kill a process by name

        Args:
            PROCNAME (str): Name of process to be killed

        Returns:
            int: Process exit code
            
        Example:
            killer = kill("chome.exe")
            print(kill) # 0
        """
        try:
            for proc in process_iter():
                # check whether the process name matches
                if proc.name() == PROCNAME:
                    proc.kill()
                    return 0
                else:
                    return -1
        except:
            pass
        
        
    def kill_all(self):
        """Kill all processes
        """
        try:
            for proc in process_iter():
                proc.kill()
        except:
            pass