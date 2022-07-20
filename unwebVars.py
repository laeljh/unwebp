#variables
supported_extensions = ['webp','png','jpg','jpeg']
output_directory = '\\downloads\\'
real_directory = ""

def get_real_dir():
    return real_directory

def set_real_dir(dir):
    globals()['real_directory'] = dir
    