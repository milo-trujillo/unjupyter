#!/usr/bin/env python3
import json, sys, os, base64, hashlib

infile = None
outfile = None

if( len(sys.argv) == 2 ):
	infile = sys.argv[1]
	outfile = os.path.splitext(infile)[0] + ".md"
elif( len(sys.argv) == 3 ):
	infile = sys.argv[1]
	outfile = sys.argv[2]
else:
	sys.stderr.write("USAGE: %s <infile.ipynb> [outfile.md]\n")
	sys.exit(1)

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
				else:
					sys.stderr.write("WARNING: Unsupported data type '%s/%s'\n" % (category, extension))

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
