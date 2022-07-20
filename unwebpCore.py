
from ast import IsNot
from distutils import extension
import os
import shutil
from PIL import Image

import unwebVars as uvars

######################
debug_bool = True
def debug(message):
    if debug_bool:
        print(message)
#####################


#a function that takes a file name and returns file extension
def get_extension(file):
    try:
        #check if '.' is in the file name
        if '.' in file:
            file_name = file.split('.')
            debug('Reading extention: ' + file_name[-1])
            extension = file_name[-1]
        else:
            debug('No extension found')
            extension = None
    except Exception as e:
        debug('Can\'t get file extension: '+str(e))
        extension = None
   # return the extension 
    return extension

#function that gets file name
def get_file_name(file):
    try:
        file_name = file.split('/')[-1]
        debug('Got file name: '+file_name)
        
    except Exception as e:
        debug('Can\'t get file name: '+str(e))
        file_name = None
    #return the file name
    return file_name

#a function that opens a file in PIL and returns the image
def open_file(file_name, file_path=uvars.output_directory):
    if file_path[-1] != '\\':
        file_path = file_path+'\\'
    debug('Trying to open file: '+file_name)
    #check if path contains : 
    if ':' in file_path:
        debug('Absolute path provided: '+file_path)
        file = file_path+file_name
        debug('Resolving file to: '+file)
    #file name and path
    #current directory
    else:
        debug('Relative path provided: '+file_path)
        current_directory = os.getcwd()
        file = current_directory+file_path+file_name
        debug('Resolving file to: '+file)
    #debug('Opening a file: '+file)
    if os.path.exists(file):
        #get absolute path
        file = os.path.abspath(file)
    try:
        #debug('Abs path: '+str(file))
        #open the file
        image = Image.open(file)
        debug('Opened file: '+file)
    except Exception as e:
        debug('Can\'t open file: '+str(e))
        image = None
    #return the image
    return image

#function that checks if a given directory exists and if not creates it
#it takes directory in format of absolute path or relative path, it can start and or end with a '\' or not
def check_directory(directory, make_as_needed=True):
    #check directory is not None
    if directory is not None:
        if directory == '':
            directory = os.curdir
        #if directory starts with '\\' remove it from the start
        if directory[0] == '\\' or directory[0]=='/':
            directory = directory[1:]
        #check if directory exists
        debug('Checking directory: '+directory)
        if os.path.exists(directory):
            #get absolute path
            abs_path = os.path.abspath(directory)
            debug("Abs path: "+str(abs_path))
        else:
            debug("Directory doesn't exist, create it?")
            if not make_as_needed:
                debug("y/n")
                decision = input()
            else:
                debug("Decision -> True")
            #if user inputs yes create the directory
            if make_as_needed or decision=='y':
                os.makedirs(directory)
                abs_path = os.path.abspath(directory)
                debug("Abs path: "+str(abs_path))
            else:
                debug("Directory not created")
                abs_path = None
            #make the directory
    else:
        debug('Error: directory is none...')
        abs_path = None
    return abs_path


#a function that takes an image and saves it to a file of a given extension
def save_file(image,file_name,save_ext, directory=uvars.output_directory, overwrite=True, keep_both = True):
    directory = check_directory(directory)
    #join the file name and extension with a '.'
    file_name = file_name.split('.')[0]
    file = directory+'\\'+file_name + '.' + save_ext
    debug('Trying to save file: '+file)
    #check if file exists
    if os.path.exists(file):
        debug('File exists. Overwrite?')
        if not overwrite:
            debug('y/n')
            decision = input()
        else:
            debug('Decision -> True')
        if overwrite or decision=='y':   
            try:
                if keep_both:   
                    debug('Keep both files on, will try alternative name for this file')                 
                    i = 0
                    #check if the file name ends with brackets and a number
                    #split name from the extension
                    try:
                        file_name_no_ext = file_name.split('.')[0]
                    except Exception as e:
                        file_name_no_ext = file_name
                        debug('File name has no extension: '+str(e))
                    #check if '(...)' is in the file name
                    numbered = False
                    if '(' in file_name_no_ext:
                        #get index of '('
                        index1 = file_name_no_ext.index('(')
                        numbered = True
                    else:
                        numbered = False
                    if ')' in file_name_no_ext:
                        #get index of ')'
                        index2 = file_name_no_ext.index(')')
                        numbered = True
                    else:
                        numbered = False                       
                    while os.path.exists(file):
                        if numbered:
                            file = directory+'\\'+file_name_no_ext[0:index1+1]+str(i)+file_name_no_ext[index2:]+'.'+save_ext
                        else:                     
                            file = directory+'\\'+file_name +'('+str(i)+')'+'.' + save_ext
                        debug('Previous name unavailable, trying: '+file)
                        i+=1
                debug('Found an available file name')
                #save the image
                image.save(file, quality=100)
                debug('Saved file: '+file)
                #close the image
                image.close()
            except Exception as e:
                debug('Can\'t save file: '+str(e))
                file = None
        else:
            debug('File not saved')
            file = None
    else:
        debug('Saving file...')
        #save the image
        image.save(file, quality=100)
        debug('Saved file: '+file)
        #close the image
        image.close()
    return file

       
