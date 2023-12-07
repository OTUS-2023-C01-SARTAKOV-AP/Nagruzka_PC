
// Данный блок функций сохраняет результаты работы текущей программы в таблице БД PostgreSQL
// здесь собраны функции по запросам к БД в частности ежесекундная выборка  данных о нагрузке сервера

#include <stdio.h> // perror()
#include <stdlib.h> 
#include <string.h>
#include <wctype.h> 
#include <wchar.h> 
#include <time.h> 
#include <ctype.h>
#include <iso646.h>
#include <stdbool.h>
#include <uchar.h>  //  /usr/include/uchar.h
#include <locale.h>
#include <errno.h> // return EXIT_SUCCESS; 


#include <libpq-fe.h>   // есть /usr/include/postgresql/ */
#include "глобальные_переменные.h" 
#include "ошибки_обработка.h"






// static PGconn *соединение; // этот переменная для соединения с БД 9указатель на имя и сам факт подсоединения к БД 
static PGconn* f_соединение_бд(void)
{
    
    char настройки_соединения[1024]=""; 
    char настройки_message[1024]=""; 
    strcat(настройки_соединения, " dbname=");
    strcat(настройки_соединения, глоб_об_ключи_запуска.arws_db);
    
        if (0==strcmp("localhost", глоб_об_ключи_запуска.arws_host))
        {  
            // при наличии записи host=localhost в ответах на ошибку - ВСЕ ЗАПИСИ ПОВТОРЯЮТСЯ ДВА РАЗА !!!! одинаковые строки и каждый раз парами!
            //strcat(настройки_соединения, " host="); 
            //strcat(настройки_соединения, глоб_об_ключи_запуска.arws_host); 
        }
        else
        {
            strcat(настройки_соединения, " hostaddr="); 
            strcat(настройки_соединения, глоб_об_ключи_запуска.arws_host); 
        }

    strcat(настройки_соединения, " port="); 
    strcat(настройки_соединения, глоб_об_ключи_запуска.порт_бд); 
    strcat(настройки_соединения, " user=");
    strcat(настройки_соединения, глоб_об_ключи_запуска.arws_user);
    
    strcpy(настройки_message, настройки_соединения); // сообщения для вывода в терминал БЕЗ ПАРОЛЯ пользователя
    strcat(настройки_message, " пароль=*****");
    
    strcat(настройки_соединения, " password=");
    strcat(настройки_соединения, глоб_об_ключи_запуска.arws_пароль);
    
    
    
    PGconn *соединение = PQconnectdb(настройки_соединения); 
        // настройки_соединения);  " dbname=test_4 port=5432 user=postgres password=11111")
        // $ PGHOST=monster PGUSER=neil ./program так уснанавливаются глобальные переменные, в нашем случае не есть хорошо 
    
    PQsetErrorContextVisibility(соединение,  PQSHOW_CONTEXT_ALWAYS);
    PQsetErrorVerbosity(соединение,  PQERRORS_VERBOSE);
    char er_msg[1000]="# ";
    strcat(er_msg, PQerrorMessage(соединение));   
    
    
    // вывод тестового сообщения, если активирован нужный параметр при запуске программы
    if (1 == глоб_об_ключи_запуска.тест_сообщ)
    {
        printf("\n Соединение будет происходить к ХОСТУ: \t %s\n", PQhost(соединение) );
        printf(" Настройка соединения: \t %s\n", настройки_message );
    }
    

    
    if (PQstatus(соединение) == CONNECTION_OK)
    {
        if (1 == глоб_об_ключи_запуска.тест_сообщ)
        {
            printf("\n --->>> ПОЗДРАВЛЯЕМ! Связь с сервером БД успешно установлена!!!\n");
            printf("Кодировка удаленного сервера:\t как число = %d \t как текст = %s\n", 
                PQclientEncoding(соединение), pg_encoding_to_char(PQclientEncoding(соединение)) ); // -1 ошибка определения кодировки
        }
    }
    else if (PQstatus(соединение) == CONNECTION_BAD)
    {
            // запись в текстовой файл об ошибке !!!!
        f_текст_ошибки(er_msg, -10);        
        
        if (1 == глоб_об_ключи_запуска.тест_сообщ)
        {
            printf(" --->>> соединение с 'соединение' НЕ УДАЛОСЬ \n");
            printf(" Настройка соединения: \t %s\n", настройки_message );
            // printf("Кодировка сервера удаленного как число: %d\n", PQclientEncoding(соединение) ); // -1 ошибка определения кодировки
            // printf("Кодировка сервера удаленного как текст: %s\n", pg_encoding_to_char(PQclientEncoding(соединение)) ); 
            // printf("ошибка соединение: \n%s\n", PQerrorMessage(соединение));
                /*  при соединении с Windows , последняя возвращает сообщение об ошибке не в кодировке UTF-8, а в своей Windows Win-1251 или что то похожее на неё  cоединение с соединение НЕ УДАЛОСЬ 
                    ошибка соединение: 
                    connection to server at "192.168.2.50", port 5432 failed: �����:  ������������ "postgres" �� ������ �������� ����������� (�� ������)
                    нужно на сервере ВИНДОУз в файле постгрес.конфиг поменять значение поля lc_messages(string) c Виндоуз1251 на UTF8
                    и тогда у нас при ошибке соединения или ошибках на стороне БД будет отображаться корректные сообщения.
                    так же есть локали сортировки,и имен БД, которые так же можно перевести в UTF8
                        ошибка соединение: 
                        connection to server at "192.168.2.50", port 5432 failed: FATAL:  password authentication failed for user "postgres"                */ 
             
             PQsetClientEncoding(соединение, "UTF8"); // нужна кодировка для Windows
             printf("ошибка соединение: \n%s\n", er_msg);
             printf("Описание ошибки смотри в текстовом файле логов по адресу: \n%s\n", "Здесь указан путь к файлу с сообщениями от программы");
        }
 
        PQfinish(соединение);
        
         // void PQreset(PGconn *conn); 
    }
    
    return соединение;
}













