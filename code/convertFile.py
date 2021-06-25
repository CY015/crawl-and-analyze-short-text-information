import os


def convert_file(file_dir,new_dir,desc_type,previous_type):
    error_list = list()
    for root,dirs,files in os.walk(file_dir):
        for file in files:
            file_path = os.path.join(root,file)

            try:
                with open(file_path, "rb") as f:

                    res = f.read().decode(previous_type).encode("utf-8").decode("utf-8-sig")   # decode 是将二进制bytes编码转换为unicode,
                with open(os.path.join(new_dir,file),"w",encoding=desc_type) as f:  # encode 是将unicode编码转换为其他编码
                    f.write(res)
            except Exception as e:
                print("file :{} because error : [{}] continue".format(file,e))
                error_list.append(file)
                continue
        if error_list:
            with open("./convert_error/error.txt","w",encoding="utf-8") as f:
                data = "\r\n".join(error_list)
                f.write(data)


# 如果想要知道原始文件的格式,使用notepad++/VS Code打开文件,右下角有文件的编码格式
if __name__ == '__main__':

    # 要将utf-16转utf-8的文件放在此文件夹下
    file_dir = "F:/1_University/3_大三/1NLP/dict"
    new_dir = "F:/1_University/3_大三/1NLP/dict-utf8"
    desc_type = "utf-8"
    previous_type = "utf-16"   # UCS-2 Little Endian(即 utf-16)
    convert_file(file_dir,new_dir,desc_type,previous_type)