#a function that takes a png transparent image and returns a non-transparent image with background
def add_background_to_transparent(transparent_image, bg_color = (255,255,255)):
    transparent_image.load() # required for png.split()
    non_transparent_image = Image.new('RGB', transparent_image.size, bg_color)
    non_transparent_image.paste(transparent_image, mask=transparent_image.split()[3]) # 3 is the alpha channel
    transparent_image.close()
    debug('Background added')
    return non_transparent_image

#function that displayes image mode
def get_image_mode(image):
    mode = image.mode
    debug('Image mode: '+mode)
    return mode

#function that extracts the path from a file
def get_path(file):
    #check if file exists
    if os.path.exists(file):
        #get absolute path
        abs_file_path = os.path.abspath(file)
        debug("File exists: "+abs_file_path)        
        abs_path = '\\'.join((abs_file_path.split('\\')[0:-1]))
        debug("Abs path: "+str(abs_path))
    else:
        debug("File doesn't exist")
        abs_path = None
    return abs_path

#main function that processes a file depending on format and mode
def open_process_save_image(file, save_format = 'png', save_path='', remove_transparency=False, bg_color = (255,255,255)):
    file_name = get_file_name(file)
    file_path = get_path(file)
    debug("File name: "+file_name+" File path: "+file_path)
    if save_path == '' or save_path is None:
        save_path = file_path
    debug("Save path: "+save_path)
    image = open_file(file_name,file_path)
    image_source_mode = get_image_mode(image)
    #if the image is in mode supporting transparency
    #if the source has transparency but needs to save to jpg or if the user wants to remove the transparency
    if image_source_mode=='RGBA' or image_source_mode=='RBGa' or image_source_mode=='LA' or image_source_mode=='La':
        if save_format == 'jpg' or remove_transparency:
            debug('conversion of transparent to non-transparent format')
            image = add_background_to_transparent(image,bg_color)
    else:
        debug('standard conversion')
    #save the image
    converted_file = save_file(image, file_name, save_format, save_path)
    return converted_file
 



#a function that takes a directory name and a list of extensions and returns all files in this directory
def get_supported_files(directory, extensions):
    directory = check_directory(directory)
    #get all files in the directory
    files = os.listdir(directory)
    #create an empty list to store the files
    supported_files = []
    #loop through all files
    for file in files:
        #check if the file isn't None
        if file is not None:
            #get the file extension
            debug('Checking file: '+file)
            ext = get_extension(file)
            #if the file extension is in the list of extensions
            if ext in extensions:
                #add the file to the list
                supported_files.append(file)
    #return the list
    debug('Opened: '+directory)
    debug('Supported files: '+str(supported_files))
    return supported_files


#a function that moves all the files to a new directory
def move_files(files, directory):
    #check if directory exists
    directory = check_directory(directory)
    moved_files = []
    #loop through all files
    for file in files:
        shutil.copy(file, directory)
        #delete the original file
        os.remove(file)
    debug('Moved files to: '+directory)
    return directory


#a function that generates and returns an image thumbnail
def generate_thumbnail(image, max_size=(100,50)):
    thumbnail=image.copy()
    thumbnail.thumbnail(max_size)
    return thumbnail

#function that shows the image
def show_image(image):
    #check if the image is not None
    if image is not None:
        image.show()
        debug('Image shown')
        image.close()
    else:
        debug('Image is None')
    return image

#open_process_save_image(my_files[0], 'png')
#for every supported file create 
#check_directory("/dir")

#file1 = 'source_file.png'
#converted = open_process_save_image(file1, 'webp')
#get_supported_files(check_directory(uvars.output_directory), uvars.supported_extensions)

#get a list of supported files in the current directory
#supported_files = get_supported_files('', uvars.supported_extensions)
#move files to the default directory
#move_files(supported_files, uvars.output_directory)
#moved_files = get_supported_files('\\new_folder\\', uvars.supported_extensions)

#image = open_file(moved_files[0])
#thumbnail = generate_thumbnail(image,(200,200))
#show_image(thumbnail)

#process image
#done1 = open_process_save_image(moved_files[1],uvars.output_directory)

#proces second image, specify it's source name, source directory, file extension and a new directory that should be created before saving the image
#if no path is provided the image will be saved in the same directory as the source file
#done2 = open_process_save_image(file_name='source_file(4).jpg',file_path='\\new_folder\\',save_ext='png')