# unjupyter

Extracts content from a Jupyter Notebook and exports it as markdown. Images will be exported as individual files, and referenced from markdown using image embed syntax, like `![filename](/path/to/image)`

## Usage

To export `foo.ipynb` as `foo.md`:

    unjupyter foo.ipynb

Or, to specify another filename to save as:

	unjupyter foo.ipynb bar.md

Or, to export all notebooks in a directory as markdown:

	unjupyter .

## Images

When notebooks contain images they are stored as base64 encoded text with no filename. Since we have to choose a filename, we name each image after the md5 checksum of its file contents, with the appropriate image extension.

## What's Supported and What's Not?

At present, the tool only understands "markdown" and "code" cells, and can only extract images and plaintext from the "output" fields of cells. This seems to cover the majority of real-world notebooks, but there are likely plenty of more obscure cells that this tool will ignore.
