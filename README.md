# gittable

Previously I drafted a small tool [`gittar`](https://github.com/Mikumikunisiteageru/gittar) to manage the versions of table files from Microsoft Excel by [`git`](https://github.com/git/git). However, when I tried gittar on a large Excel file in practice, I found surprisingly that saving all versions of the file independently consumed less disk space than using gittar.

It seemed that Microsoft Excel registers all cell values (distinct? probably not) as a list (xl/sharedStrings.xml), and then cite these values by their pointers in actual tables (e.g. xl/worksheets/sheet1.xml). When the content of one single cell is altered, the list may be rearranged and hence the pointers, and may further affect thousands on lines referring to them --- for git there will be a lot of work to do.

Another way to present the Excel sheets to git is to export the data as a plain text vector --- as if the sheets are copied from Excel and pasted into plain text environments. By doing so, all the local insertions, modifications, and deletions remain local in plain text, although all styles, formats, and formulae are lost after the conversion.

Here I write `gittable` implement the idea above, which converts the sheets in a Excel file into plain text without any style before sending them to git.

## Installation

The script of `gittable` is written in Python 3. Dependencies including `os`, `shutil`, `sys`, and `pandas` (all Python packages) should be ready before using the command.

In Windows OS, the directory containing `gittable.py` and `gittable.bat` can be added to the `PATH` environmental variable to allow the tool to launch anywhere in the system when necessary.

## Usage

All `gittable` commands resemble those for `git`, except `gittable add` and `gittable diff` currently require an argument corresponding to an existing file.

```
gittable init
gittable add somefile.xlsx
gittable commit -m "commit message"
```

After modifying the content of `somefile.xlsx`, the user may execute `gittable diff somefile.xlsx` to check the difference between the current status and the last committed version.

The command `gittable reset` has not been implemented yet.

## History

- v0.0.1, prototype
