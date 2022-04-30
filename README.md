# PyHutool
<p align="center">
	<a href="https://pyhutool.readthedocs.org"><img src="https://www.xujiantao.com/images/pyhutool-logo.png" width="45%"></a>
</p>
<p align="center">
	<strong>🍬A set of tools that keep Python sweet.</strong>
</p>
<p align="center">
	👉 <a href="https://pyhutool.readthedocs.org">https://pyhutool.readthedocs.org</a> 👈
</p>

<p align="center">

[![Documentation Status](https://readthedocs.org/projects/pyhutool/badge/?version=latest)](https://pyhutool.readthedocs.io/en/latest/?badge=latest)
[![GitHub license](https://img.shields.io/github/license/KAY53N/PyHutool)](https://github.com/KAY53N/PyHutool/blob/main/LICENSE)
[![GitHub issues](https://img.shields.io/github/issues/KAY53N/PyHutool)](https://github.com/KAY53N/PyHutool/issues)
[![GitHub stars](https://img.shields.io/github/stars/KAY53N/PyHutool)](https://github.com/KAY53N/PyHutool/stargazers)

</p>

<br />

## 📚简介
PyHutool是一个小而全的Java工具类库，借鉴Java的[Hutool](https://github.com/dromara/hutool) <br /><br />
PyHutool中的工具方法来自每个用户的精雕细琢，它涵盖了Python开发底层代码中的方方面面，它既是大型项目开发中解决小问题的利器，也是小型项目中的效率担当<br /><br />
PyHutool是项目中“util”包友好的替代，它节省了开发人员对项目中公用类和公用工具方法的封装时间，使开发专注于业务，同时可以最大限度的避免封装不完善带来的bug<br />

### 🍺PyHutool如何改变我们的coding方式
PyHutool的目标是使用一个工具方法代替一段复杂代码，从而最大限度的避免“复制粘贴”代码的问题，彻底改变我们写代码的方式。
以截图为例：
- 👴【以前】打开搜索引擎 -> 搜“Python 截图” -> 打开某篇博客-> 复制粘贴 -> 改改好用
- 👦【现在】引入PyHutool  -> gui.screenshot('test.png')
PyHutool的存在就是为了减少代码搜索成本，避免网络上参差不齐的代码出现导致的bug。
-------------------------------------------------------------------------------

## 🛠️包含组件
| 模块                | 介绍                               |
| -------------------|----------------------------------|
| pyhutool.core        | 核心，包括文件处理、数据转换、日期、各种Util等        |
| pyhutool.gui         | 自动化库，包含按键、鼠标、截图的操作等              |
| pyhutool.system         | 获取系统相关信息，如显示器数量，当前窗口标题，系统运行的应用信息 |
| pyhutool.crypto         | 加密解密模块，提供对称、非对称和摘要算法封装           |
| pyhutool.cryptocurrency | 加密货币相关类库封装       |

## 📝文档 
[📘中文文档](https://pyhutool.readthedocs.io/zh_CN/latest/index.html) Full documentation available at https://pyhutool.readthedocs.io/zh_CN/latest/index.html
<br />
[📘English Documentation](https://pyhutool.readthedocs.io/en/latest/index.html) Full documentation available at https://pyhutool.readthedocs.io/en/latest/index.html

## 📦安装
```shell
pip install pyhutool
```