// внесение строки с записью в БД и проверка результата (успешности операции)
static int f_запись_вбд_нагрузки_пк(PGconn *связь_сервер_quik)
{
    // Глобальные переменные, которые активируются в main.c
//char глоб_время_как_текст[50]=""; 
//char глоб_логфайл_путь[СТРОКА_255]=""; 
//int глоб_режим_тестов=0; 
//struct ключи_запуска глоб_об_ключи_запуска;
//struct нагрузка_оперсист глоб_об_нагрузка_оперсист; 


    PGresult *результат_запроса ;    
    long int разница = 0;
   
    char запрос_1[8000]="INSERT into ";
    strcat(запрос_1, глоб_об_ключи_запуска.arws_schema); // имя схемы
    strcat(запрос_1, "."); 
    strcat(запрос_1, глоб_об_ключи_запуска.arws_table);  // имя таблицы
    strcat(запрос_1, " (время, ssd_read_block, ssd_write_block,           swap_read_block, swap_write_block, ram_full_free, ram_ssd_очередь, ram_ssd_запись, "); 
        strcat(запрос_1, " cpu_min, cpu_max, cpu_midle,      ram_used_min, ram_used_max, ram_used_midle, "); // 9(-1)  :  14(-1)
        strcat(запрос_1, " cpu_t_min, cpu_t_max, cpu_t_midle, ");   // 15-17  (14-16 )
        strcat(запрос_1, " ram_доступно_min, ram_доступно_max, ram_доступно_midle, "); 
        strcat(запрос_1, " ram_buf_min, ram_buf_max, ram_buf_midle,           ram_cach_min, ram_cach_max, ram_cach_midle, "); 
    strcat(запрос_1, " ram_user_min, ram_user_max, ram_user_midle) "); 
    
    strcat(запрос_1, " values ((select to_timestamp($1)), $2, $3,      $4, $5, $6, $7, $8, "); 
        strcat(запрос_1, " $9, $10, $11,      $12, $13, $14,  "); 
        strcat(запрос_1, " $15, $16, $17,   "); 
        strcat(запрос_1, " $18, $19, $20,   "); 
        strcat(запрос_1, " $21, $22, $23,   $24, $25, $26, "); 
        strcat(запрос_1, " $27, $28, $29)  "); 
        
    strcat(запрос_1, " ON CONFLICT (время) DO UPDATE  "); 
    strcat(запрос_1, " SET "); 
        strcat(запрос_1, " ssd_read_block = EXCLUDED.ssd_read_block, "); 
        strcat(запрос_1, " ssd_write_block = EXCLUDED.ssd_write_block, "); 
        strcat(запрос_1, " swap_read_block = EXCLUDED.swap_read_block, "); 
        strcat(запрос_1, " swap_write_block = EXCLUDED.swap_write_block, "); 
        strcat(запрос_1, " ram_full_free = EXCLUDED.ram_full_free, "); 
        strcat(запрос_1, " ram_ssd_очередь = EXCLUDED.ram_ssd_очередь, "); 
        strcat(запрос_1, " ram_ssd_запись = EXCLUDED.ram_ssd_запись, "); 
        strcat(запрос_1, " cpu_min = EXCLUDED.cpu_min, "); 
        strcat(запрос_1, " cpu_max = EXCLUDED.cpu_max, "); 
        strcat(запрос_1, " cpu_midle = EXCLUDED.cpu_midle, "); 
        strcat(запрос_1, " ram_used_min = EXCLUDED.ram_used_min, "); 
        strcat(запрос_1, " ram_used_max = EXCLUDED.ram_used_max, "); 
        strcat(запрос_1, " ram_used_midle = EXCLUDED.ram_used_midle, "); 
        strcat(запрос_1, " cpu_t_min = EXCLUDED.cpu_t_min, "); 
        strcat(запрос_1, " cpu_t_max = EXCLUDED.cpu_t_max, "); 
        strcat(запрос_1, " cpu_t_midle = EXCLUDED.cpu_t_midle, "); 
        strcat(запрос_1, " ram_доступно_min = EXCLUDED.ram_доступно_min, "); 
        strcat(запрос_1, " ram_доступно_max = EXCLUDED.ram_доступно_max, "); 
        strcat(запрос_1, " ram_доступно_midle = EXCLUDED.ram_доступно_midle, "); 
        strcat(запрос_1, " ram_buf_min = EXCLUDED.ram_buf_min, "); 
        strcat(запрос_1, " ram_buf_max = EXCLUDED.ram_buf_max, "); 
        strcat(запрос_1, " ram_buf_midle = EXCLUDED.ram_buf_midle, "); 
        strcat(запрос_1, " ram_cach_min = EXCLUDED.ram_cach_min, "); 
        strcat(запрос_1, " ram_cach_max = EXCLUDED.ram_cach_max, "); 
        strcat(запрос_1, " ram_cach_midle = EXCLUDED.ram_cach_midle, "); 
        strcat(запрос_1, " ram_user_min = EXCLUDED.ram_user_min, "); 
        strcat(запрос_1, " ram_user_max = EXCLUDED.ram_user_max, "); 
        strcat(запрос_1, " ram_user_midle = EXCLUDED.ram_user_midle; "); 
    
        // ВНИМАНИЕ. массив со значениями, передаваемый в Постргерс на стороне Си начинается с [0] НО В САМОМ ЗАПРОСЕ данные начинаются с $1  !!!!!
    char *paramValues2[29];
    int циклов = (глоб_об_нагрузка_оперсист.циклов < 1) ? 1: глоб_об_нагрузка_оперсист.циклов;
        // ВНимание !!!! вариант char строка_2[3][64];  sprintf(строка_2[2], "%i", 11456);  paramValues2[2] = строка_2[2];   выводит КУЧУ предупреждений, хоть он и короче!!!  
    char стр0[63]="";
    char стр1[63]="";
    char стр2[63]=""; 
    char стр3[63]="";
    char стр4[63]="";
    char стр5[63]="";
    char стр6[63]="";
    char стр7[63]="";
    char стр8[63]="";
    char стр9[63]="";
    char стр10[63]="";
    char стр11[63]="";
    char стр12[63]="";
    char стр13[63]="";
    char стр14[63]="";
    char стр15[63]="";
    char стр16[63]="";
    char стр17[63]="";
    char стр18[63]="";
    char стр19[63]="";
    char стр20[63]="";
    char стр21[63]="";
    char стр22[63]="";
    char стр23[63]="";
    char стр24[63]="";
    char стр25[63]="";
    char стр26[63]="";
    char стр27[63]="";
    char стр28[63]="";
    sprintf(стр0, "%li", (long int) глоб_об_нагрузка_оперсист.время_начало);        //время
        paramValues2[0] = стр0; 
    разница = (long int) (глоб_об_нагрузка_оперсист.ssd_read_block_new - глоб_об_нагрузка_оперсист.ssd_read_block_old);     // ssd_read_block       
        разница = (разница<1) ? 1 : разница;
        sprintf(стр1, "%li", разница);                     
        paramValues2[1] = стр1;
    разница = (long int) (глоб_об_нагрузка_оперсист.ssd_write_block_new - глоб_об_нагрузка_оперсист.ssd_write_block_old);   // ssd_write_block
        разница = (разница<1) ? 1 : разница;
        sprintf(стр2, "%li", разница);                      
        paramValues2[2] = стр2;
        
    sprintf(стр3, "%i", глоб_об_нагрузка_оперсист.swap_read_block);                         // swap_read_block
        paramValues2[3] = стр3;
    sprintf(стр4, "%i", глоб_об_нагрузка_оперсист.swap_write_block);                        // swap_write_block
        paramValues2[4] = стр4;
    sprintf(стр5, "%5.2lf", (double) (100.0 * глоб_об_нагрузка_оперсист.ram_полность_свободна_кб/глоб_об_нагрузка_оперсист.ram_всего_кб) );      // ram_full_free
        paramValues2[5] = стр5;
    sprintf(стр6, "%i", (int) глоб_об_нагрузка_оперсист.ram_max_очередь_записи_надиск_кб);        // ram_ssd_очередь
        paramValues2[6] = стр6;    
    sprintf(стр7, "%i", (int) глоб_об_нагрузка_оперсист.ram_max_активная_запись_надиск_кб);       // ram_ssd_запись
        paramValues2[7] = стр7;    

    sprintf(стр8, "%5.2lf", глоб_об_нагрузка_оперсист.cpu_min);                 // cpu_min
        paramValues2[8] = стр8;
    sprintf(стр9, "%5.2lf", глоб_об_нагрузка_оперсист.cpu_max);                 // cpu_max
        paramValues2[9] = стр9;
    sprintf(стр10, "%5.2lf", глоб_об_нагрузка_оперсист.cpu_сумма/циклов);       // cpu_midle
        paramValues2[10] = стр10;
    sprintf(стр11, "%5.2lf", 100.0 * глоб_об_нагрузка_оперсист.ram_used_min);                // ram_used_min
        paramValues2[11] = стр11;
    sprintf(стр12, "%5.2lf", 100.0 * глоб_об_нагрузка_оперсист.ram_used_max);                // ram_used_max
        paramValues2[12] = стр12;
    sprintf(стр13, "%5.2lf", 100.0 * (глоб_об_нагрузка_оперсист.ram_used_сумма/циклов) );       // ram_used_midle
        paramValues2[13] = стр13;   

    sprintf(стр14, "%5.2lf", глоб_об_нагрузка_оперсист.cpu_t_min);                // cpu_t_min
        paramValues2[14] = стр14;
    sprintf(стр15, "%5.2lf", глоб_об_нагрузка_оперсист.cpu_t_max);                // cpu_t_max
        paramValues2[15] = стр15;
    sprintf(стр16, "%5.2lf", глоб_об_нагрузка_оперсист.cpu_t_сумма/циклов );       // cpu_t_midle
        paramValues2[16] = стр16;

    sprintf(стр17, "%5.2lf", 100.0 * глоб_об_нагрузка_оперсист.ram_available_min);              // ram_доступно_min
        paramValues2[17] = стр17;   
    sprintf(стр18, "%5.2lf", 100.0 * глоб_об_нагрузка_оперсист.ram_available_max);              // ram_доступно_max
        paramValues2[18] = стр18;
    sprintf(стр19, "%5.2lf", 100.0 * (глоб_об_нагрузка_оперсист.ram_available_сумма/циклов) );     // ram_доступно_midle
        paramValues2[19] = стр19;

    sprintf(стр20, "%5.2lf", 100.0 * глоб_об_нагрузка_оперсист.ram_buffers_min);                // ram_buf_min
        paramValues2[20] = стр20;        
     sprintf(стр21, "%5.2lf", 100.0 * глоб_об_нагрузка_оперсист.ram_buffers_max);               // ram_buf_max
        paramValues2[21] = стр21;           
    sprintf(стр22, "%5.2lf", 100.0 * (глоб_об_нагрузка_оперсист.ram_buffers_сумма/циклов) );       // ram_buf_midle
        paramValues2[22] = стр22;    
    sprintf(стр23, "%5.2lf", 100.0 * глоб_об_нагрузка_оперсист.ram_cached_min);                 // ram_cach_min
        paramValues2[23] = стр23;
    sprintf(стр24, "%5.2lf", 100.0 * глоб_об_нагрузка_оперсист.ram_cached_max);                 // ram_cach_max
        paramValues2[24] = стр24;    
    sprintf(стр25, "%5.2lf", 100.0 * (глоб_об_нагрузка_оперсист.ram_cached_сумма/циклов) );        // ram_cach_midle
        paramValues2[25] = стр25;    
    
    sprintf(стр26, "%5.2lf", 100.0 * глоб_об_нагрузка_оперсист.ram_anon_pages_min);                // ram_user_min
        paramValues2[26] = стр26;    
    sprintf(стр27, "%5.2lf", 100.0 * глоб_об_нагрузка_оперсист.ram_anon_pages_max);                // ram_user_max
        paramValues2[27] = стр27;    
    sprintf(стр28, "%5.2lf", 100.0 * (глоб_об_нагрузка_оперсист.ram_anon_pages_сумма/циклов) );       // ram_user_midle
        paramValues2[28] = стр28;    
        
        
    if (1 == глоб_режим_тестов)
    {
        printf("\n Ниже перечислены значения 29 переменных, которые будут переданы в БД в таблицу нагрузки ПК\n"
        " ВНИАМНИЕ! не должно быть значений '-nan' \n" );
        
        for (int j=0; j<29; j++)
        {
            printf(" [%d] = %s\n", j,  paramValues2[j] );
        }
        
        printf("\n Рашифровка некоторых значений из списка, которые чаще всего меняются:\n"
        " time[0]=%s, tpu_midle[10]=%s, ssd_write_block[2]=%s  ram_ssd_очередь[6]=%s cpu_t_midle[16]=%s \n" 
        " ram_user_min[26] =%s, ram_user_max[27]=%s, ram_user_midle[28]=%s \n\n", 
        paramValues2[0] , paramValues2[10] , paramValues2[2], paramValues2[6], paramValues2[16], 
        paramValues2[26], paramValues2[27], paramValues2[28]);  
    }

    
    

    результат_запроса = PQexecParams(связь_сервер_quik, запрос_1, 29, NULL, \
        paramValues2, NULL, NULL, 0); 

        
    if (PQresultStatus(результат_запроса) == PGRES_COMMAND_OK) 
    {
        
        if (1 == глоб_режим_тестов)
        {
           printf("\t\tВставка строки с данными о нагрузке ПК УСПЕШНО выполнена!\n"); 
        }
    }
    else if (PQresultStatus(результат_запроса) != PGRES_COMMAND_OK)
    {
        PQsetErrorContextVisibility(связь_сервер_quik,  PQSHOW_CONTEXT_ALWAYS);
        PQsetErrorVerbosity(связь_сервер_quik,  PQERRORS_VERBOSE);
        char er_msg[5000]="# ";
        strcat(er_msg, PQerrorMessage(связь_сервер_quik));  // ОДИНАКОВО!!! = strcat(er_msg, PQresultErrorMessage(результат_запроса)); 
        strcat(er_msg, " ");
        //char *Pconst PGresult *res,    PGVerbosity verbosity,  PGContextVisibility show_context);
        // strcat(er_msg, PQresultVerboseErrorMessage(результат_запроса, PQERRORS_VERBOSE, PQSHOW_CONTEXT_ALWAYS));  = ОДИНАКОВО!!!  strcat(er_msg, PQresultErrorMessage(результат_запроса));
        
        
        
        
        printf("\t ОШИБКА: при вставке строки с данными о нагрузке ПК: \n\t %s\n", er_msg); // PQerrorMessage(связь_сервер_quik)
        
        f_текст_ошибки(er_msg, -20);    // запись в текстовой файл об ошибке !!!!
        PQclear(результат_запроса);     // освобождает память области, связанную с    PGresult *результат_запроса
    
        return -20;                     // глобальная таблица ошибок, в которой нумерация это модуль отрицательного номера ошибки, 
    }     
    
     // освобождает память области, связанную с    PGresult *результат_запроса
    PQclear(результат_запроса);
    
    return 0;
}




