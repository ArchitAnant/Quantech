import zipfile

z = zipfile.ZipFile("/Users/architanant/Documents/Quantech/file_processing/test-1.pdf")

#print list of valid attributes for ZipFile object
print (dir(z))

#print all files in zip archive
all_files = z.namelist()
print (all_files)

#get all files in word/media/ directory
images = filter(lambda x: x.startswith('word/media/'), all_files)
print (images)

#open an image and save it
image1 = z.open('word/media/image1.jpeg').read()
f = open('image1.jpeg','wb')
f.write(image1)

#Extract file
z.extract('word/media/image1.jpeg', r'path_to_dir')