class Disks:
    """Drive letters and storage capcacity keys: percentage_used, free_space and total_space

    Examples:
        for index in range(len(disks.drives())):
            print(disks.drives()[index], str(disks.space()[index]["free_space"]) + " GB FREE SPACE")

        output:
            C:\ 99 GB FREE SPACE
            D:\ 100 GB FREE SPACE
            E:\ 900 GB FREE SPACE
    """
    #CORRECT ME IF I AM WRONG: IF ONE DISK HAS THE SAME STORAGE CAPACITY AS ANOTHER BUT ONE SHOWS LESS TOTAL CAPACITY THAT MEANS IT IS MORE WORN OUT 
    def drives(self) -> list:
        """Drive letters

        Returns:
            list: Drive letters
        """
        disks = []
        for disk in disk_partitions():
            disks.append(disk.device)
        return disks
    
    
    def space() -> list:
        """Storage capabilities: percentage_used, free_space and total_space 

        Returns:
            list: percentage_used, free_space and total_space
        """
        disks_info = []
        for disk in disk_partitions():
            disks_info.append(disk_usage(disk.device)._asdict())
        for info in disks_info:
            for item in info.items():
                if item[0] == "percent":
                    info.update({item[0]: round(item[1])})
                else:
                    info.update({item[0]: round(item[1]/1073741824)})
        for item in disks_info:
            for key in list(item.keys()):
                if key == "percent":
                    item.update({"percentage_used" :item[key]})
                    del item[key]
                elif key == "free":
                    item.update({"free_space": item[key]})
                    del item[key]
                elif key == "used":
                    item.update({"used_space": item[key]})
                    del item[key]
                elif key == "total":
                    item.update({"total_space": item[key]})
                    del item[key]
        return disks_info