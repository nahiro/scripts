# https://www.denzow.me/entry/2017/09/13/235856
# codingt:utf-8
import subprocess
import sys
import os

class WindowsProcess(object):
    """
    Windows上でのwmic processでの結果に紐づくクラス
    """

    def __init__(self, attributes):
        """
        :param attributes:[
            [key, value],
            [key, value],
        ]
        """
        for k, v in attributes:
            # Pythonはlowerなので揃える
            setattr(self, k.lower(), v)

    def __str__(self):
        display_name = self.commandline if self.commandline else self.caption
        return "Process[{} {} {}]".format(
            self.parentprocessid,
            self.processid,
            display_name
        )


    def __repr__(self):
        return self.__str__()




def get_processes():
    """
    プロセス一覧をwmic経由で取得する
    :param process_name:
    :return:
    """
    encoding = sys.stdout.encoding
    if not encoding:
        encoding = "UTF-8"
    # wmic process  get /FORMAT:LIST
    command_str = " ".join([
        "wmic",
        "process",
        "get",
        "/FORMAT:LIST"
    ])

    result = subprocess.run(command_str, shell=True, stdout=subprocess.PIPE)
    if not result.stdout:
        return []
    # 1行目はヘッダなので。
    process_list = []
    buf = []
    for line in result.stdout.decode(encoding).split("\r\r\n"):
        # 結果はプロセスごとに空行が挟まっている
        if line == "":
            if buf:
                target_process = WindowsProcess(buf)
                process_list.append(target_process)
                buf = []
            continue
        key = line.split("=")[0]
        value = "=".join(line.split("=")[1:])
        buf.append([key, value])

    return process_list

if __name__ == "__main__":
    for proc in get_processes():
        print(proc)
