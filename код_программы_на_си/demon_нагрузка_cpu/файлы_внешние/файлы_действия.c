// работа с внешними файлами в том числе запись и чтение файлов, 
// добавление информации к текущему (существующему) файлу
// работа с ЛОГ ФАЙЛАМИ

#include <stdio.h> 
#include <stdlib.h> 
#include <string.h>
#include <wctype.h> 
#include <wchar.h> 
#include <time.h> 
/* #include <libpq-fe.h>   // есть /usr/include/postgresql/ */
#include <ctype.h>
#include <iso646.h>
#include <stdbool.h>
#include <uchar.h>  //  /usr/include/uchar.h
#include <locale.h>
#include <math.h>
#include <threads.h> 
#include <unistd.h> // для sleep() read()
#include <errno.h> // return EXIT_SUCCESS; 


#include "глобальные_переменные.h" 
#include "системные_функции.h" 




// тестовая запись в лог файл. Возможно, что запись в данную директорию запрещена или что данный файл имеет урезанные права
int f_логфайл_тест_записи(void)
{
    
    errno = 0;	
    FILE *лог_файл = fopen(глоб_логфайл_путь, "a");
    
    int error_num = errno;
    
    if (лог_файл == NULL) 
    {        
            //  !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        locale_t locale = newlocale(LC_ALL_MASK, "ru_RU.UTF-8", (locale_t) 0);
        char* ошибка=strerror_l(error_num, locale); 
        
        if (1 == глоб_режим_тестов)
        {
            fprintf(stderr, "\nFile : %s \nLine : %d \nCurrent function : %s() \nFailed function : %s() \nError message : %s\n", 
                                __FILE__,        __LINE__,       __func__,              "fopen",                  ошибка);
                    // File : /home/postgres/Документы/_отдельные_программы_си/001_demon_нагрузка_cpu/demon_нагрузка_cpu/файлы_внешние/файлы_действия.c 
                    // Line : 58 
                    // Current function : f_логфайл_тест_записи() 
                    // Failed function : fopen() 
                    // Error message : Нет такого файла или каталог
        }
        else
        {
            fprintf(stderr, "f_логфайл_тест_записи. Сообщение об ошибке (%d) : %s\n", error_num, ошибка);
            printf("%s \n", ошибка);
                    // Error message (2)  : Нет такого файла или каталога
                    // Нет такого файла или каталога 
        }

        freelocale(locale); 
        fclose(лог_файл);
        
        return -1;
    }
    
    f_дата_время_текст_значение();

    fputs(глоб_время_как_текст,  лог_файл);
    fputs("Тестовая запись проверки корректности пути лог.файла. \n", лог_файл);
    fclose(лог_файл);
            
    return 0;
}



// Запись ошибки в предопределённый ранее лог.файла (учет ошибок, действий)
int f_логфайл_запись_сообщения(const char* текст_сообщения)
{
    // просто записываем в журнал сообщение, что пришло.
    // Пришедшее сообщение уже должно быть полностью отформатировано для записи, то есть иметь временную метку и все необходимые поля.

    long int размер_логжурнала=0;
    
    errno = 0;	
    FILE *лог_файл = fopen(глоб_логфайл_путь, "a");
    
    int error_num = errno;
    
    if (лог_файл == NULL) 
    {        
        locale_t locale = newlocale(LC_ALL_MASK, "ru_RU.UTF-8", (locale_t) 0);
        char* ошибка=strerror_l(error_num, locale);
        fprintf(stderr, "f_логфайл_тест_записи. Сообщение об ошибке (%d) : %s\n", error_num, ошибка);
        printf("%s \n", ошибка);

        freelocale(locale); 
        fclose(лог_файл);
        
        return 0;
    }
    
    
    // определить его размер если более 3 Мб - то обнуляем его (создаём новый файл)
    размер_логжурнала = f_размер_логжурнала();
    if (размер_логжурнала > 3000*1000)
    {
        fclose(лог_файл);
        f_пауза_вработе_программы(0, 0.6);
        
        FILE *лог_файл = fopen(глоб_логфайл_путь, "w");
        f_пауза_вработе_программы(0, 0.4);
    }

    fputs(текст_сообщения, лог_файл);
    fputs("\n", лог_файл);
    fclose(лог_файл);
    
    return 0;
}



