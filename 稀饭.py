import os
import urllib.request
import sys
import time
import platform


class SystemChecker:
    @staticmethod
    def is_linux():
        return platform.system() == 'Linux'

    @staticmethod
    def is_amd_architecture():
        machine = platform.machine().lower()
        amd_patterns = [
            'x86_64', 'amd64', 'x86', 'i386', 'i686',
            'amd', 'intel'
        ]
        return any(pattern in machine for pattern in amd_patterns)

    @staticmethod
    def is_linux_amd():
        return SystemChecker.is_linux() and SystemChecker.is_amd_architecture()

    @staticmethod
    def get_detailed_info():
        return {'os': platform.system(), 'architecture': platform.machine()}


checker = SystemChecker()

if checker.is_linux_amd():
    pass
else:
    info = checker.get_detailed_info()
    print(f'当前系统不支持,当前系统类型: {info["os"]},系统架构: {info["architecture"]}')
    exit(1)


####################使用教程区####################

# 抓包 https://tube.e.kuaishou.com/rest/e/tube/inspire/home
# 格式1：备注#Cookie#BrowserUa#User-Agent#SystemUa#Ks-Pkgld#message
# 格式2：备注#Cookie#BrowserUa#User-Agent#SystemUa#Ks-Pkgld#message#sock5
# socks5存在则使用代理，反之
# socks代理选择参数，可填可不填 格式：ip|port|username|password
# ck变量：xfck, 填写上面两种格式ck均可，多号新建变量即可
# 并发变量：XF_Bf, 设置为True为开启并发，默认关闭
# 卡密变量：XF_Card 填写购买的卡密即可
# 卡密变量：XF_Yxms 【1】为正常任务，【2】为直接查询收益情况，【3】为导出当日全部账号收益为excel表格，默认1


def GET_SO():
    PythonV = sys.version_info
    if PythonV.major == 3 and PythonV.minor == 10:
        PythonV = '10'
        print('当前Python版本为3.10 开始安装...')
    elif PythonV.major == 3 and PythonV.minor == 11:
        PythonV = '11'
        print('当前Python版本为3.11 开始安装...')
    else:
        return False, f'不支持的Python版本：{sys.version}'

    try:
        mirrors = [
            f'https://raw.bgithub.xyz/BIGOSTK/pyso/refs/heads/main/xf_{PythonV}.so',
            f'https://gh.qninq.cn/https://raw.githubusercontent.com/BIGOSTK/pyso/main/xf_{PythonV}.so'
        ]

        last_error = None
        for url in mirrors:
            try:
                print(f'尝试从 {url} 下载...')
                with urllib.request.urlopen(url, timeout=15) as response:
                    if response.status == 200:
                        with open('./xf.so', 'wb') as out_file:
                            out_file.write(response.read())
                        print('下载成功')
                        return True, None
            except Exception as e:
                last_error = e
                print(f'下载失败: {e}')
                time.sleep(1)

        return False, f'所有镜像尝试失败: {last_error}'

    except Exception as e:
        return False, e


def main():
    if not os.path.exists('./xf.so'):
        success, error = GET_SO()
        if not success:
            print(f'无法获取xf.so: {error}')
            return

    try:
        import xf
        yxms = os.environ.get('XF_Yxms', '1')
        yxms = str(yxms)
        if yxms == '1':
            xf.main()
        elif yxms == '2':
            xf.get_coin()
        elif yxms == '3':
            xf.get_excel()
    except ImportError as e:
        print(f'导入xf模块失败: {e}')
    except Exception as e:
        print(f'执行xf.main()时出错: {e}')


if __name__ == '__main__':
    main()
