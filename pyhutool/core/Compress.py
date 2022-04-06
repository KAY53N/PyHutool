import os


class Zip:
    # 创建压缩文件方法，可指定文件路径、压缩文件路径、密码
    @staticmethod
    def create_zip(file_path, zip_path, password=None):
        import zipfile
        zip_file = zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED)
        if password:
            zip_file.setpassword(password)
        for root, dirs, files in os.walk(file_path):
            for file in files:
                zip_file.write(os.path.join(root, file))
        zip_file.close()

    # 解压缩文件方法
    @staticmethod
    def unzip(zip_path, file_path):
        import zipfile
        zip_file = zipfile.ZipFile(zip_path, 'r')
        for file in zip_file.namelist():
            zip_file.extract(file, file_path)
        zip_file.close()

    # 解压压缩包中指定文件
    @staticmethod
    def unzip_file(zip_path, file_name, file_path):
        import zipfile
        zip_file = zipfile.ZipFile(zip_path, 'r')
        zip_file.extract(file_name, file_path)
        zip_file.close()

    # 解压缩文件夹方法
    @staticmethod
    def unzip_dir(zip_path, dir_path):
        import zipfile
        zip_file = zipfile.ZipFile(zip_path, 'r')
        for file in zip_file.namelist():
            zip_file.extract(file, dir_path)
        zip_file.close()

    # 查看压缩文件内容方法，返回压缩文件内容列表
    @staticmethod
    def zip_content(zip_path):
        import zipfile
        zip_file = zipfile.ZipFile(zip_path, 'r')
        return zip_file.namelist()