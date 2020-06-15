import subprocess
import re
import os

"""
To get to know how to use this project: https://github.com/AntoData/appium-framework/wiki
"""


def upload_file_to_bitbar(file_apk: str) -> str:
    """
    This methods uploads the file with extension apk in folder apks that we pass as a parameter in "file_apk"
    to BitBar
    :param file_apk: File apk in folder apks
    :return: A string with the id of the file we uploaded to Bitbar
    """
    # We set up the command to upload the file in "file_apk" to bitbar, replacing {0} with file_apk
    if os.path.exists("../apks/{0}".format(file_apk)):
        command: str = 'curl -X POST -u ONzNQdFzFsNyzwfwECg6XhXYEfuEJvTQ: https://cloud.bitbar.com/api/me/files -F ' \
                       '"file=@../apks/{0}"'.format(file_apk)
    else:
        command: str = 'curl -X POST -u ONzNQdFzFsNyzwfwECg6XhXYEfuEJvTQ: https://cloud.bitbar.com/api/me/files -F ' \
                       '"file=@./apks/{0}"'.format(file_apk)
    print("Executing command to upload apk file to BitBar:")
    print(command)
    # We execute the command
    file_properties_bytes = subprocess.run(command, stdout=subprocess.PIPE)
    print(file_properties_bytes.stdout)
    file_properties_str: str = str(file_properties_bytes.stdout)
    # We get the id of the file from the return of the command we have just executed
    return get_id_from_command(file_properties_str)


def get_id_from_command(command_result: str) -> str:
    """
    This method handles the parsing of the response of the command to upload the file apk to bitbar to get the id of
    that file in bitbar which will be needed to execute the remote test in bitbar
    :param command_result:
    :return: A string variable with the id of the file in bitbar
    """
    # We search the following regular expresion in the result of the command
    id_regexp: re = re.search("\"id\":[0-9]*", command_result)
    # We get the first match in the string with the result of the command
    id_group: str = id_regexp.group()
    print("Variable ID found: {0}".format(id_group))
    # We split by : to get the name of the variable and the id
    id_array: [str] = id_group.split(":")
    try:
        # We get the id of the file
        id_result: str = id_array[1]
    except IndexError:
        # We catch this exception because if the array is not of size 2, we are not parsing correctly the result
        print("We did not get a correct response from the command to upload the apk")
        # We return "" in this case
        return ""
    print("File id: {0}".format(id_result))
    # We return the id of the file as a string
    return id_result
