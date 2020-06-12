# zipAnalyzer
A cli script to analyze zip archives.

## Installation

Install the package with pip

    pip install zip-analyzer

## Usage
Type ```zipAnalyzer --help``` to view the help.

```
usage: zipAnalyzer FILE [OPTIONS]

A cli script to analyze zip archives.

optional arguments:
  -h, --help           show this help message and exit
  -c, --crack          Tries to crack the encryption by enumeration over a password list. Extracts the zip archive if the password was found.
  --passlist PASSLIST  Path to custom password list
```

## Example analyze zip file
```
$zipAnalyzer invoice.zip
encrypted:           True

File Name                 Modified           Size
invoice.docm       2020-05-13 09:36:06       7080
```

## Example use password list
```
$zipAnalyzer invoice.zip -c
[+] Try 41 passwords
[+] Password found: "777"
[+] Files extracted
```
