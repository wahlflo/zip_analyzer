import argparse
import os
import zipfile
import sys
from importlib_resources import files
from cli_formatter.output_formatting import warning, error, info
import zip_analyzer


def __parse_cli_arguments():
    flags_to_parse = list()
    path = None
    for x in sys.argv[1:]:
        if not x.startswith('-') and path is None:
            path = x
        else:
            flags_to_parse.append(x)
    return flags_to_parse, path


def analyse_zip_archive(zip_archive: zipfile.ZipFile):
    is_encrypted = __archive_is_encrypted(zip_archive=zip_archive)
    print('encrypted:'.ljust(20), is_encrypted)
    print()
    zip_archive.printdir()


def crack_zip_archive(password_list: list, zip_archive: zipfile.ZipFile) -> str or None:
    """ returns password of the zip file or None if the password was not in the password list """
    if not __archive_is_encrypted(zip_archive=zip_archive):
        warning('Zip file is not encrypted')
    info('Try {} passwords'.format(len(password_list)))
    for x in password_list:
        try:
            zip_archive.extractall(pwd=x.encode('utf-8'))
            info('Password found: "{}"'.format(x))
            info('Files extracted')
            return x
        except KeyboardInterrupt:
            warning('Keyboard Interruption. Existing.')
        except:
            pass
    info('Password not found')
    return None


def __archive_is_encrypted(zip_archive: zipfile.ZipFile):
    try:
        zip_archive.testzip()
        return False
    except RuntimeError:
        return True


def main():
    flags_to_parse, path_to_file = __parse_cli_arguments()

    argument_parser = argparse.ArgumentParser(usage='zipAnalyzer FILE [OPTIONS]', description='A cli script to analyze zip archive.')
    argument_parser.add_argument('-c', '--crack', help="Tries to crack the encryption by enumeration over a password list. Extracts the zip archive if the password was found.", action='store_true', default=False)
    argument_parser.add_argument('--passlist', type=str, help="Path to custom password list", default=None)

    parsed_arguments = argument_parser.parse_args(flags_to_parse)

    if path_to_file is None:
        argument_parser.print_help()
        exit()

    path_to_archive = os.path.abspath(parsed_arguments.input)

    # read password list
    if parsed_arguments.passlist is not None:
        path_to_password_list = os.path.abspath(parsed_arguments.passlist)
    else:
        path_to_password_list = files(zip_analyzer).joinpath('password_list.txt').read_text()
    password_list = list()
    with open(path_to_password_list, mode='r', encoding='utf-8') as password_list_file:
        for line in password_list_file:
            password_list.append(line.strip())

    try:
        zip_archive = zipfile.ZipFile(path_to_archive)
    except Exception as exception:
        error('Zip file could not be read: {}'.format(exception))
        exit()
    else:
        if parsed_arguments.crack:
            crack_zip_archive(password_list=password_list, zip_archive=zip_archive)
        else:
            analyse_zip_archive(zip_archive=zip_archive)


if __name__ == '__main__':
    main()