int f_блок_записи_вбд_нагрузок_пк(void)
{
    int функция_успешно_выполнена;
    
    /*  соединение с БД*/    
    PGconn *связь_сервер_quik = f_соединение_бд();
    
    
    if (PQstatus(связь_сервер_quik) != CONNECTION_OK)
    {
       if (1 == глоб_об_ключи_запуска.тест_сообщ)
       {
            printf("Соединение с сервером НЕ УДАЛОСЬ !!!\n");
            /*   Настройка соединение имеет вид =  dbname=ммвб host=localhost port=5432 user_2=postgres password_2=11111
                 Мы подсоединились к хосту = 
                 --->>> соединение с 'соединение' НЕ УДАЛОСЬ 
                ошибка соединение: 
                invalid connection option "user_2"

                ошибка соединение: 
                invalid connection option "user_2"

                Соединение с сервером НЕ УДАЛОСЬ !!!
                Завершили               */
       }
       return -10;
    }    
    
    
    
    if (1 == глоб_об_ключи_запуска.тест_сообщ)
    {
        // printf("Указатель на соедниение успешно создан! \n");
        // PQsetClientEncoding(связь_сервер_quik, "UTF8"); // ERROR:  invalid value for parameter "client_encoding": "ru_RU.UTF-8"
    }
    
    
    функция_успешно_выполнена = f_запись_вбд_нагрузки_пк(связь_сервер_quik);
    
    if (0 != функция_успешно_выполнена) 
    {
        printf("Описание ошибки смотри в текстовом файле логов по адресу: \n\t\t%s\n", глоб_логфайл_путь);
        PQfinish(связь_сервер_quik);
        
        return -20;
    }

    
    
    // PQreset(связь_сервер_quik) - переустановка соединения с теми же параметрами что и раньше
    PQfinish(связь_сервер_quik); // закрытие подключения к БД и очистка памяти от подключения
    return 0;
    
}




// volatile

/*
static void exit_nicely(PGconn *conn)
{
 PQfinish(conn);
 return;
}

*/