import re
# check = bool(
#     re.search("/^([a-z0-9_\.-]+)@([\da-z\.-]+)\.([a-z\.]{2,6})$/", "hana840101@gmail.com"))
regex = re.compile(
    r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
check = bool(re.search(regex, "hana840101@yahoo.com.tw"))
print(check)
