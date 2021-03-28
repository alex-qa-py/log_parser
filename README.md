# log_parser

commandline arguments:
--file choosing file
--dir choosing directory
--ext choosing file extention

In the method, create_list_of_files is checked the command line arguments and created a list of files. 
After is used cycle "for" to read lines from files and parse them. 
After parsing results are written to JSON separate files. 
Files are called "result" plus the name of the parsing file. 
