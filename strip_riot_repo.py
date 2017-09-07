#!/usr/bin/python

from shutil import copytree, ignore_patterns, rmtree

def main():
    
    try:
        copytree("RIOT", "RIOT_stripped", ignore=ignore_patterns(".*", "doc", "tests", "generated_by_riotam"))
        
        path = "RIOT_stripped/Makefile.include"
        file_content = []
        with open(path, "r") as makefile:
            
            lines = makefile.readlines()
            
            for line in lines:
                file_content.append(line)
            
        with open(path, "w") as makefile:
            for line in file_content:
                
                print line
                
                if "flash: all" in line:
                    makefile.write(line.replace(" all", ""))
                else:
                    makefile.write(line)
                    
        
    except Exception as e:
        print e
        
if __name__ == "__main__":
    main()