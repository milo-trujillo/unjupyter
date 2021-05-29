# unjupyter

Extracts content from a Jupyter Notebook and exports it as markdown. Images will be exported as individual files, and referenced from markdown using image embed syntax, like `![filename](/path/to/image)`

Jupyter Notebooks can be convenient for exploration of data, and are great for providing interactive demos to students. However, they're often used for documentation or presentation of results, where markdown would be sufficient. This tool removes the need to launch a full Python interpreter + web browser + JavaScript blob to read a text file with images in it. This is especially convenient if you are trying to read the contents of a notebook on a remote server over ssh.

## Usage

To export `foo.ipynb` as `foo.md`:

    unjupyter foo.ipynb

Or, to specify another filename to save as:

	unjupyter foo.ipynb bar.md

Or, to export all notebooks in a directory as markdown:

	unjupyter .

## Images

When notebooks contain images they are stored as base64 encoded text with no filename. Since we have to choose a filename to export them, we name each image after the md5 checksum of its file contents, with the appropriate image extension.

## What's Supported and What's Not?

At present, the tool only understands "markdown" and "code" cells, and can only extract images, plaintext, and html (only if no plaintext is available) from the "output" fields of cells. This seems to cover the majority of notebooks that are simple enough to legitimize conversion to markdown.
