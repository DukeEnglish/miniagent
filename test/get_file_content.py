import os

class MarkdownDocumenter:
    def __init__(self, directory, output_file, whitelist=None, blacklist=None):
        self.directory = directory
        self.output_file = output_file
        # 转换列表为集合，便于快速查找
        self.whitelist = set(whitelist) if whitelist else None
        self.blacklist = set(blacklist) if blacklist else None

    def document_files(self):
        with open(self.output_file, 'w', encoding='utf-8') as md_file:
            for root, dirs, files in os.walk(self.directory):
                for file in files:
                    # 构造文件的完整路径
                    file_path = os.path.join(root, file)
                    # 检查文件是否在白名单或黑名单中
                    if self.is_allowed_file(file, root):
                        
                        self.write_file_to_markdown(file_path, md_file)

    def is_allowed_file(self, file, root):
        # 获取文件相对于目录的路径
        # relative_path = os.path.relpath(os.path.join(root, file), self.directory)
        # print(file, self.whitelist)
        # 检查文件是否在白名单中或不在黑名单中
        if self.whitelist and file not in self.whitelist:
            return False
        if self.blacklist and file in self.blacklist:
            return False
        # 如果没有指定白名单，则默认所有文件都允许
        return True

    def write_file_to_markdown(self, file_path, md_file):
        print(file_path)
        file_suffix = file_path.strip().split(".")[-1]
        if not file_suffix or file_suffix not in ("py", "txt", "md", "css", "html", "js"):
            return
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read().strip()  # 读取内容并去除首尾空白字符
            file_name = os.path.basename(file_path)
            file_extension = os.path.splitext(file_path)[1][1:]  # 获取文件扩展名
            self.format_and_write(md_file, file_name, content, file_extension)

    def format_and_write(self, md_file, file_name, content, file_extension):
        # 根据文件扩展名确定代码块的语言
        language = file_extension if file_extension in ['python', 'js', 'html', 'css'] else 'text'
        md_file.write(f'## `{file_name}`\n```{language}\n{content}\n```\n\n')

if __name__ == "__main__":
    # directory = input("Enter the directory path to read files from: ")
    # output_file = input("Enter the output markdown file path: ")
    # whitelist_input = input("Enter file names for whitelist (comma-separated, leave empty if none): ")
    # blacklist_input = input("Enter file names for blacklist (comma-separated, leave empty if none): ")
    directory = "../agent_web/"
    output_file = "ttt2.md"
    whitelist_input = ""
    blacklist_input = ".DS_Store,config.py"
    # 将输入的字符串转换为列表，去除空白字符
    whitelist = [name.strip() for name in whitelist_input.split(',')] if whitelist_input else None
    blacklist = [name.strip() for name in blacklist_input.split(',')] if blacklist_input else None
    

    documenter = MarkdownDocumenter(directory, output_file, whitelist, blacklist)
    documenter.document_files()