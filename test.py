import os
import re

# تابع برای ویرایش یک فایل .cs
def edit_cs_file(file_path):
    with open(file_path, 'r') as file:
        content = file.read()

        # یافتن متغیرهای Status، Type، Explain، DateInsert در کلاس
        match = re.search(r'class (\w+)', content)
        if match:
            class_name = match.group(1)
            if 'MainEntity' not in content:
                # ارث‌بری از MainEntity
                content = re.sub(r'class (\w+)', r'class \1 : MainEntity', content)
            if not re.search(r'int\s+Status\s*{\s*get;\s*set;\s*}', content):
                # اضافه کردن متغیر Status
                content = re.sub(r'int\s+ID\s*{\s*get;\s*set;\s*}', r'int ID { get; set; }\n    public int Status { get; set; }', content)
            if not re.search(r'int\s+Type\s*{\s*get;\s*set;\s*}', content):
                # اضافه کردن متغیر Type
                content = re.sub(r'int\s+ID\s*{\s*get;\s*set;\s*}', r'int ID { get; set; }\n    public int Type { get; set; }', content)
            if not re.search(r'string\s+Explain\s*{\s*get;\s*set;\s*}', content):
                # اضافه کردن متغیر Explain
                content = re.sub(r'int\s+ID\s*{\s*get;\s*set;\s*}', r'int ID { get; set; }\n    public string Explain { get; set; }', content)
            if not re.search(r'System\.DateTime\s+DateInsert\s*{\s*get;\s*set;\s*}', content):
                # اضافه کردن متغیر DateInsert با System.DateTime
                content = re.sub(r'int\s+ID\s*{\s*get;\s*set;\s*}', r'int ID { get; set; }\n    public System.DateTime DateInsert { get; set; }', content)

    # نوشتن تغییرات به فایل
    with open(file_path, 'w') as file:
        file.write(content)

# مسیر فولدر مورد نظر
folder_path = 'C:\\Users\\SistanAlaptop\\source\\repos\\___BACKUPS\\Entities'

# پیمایش تمام فایل‌های .cs در فولدر
for root, dirs, files in os.walk(folder_path):
    for file in files:
        if file.endswith('.cs'):
            file_path = os.path.join(root, file)
            edit_cs_file(file_path)
