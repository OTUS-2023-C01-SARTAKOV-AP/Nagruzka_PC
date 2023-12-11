
add_library(zaprosi_in_db STATIC запросы_к_бд.c) 

find_package(PostgreSQL)

include_directories(../main_program)
include_directories(../бд_запросы)
include_directories(../блок_нагрузка_пк)
include_directories(../настр_ключи_при_запуске)
include_directories(../ошибки_обработка)
include_directories(../системные_команды)
include_directories(../файлы_внешние)
include_directories(/usr/include/postgresql) # include <libpq-fe.h> OK


set (IMPORTED True)
find_file(PostgreSQL 16.0) 	# OK

message(STATUS "\nИщем библиотеку PostgreSQL: <libpq-fe.h> и ...*/libpq.so ")
message(STATUS "PostgreSQL_FOUND (find_package)= ${PostgreSQL_FOUND}")		# Верный, если PostgreSQL найден.
message(STATUS "PostgreSQL_LIBRARIES = ${PostgreSQL_LIBRARIES}")			# библиотеки PostgreSQL необходимы для соединения
message(STATUS "PostgreSQL_INCLUDE_DIRS = ${PostgreSQL_INCLUDE_DIRS}") 		# каталоги заголовков PostgreSQL
message(STATUS "PostgreSQL_LIBRARY_DIRS = ${PostgreSQL_LIBRARY_DIRS}") 		# каталоги ссылок для библиотек PostgreSQL
message(STATUS "PostgreSQL_VERSION_STRING = ${PostgreSQL_VERSION_STRING}") 	# версия PostgreSQL найдена

