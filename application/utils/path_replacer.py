
def replace_path_delimiters(path):
	from os import sep
	p = path.replace('\\', '/').replace('//', '/').split('/')
	return sep.join(p)

