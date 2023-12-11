# SET(BUILD_SHARED_LIBS FALSE) означает, что в данном моделу запрещено создавать динамическую библиотеку
# влияет на все модули, после команды выше = BUILD_SHARED_LIBS FALSE или как STATIC в коде ниже

set (IMPORTED True)

include_directories(../main_program)
include_directories(../бд_запросы)
include_directories(../блок_нагрузка_пк)
include_directories(../настр_ключи_при_запуске)
include_directories(../ошибки_обработка)
include_directories(../системные_команды)
include_directories(../файлы_внешние)
include_directories(/usr/include/postgresql) # include <libpq-fe.h> OK

add_executable(${PROJECT_NAME} main.c) 	# названием модуля main.c он же потом нужен будет при компиляции проекта.
	# Название ТОЛЬКО латиницей, иначе будет ошибка при компиляции (даже на самом свежем Debian

