
add_library(vhodn_dannie STATIC входные_данные.c) 

include_directories(../main_program)
include_directories(../бд_запросы)
include_directories(../блок_нагрузка_пк)
include_directories(../настр_ключи_при_запуске)
include_directories(../ошибки_обработка)
include_directories(../системные_команды)
include_directories(../файлы_внешние)
include_directories(/usr/include/postgresql) # include <libpq-fe.h> OK
