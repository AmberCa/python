import os

dirs = os.listdir('test')
print(dirs)
for f in dirs:
	parent_dir = os.path.abspath('test')
	print(parent_dir)
	sourcefile = os.path.join(parent_dir, f)
	print('sourcefile---%s'%sourcefile)
	destfile = os.path.join(parent_dir, 're_' + f)
	print('destfile---%s'%destfile)
	os.rename(sourcefile, destfile)
	
