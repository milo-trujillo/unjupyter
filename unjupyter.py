#!/usr/bin/env python3
import json, sys, os, base64, hashlib, glob

def writeSource(f, src):
	for line in src:
		f.write(line)

def processOutputs(f, outputs):
	for output in outputs:
		if( "text" in output.keys() ):
				f.write("```\n")
				for line in output["text"]:
					f.write(line)
				f.write("\n```\n")
		if( "data" in output.keys() ):
			filetypes = output["data"].keys()
			for filetype in filetypes:
				category, extension = filetype.split("/")
				if( category == "image" ):
					data = output["data"][filetype]
					raw = base64.b64decode(data)
					filename = hashlib.md5(raw).hexdigest() + "." + extension
					with open(filename, "wb") as image:
						image.write(raw)
					f.write("\n![%s/%s](%s)\n\n" % (category, extension, filename))
				elif( category == "text" and extension == "plain" ):
					data = output["data"][filetype]
					f.write("```\n")
					writeSource(f, data)
					f.write("\n```\n\n")
				elif( category == "text" and extension == "html" and "text/plain" in filetypes ):
					sys.stderr.write("Info: Ignoring an 'html' output in favor of available plaintext\n")
				elif( category == "text" and extension == "html" ):
					sys.stderr.write("Info: Writing raw html because there is no plaintext counterpart :(\n")
					data = output["data"][filetype]
					writeSource(f, data)
					f.write("\n\n")
				else:
					sys.stderr.write("WARNING: Skipping unsupported data type '%s'\n" % (filetype))

def convertNotebook(infile, outfile):
	with open(outfile, "w") as md:
		with open(infile, "r") as notebook:
			data = json.load(notebook)
			cells = data["cells"]
			for cell in cells:
				if( cell["cell_type"] == "markdown" ):
					writeSource(md, cell["source"])
					md.write("\n\n")
				elif( cell["cell_type"] == "code" ):
					if( len(cell["source"]) > 0 ):
						md.write("```\n")
						writeSource(md, cell["source"])
						md.write("\n```\n\n")
					if( len(cell["outputs"]) > 0 ):
						md.write("Output:\n\n")
						processOutputs(md, cell["outputs"])
						md.write("\n")
	sys.stderr.flush()
	print("Notebook '%s' exported as '%s'" % (infile, outfile))

if __name__ == "__main__":
	if( len(sys.argv) == 2 ):
		if( os.path.isdir(sys.argv[1]) ):
			for infile in glob.glob(sys.argv[1]+"/*.ipynb"):
				outfile = os.path.splitext(infile)[0] + ".md"
				convertNotebook(infile, outfile)
		else:
			infile = sys.argv[1]
			outfile = os.path.splitext(infile)[0] + ".md"
			convertNotebook(infile, outfile)
	elif( len(sys.argv) == 3 ):
		infile = sys.argv[1]
		outfile = sys.argv[2]
		convertNotebook(infile, outfile)
	else:
		sys.stderr.write("USAGE: %s <infile.ipynb> [outfile.md]\n")
		sys.stderr.write("   or: %s <directory>\n")
		sys.exit(1)
