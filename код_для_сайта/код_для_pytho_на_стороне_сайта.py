

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!ваш стандартный код по формированию шапки страницы html

    
# Наполнение сайта (основной контент)
# ******************************************************************************
# ******************************************************************************


import cgi, os, sys
import datetime 
from datetime import date
import psycopg2
import json  


date_now = date.today()
data=cgi.FieldStorage()



if 'data_start' not in data.keys():
    print('''<h1>Нагрузка ПК за указанный день.</h1> ''')

    #Вывод формы, в которой нужно указать период для вывода ошибок
    print('''  <form method="POST" action="f_1300_nagruzka_pc.py">
        <fieldset>
        <legend align="center" style="color:#7e7efd; font-size:25px"> &nbsp; Укажите период дат, за которые нужно предоставить отчёт. &nbsp; </legend>
        <input type="hidden" name="zapros_name" value="1">
        <div> ''')

    print('''Укажите дату вывода графиков:
            <input type="date" name="data_start"  value="{0}" min="2023-11-08"> &nbsp; &nbsp; 
    
             <br>&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;  &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; <br>
             &nbsp; &nbsp; &nbsp;  &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; 
            <input type="submit" class="c-button" value=" Вывести "> 
             <br> &nbsp; <br> 
            </div>
        </fieldset>
           </form>
            <p> &nbsp; <br> '''.format(date_now))






if 'data_start' in data.keys():

	#!!!!!!!!!!!!!!!!!!ваш код для соединения с БД
	#!!!!!!!!!!!!!!!!!!ниже - просто код по сипользованию уже существующей функции
	#    # Соединение с БД PostgreSQL
	#    from f0_conn_db import conn_db
	#    соединение_бд=conn_db()
	#    if соединение_бд=='error_000':
	#        sys.exit()
	#    else:
	#        cur = соединение_бд.cursor()


    json_values={}
    json_values['дата_старт']=str(data.getvalue('data_start'))
    json_values['дата_конец']=str(data.getvalue('data_start'))    # data_end
    json_values['id_роли_в_бд']=str(п_id_роли_в_бд)  
    json_values=json.dumps(json_values, ensure_ascii=False)
    п_запрос="select site_html.f_отчет_нагрузка_пк('{0}'::json)".format(json_values) 
    #print(п_запрос, '<br>')

    cur.execute(п_запрос)
    row = cur.fetchone()
    п_ответ_разбор=row[0] # это вернулся массив json
    #print('<br>', row, '<br>', str(data.getvalue('data_start')), '<br>', str(data.getvalue('data_end')), '<br>', п_ответ_разбор, '<br>')
    # успешно   ошибка


    if п_ответ_разбор['ответ']=='ошибка':   
        print('''<br> Что то пошло не так.<br>
            <font size="4" color="#f33" face="Arial"><b>{0}</b></font><br>
              Если расшифровки ответа нет, то сделайте скриншот страницы и обратитесь к разработику программы. 
              <p>  &nbsp;  </p>  '''.format(п_ответ_разбор['расшифровка_ответа']) 
              )
    else:
        pass 


    # Закрываем подключение.
    # соединение_бд.commit()
    cur.close()
    соединение_бд.close()








# 
# ============ НАЧАЛО Вывода информации ' ====================================
# 
# ============ НАЧАЛО Вывода информации ' ====================================
if ('data_start' in data.keys()) and (п_ответ_разбор['ответ']=='успешно'):   
    print('''<h1>Нагрузка ПК за {0}.</h1> '''.format(str(data.getvalue('data_start')) ))

    п_ответ_разбор=п_ответ_разбор['расшифровка_ответа']


    import matplotlib.pyplot as plt
    import matplotlib as mpl
    import numpy as np
    import matplotlib.ticker as ticker  
     
    import base64
    from io import BytesIO


    p_x_время=np.array(п_ответ_разбор['arr_время'])
    #params = {"ytick.color" : "crimson"}    # "text.color" : "blue", "xtick.color" : "crimson",
    #plt.rcParams.update(params)



    # ПОЛНОСТЬЮ СВОБОДАЯ ОПЕРАТИВНАЯ ПАМЯТЬ 'arr_ram_full_free', arr_ram_full_free, 
    #plt.style.use('default')
    p_график=np.array(п_ответ_разбор['arr_ram_full_free'])
    # блок для отображения графиков
    fig, ax = plt.subplots(1, 1, figsize=(19, 4), dpi=100, facecolor='#ABABAB', edgecolor='#727272', linewidth=10)

        # fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(nrows=2, ncols=2)    
            # https://matplotlib.org/stable/gallery/subplots_axes_and_figures/demo_tight_layout.html#sphx-glr-gallery-subplots-axes-and-figures-demo-tight-layout-py
            # https://matplotlib.org/stable/gallery/images_contours_and_fields/image_annotated_heatmap.html#sphx-glr-gallery-images-contours-and-fields-image-annotated-heatmap-py
        # fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2)          fig, (ax1, ax2) = plt.subplots(nrows=2, ncols=1)

        # добавляем подписи к осям и заголовок диаграммы
    ax.set(title='Оперативная память, которая ПОЛНОСТЮ свободна')
    ax.set_xlabel(r'$Время.$      В  00:15  и  07:45  очистка кэш памяти.', fontsize=10)
    ax.set_ylabel(r'$Проценты$', fontsize=12)    
        # сами графики      # visible=False     '--k'   ':b',
    ax.fill_between(p_x_время, 0, p_график, color='#38ACEC', label=' ВООБЩЕ НИЧЕМ не занятая RAM в % ', alpha=0.5 ) # where=(y < 0)           
    ax.plot(p_x_время, p_график, color='#FA1010', linewidth=2)  #'None' или ' '  linestyle='-.', marker='d'
    ax.set_ylim([9, 82]) # Границы по оси У
        # включаем основную сетку
    ax.grid(which='major', linewidth=1,  linestyle='-', drawstyle='steps', alpha=0.4) # {'default', 'steps', 'steps-pre', 'steps-mid', 'steps-post'}, default: 'default'
    ax.grid(which='minor', linewidth=1, linestyle=':', alpha=0.3)    # дополнительная
        #  Устанавливаем интервал основных делений:
                #ax.xaxis.set_major_locator(ticker.LinearLocator(25))    # жестко задано количество вертикальных линий (меток на оси Х)
    ax.xaxis.set_major_locator(ticker.MultipleLocator(15)) # Интервал между метками. При 15 = 300/15 = 20 делений !!!! 15 оптимум! 12 уже очень близка (каша)
    ax.yaxis.set_major_locator(ticker.MultipleLocator(10))
    ax.yaxis.set_minor_locator(ticker.MultipleLocator(5)) 
                #ax[0].xticks(rotation=90)      # ax.tick_params(axis='x', labelrotation=15)
            # выводим легенду
    ax.legend(loc='lower left', bbox_to_anchor=(0.02, 0.999), fontsize=9)     #'upper left', bbox_to_anchor=(0.5, 0.5)  'upper right'   'lower right'  
    plt.tight_layout(pad=0.4, w_pad=0.5, h_pad=1.0)
    #plt.tight_layout(rect=[None, None, 0.45, None])
        # Установка расстояния между таблицами
    plt.subplots_adjust(wspace=0, hspace=0.35)
    plt.show()

        # Вывод графика как b64encode
    tmpfile = BytesIO()
    plt.savefig(tmpfile, format='png')
    encoded = base64.b64encode(tmpfile.getvalue()).decode('utf-8')
    print('''
    <div class="display_data">
    <div class="output_subarea output_image">
    <img src="data:image/png;base64,{}" class="unconstrained">
    </div>
    </div>'''.format(encoded))











        # Оперативная память. Занятая пользовательскими приложениями (в т.ч и Си программы)
    plt.style.use('default')
    p_ram_min=np.array(п_ответ_разбор['arr_ram_user_min'])
    p_ram_max=np.array(п_ответ_разбор['arr_ram_user_max'])
    p_ram_midl=np.array(п_ответ_разбор['arr_ram_user_midle'])

        # блок для отображения графиков
    fig, ax = plt.subplots(1, 1, figsize=(19, 4), dpi=100, facecolor='#ABABAB', edgecolor='#727272', linewidth=10)
        # добавляем подписи к осям и заголовок диаграммы
    ax.set(title=r'$Оперативная$ $память.$  $Занятая$ $пользовательскими$ $приложениями$ $(в$ $т.ч.$ $и$ $Си$ $программы)$')
    ax.set_xlabel(r'$Время$', fontsize=10)
    ax.set_ylabel(r'$Проценты$ $от$ $всей$ $RAM$', fontsize=12)    
        # сами графики
    ax.fill_between(p_x_время, p_ram_min, p_ram_max, color='#0000FF', label='user RAM. Дельта MAX-MIN', alpha=0.2 ) # where=(y < 0)           
    ax.plot(p_x_время, p_ram_max, ':b',  label='максимум',  linewidth=1, alpha=0.9 )   # п_ответ_разбор['arr_cpu_max']
    ax.plot(p_x_время, p_ram_min, '--k', label='минимум',  linewidth=1) # visible=False
    ax.plot(p_x_время, p_ram_midl, color='#FA1010', label='математ.средняя', linewidth=2)
    ax.set_ylim([3, 43]) # Границы по оси У
        # включаем основную сетку
    ax.grid(which='major', linewidth=1, linestyle='-.', drawstyle='steps', alpha=0.4) # основная сетка
    ax.grid(which='minor', linewidth=1, linestyle=':', alpha=0.3)    # дополнительная
        #  Устанавливаем интервал основных делений:
    ax.xaxis.set_major_locator(ticker.MultipleLocator(15))
    ax.yaxis.set_major_locator(ticker.MultipleLocator(10))
    ax.yaxis.set_minor_locator(ticker.MultipleLocator(5))
        # выводим легенду
    ax.legend(loc='upper left', bbox_to_anchor=(0.01, 0.98), fontsize=9)  
    plt.tight_layout(pad=0.4, w_pad=0.5, h_pad=1.0)
    #plt.tight_layout(rect=[None, None, 0.45, None])
        # Установка расстояния между таблицами
    plt.subplots_adjust(wspace=0, hspace=0.35)
    plt.show()

        # Вывод графика как b64encode
    tmpfile = BytesIO()
    plt.savefig(tmpfile, format='png')
    encoded = base64.b64encode(tmpfile.getvalue()).decode('utf-8')
    print('''
    <div class="display_data">
    <div class="output_subarea output_image">
    <img src="data:image/png;base64,{}" class="unconstrained">
    </div>
    </div>'''.format(encoded))


 


        # Оперативная память. Используемая часть (та что не может быть освобождена) 
    plt.style.use('default')
    p_ram_min=np.array(п_ответ_разбор['arr_ram_used_min'])
    p_ram_max=np.array(п_ответ_разбор['arr_ram_used_max'])
    p_ram_midl=np.array(п_ответ_разбор['arr_ram_used_midle'])

        # блок для отображения графиков
    fig, ax = plt.subplots(1, 1, figsize=(19, 4), dpi=100, facecolor='#ABABAB', edgecolor='#727272', linewidth=10)
        # добавляем подписи к осям и заголовок диаграммы
    ax.set(title=r'Оперативная память. Используемая часть (та что не может быть освобождена)')
    ax.set_xlabel(r'$Время$', fontsize=10)
    ax.set_ylabel(r'$Проценты$ $от$ $всей$ $RAM$', fontsize=12)  
        # сами графики
    ax.fill_between(p_x_время, p_ram_min, p_ram_max, color='#C38EC7', label='Дельта MAX-MIN', alpha=0.2 ) # where=(y < 0)           
    ax.plot(p_x_время, p_ram_max, ':b',  label='максимум',  linewidth=1, alpha=0.9 )   # п_ответ_разбор['arr_cpu_max']
    ax.plot(p_x_время, p_ram_min, '--k', label='минимум',  linewidth=1) # visible=False
    ax.plot(p_x_время, p_ram_midl, color='#3EA055', label='математ.средняя', linewidth=2)
    ax.set_ylim([3, 43]) # Границы по оси У
        # включаем основную сетку
    ax.grid(which='major', linewidth=1, linestyle='-.', drawstyle='steps', alpha=0.4) # основная сетка
    ax.grid(which='minor', linewidth=1, linestyle=':', alpha=0.3)    # дополнительная
        #  Устанавливаем интервал основных делений:
    ax.xaxis.set_major_locator(ticker.MultipleLocator(15))
    ax.yaxis.set_major_locator(ticker.MultipleLocator(10))
    ax.yaxis.set_minor_locator(ticker.MultipleLocator(5))
            # выводим легенду
    ax.legend(loc='upper left', bbox_to_anchor=(0.01, 0.98), fontsize=9) 
    plt.tight_layout(pad=0.4, w_pad=0.5, h_pad=1.0)
    #plt.tight_layout(rect=[None, None, 0.45, None])
        # Установка расстояния между таблицами
    plt.subplots_adjust(wspace=0, hspace=0.35)
    plt.show()

        # Вывод графика как b64encode
    tmpfile = BytesIO()
    plt.savefig(tmpfile, format='png')
    encoded = base64.b64encode(tmpfile.getvalue()).decode('utf-8')
    print('''
    <div class="display_data">
    <div class="output_subarea output_image">
    <img src="data:image/png;base64,{}" class="unconstrained">
    </div>
    </div>'''.format(encoded))



















        # НАГРУЗКА ПРОЦЕССОРА 
    #plt.style.use('default')
    p_min=np.array(п_ответ_разбор['arr_cpu_min'])
    p_max=np.array(п_ответ_разбор['arr_cpu_max'])
    p_midl=np.array(п_ответ_разбор['arr_cpu_midle'])

    p_t_cpu_min=np.array(п_ответ_разбор['arr_cpu_t_min'])
    p_t_cpu_max=np.array(п_ответ_разбор['arr_cpu_t_max'])
    p_t_cpu_midl=np.array(п_ответ_разбор['arr_cpu_t_midle'])

        # блок для отображения графиков
    fig, ax = plt.subplots(1, 1, figsize=(19, 4), dpi=100, facecolor='#ABABAB', edgecolor='#727272', linewidth=10)
        # добавляем подписи к осям и заголовок диаграммы
    ax.set(title=r'$Суммарная$  $нагрузки$ $всех$ $ядер$ $центрального$ $процессора$')
    ax.set_xlabel(r'$Время$', fontsize=10)
    ax.set_ylabel(r'$Проценты$', fontsize=12)    
        # сами графики
    ax.fill_between(p_x_время, p_min, p_max, color='#0000FF', label='Дельта MAX-MIN', alpha=0.2 ) # where=(y < 0)           
    ax.plot(p_x_время, p_max, ':b',  label='максимум',  linewidth=1, alpha=0.9 )   # п_ответ_разбор['arr_cpu_max']
    ax.plot(p_x_время, p_min, '--k', label='минимум',  linewidth=1) # visible=False
    ax.plot(p_x_время, p_midl, color='#FA1010', label='средняя нагрузка', linewidth=3)
    ax.set_ylim([0, 83]) # Границы по оси У
        # выводим легенду
    ax.legend(loc='upper left', bbox_to_anchor=(0.01, 0.98), fontsize=9)     #'upper left', bbox_to_anchor=(0.5, 0.5)  'upper right'   'lower right'  
    plt.tight_layout(pad=0.4, w_pad=0.5, h_pad=1.0)
    #plt.tight_layout(rect=[None, None, 0.45, None])
        # включаем основную сетку
    ax.grid(which='major', linewidth=1,  linestyle='-', drawstyle='steps', alpha=0.2) # {'default', 'steps', 'steps-pre', 'steps-mid', 'steps-post'}, default: 'default'
        #  Устанавливаем интервал основных делений:
    #ax.xaxis.set_major_locator(ticker.LinearLocator(25))    # жестко задано количество вертикальных линий (меток на оси Х)
    ax.xaxis.set_major_locator(ticker.MultipleLocator(15)) # Интервал между метками. При 15 = 300/15 = 20 делений !!!! 15 оптимум! 12 уже очень близка (каша)
    #ax[0].xticks(rotation=90)      # ax.tick_params(axis='x', labelrotation=15)
        # Установка расстояния между таблицами
    plt.subplots_adjust(wspace=0, hspace=0.35)
    plt.show()

        # Вывод графика как b64encode
    tmpfile = BytesIO()
    plt.savefig(tmpfile, format='png')
    encoded = base64.b64encode(tmpfile.getvalue()).decode('utf-8')
    print('''
    <div class="display_data">
    <div class="output_subarea output_image">
    <img src="data:image/png;base64,{}" class="unconstrained">
    </div>
    </div>'''.format(encoded))













        # ТЕМПЕРАТУРА ПРОЦЕССОРА 
    plt.style.use('default')
    p_t_cpu_min=np.array(п_ответ_разбор['arr_cpu_t_min'])
    p_t_cpu_max=np.array(п_ответ_разбор['arr_cpu_t_max'])
    p_t_cpu_midl=np.array(п_ответ_разбор['arr_cpu_t_midle'])

        # блок для отображения графиков
    fig, ax = plt.subplots(1, 1, figsize=(19, 4), dpi=100, facecolor='#ABABAB', edgecolor='#727272', linewidth=10)
        # добавляем подписи к осям и заголовок диаграммы
    ax.set(title=r' $Температура$ $первого$ $ядра$ $процессора$ $(самого$ $горячего)$')
    ax.set_xlabel(r' $Время$ ', fontsize=10)
    ax.set_ylabel(r' $Градусы$  $цельсия$ ', fontsize=12)    
        # сами графики
    ax.fill_between(p_x_время, p_t_cpu_min, p_t_cpu_max, color='#EE9A4D', label='Дельта MAX-MIN', alpha=0.2 ) # where=(y < 0)           
    ax.plot(p_x_время, p_t_cpu_max, ':b',  label='t максимум гр.C',  linewidth=1, alpha=0.9 )   # п_ответ_разбор['arr_cpu_max']
    ax.plot(p_x_время, p_t_cpu_min, '--k', label='t минимум гр.C',  linewidth=1) # visible=False
    ax.set_ylim([35, 105]) # Границы по оси У
    ax.plot(p_x_время, p_t_cpu_midl, color='#FA1010', label='t средняя гр.C', linewidth=3)
        # выводим легенду
    ax.legend(loc='upper left', bbox_to_anchor=(0.01, 0.98), fontsize=9)     #'upper left', bbox_to_anchor=(0.5, 0.5)  'upper right'   'lower right'  
    plt.tight_layout(pad=0.4, w_pad=0.5, h_pad=1.0)
    #plt.tight_layout(rect=[None, None, 0.45, None])
        # включаем основную сетку
    ax.grid(which='major', linewidth=1,  linestyle='-', drawstyle='steps', alpha=0.2) # {'default', 'steps', 'steps-pre', 'steps-mid', 'steps-post'}, default: 'default'
        #  Устанавливаем интервал основных делений:
    #ax.xaxis.set_major_locator(ticker.LinearLocator(25))    # жестко задано количество вертикальных линий (меток на оси Х)
    ax.xaxis.set_major_locator(ticker.MultipleLocator(15)) # Интервал между метками. При 15 = 300/15 = 20 делений !!!! 15 оптимум! =75 минут 12 уже очень близка (каша)
    #ax[0].xticks(rotation=90)      # ax.tick_params(axis='x', labelrotation=15)
   
        # Установка расстояния между таблицами
    plt.subplots_adjust(wspace=0, hspace=0.35)
    plt.show()

        # Вывод графика как b64encode
    tmpfile = BytesIO()
    plt.savefig(tmpfile, format='png')
    encoded = base64.b64encode(tmpfile.getvalue()).decode('utf-8')
    print('''
    <div class="display_data">
    <div class="output_subarea output_image">
    <img src="data:image/png;base64,{}" class="unconstrained">
    </div>
    </div>'''.format(encoded))










         # SSD диск. Чтение и запись блоков за 5 минут
    plt.style.use('default')
    p_ssd_read=np.array(п_ответ_разбор['arr_ssd_read_block'])
    p_ssd_write=np.array(п_ответ_разбор['arr_ssd_write_block'])

        # блок для отображения графиков
    fig, ax = plt.subplots(1, 1, figsize=(19, 4), dpi=100, facecolor='#ABABAB', edgecolor='#727272', linewidth=10)         
        # добавляем подписи к осям и заголовок диаграммы
    ax.set(title=r'$SSD$ $диск.$ $Чтение$ $и$ $запись$ $блоков$ $за$ $5$ $минут$  ЛОГАРИФМИЧЕСКАЯ ШКАЛА')
    ax.set_xlabel(r' $Время$ ', fontsize=10)
    ax.set_ylabel(r' $блоков,$  $штук$ ', fontsize=12) 
        # сами графики        
    ax.step(p_x_время, p_ssd_read, label='Прочитано с диска блоков', color='#BABABA', linestyle='-') 
    ax.plot(p_x_время, p_ssd_write, color='#6495ED', label='Записано на диск блоков', linewidth=2) 
        # выводим легенду
    ax.legend(loc='upper left', bbox_to_anchor=(0.0, 1.07), fontsize=9)
    ax.set_yscale('log')    
        # включаем основную сетку
    ax.grid(which='major', linewidth=1,  linestyle='-',  drawstyle='steps', alpha=0.4) 
        #  Устанавливаем интервал основных делений:
    ax.xaxis.set_major_locator(ticker.MultipleLocator(15)) 

        # Установка расстояния между таблицами
    plt.tight_layout(pad=0.4, w_pad=0.5, h_pad=1.0)      
    plt.subplots_adjust(wspace=0.6, hspace=0.35)
    plt.show()

        # Вывод графика как b64encode
    tmpfile = BytesIO()
    plt.savefig(tmpfile, format='png')
    encoded = base64.b64encode(tmpfile.getvalue()).decode('utf-8')
    print('''
    <div class="display_data">
    <div class="output_subarea output_image">
    <img src="data:image/png;base64,{}" class="unconstrained">
    </div>
    </div>'''.format(encoded))












         # SWAP диск. Чтение и запись блоков за 5 минут
    plt.style.use('default')
    p_ssd_read=np.array(п_ответ_разбор['arr_swap_read_block'])
    p_ssd_write=np.array(п_ответ_разбор['arr_swap_write_block'])

        # блок для отображения графиков
    fig, (ax_r, ax_w) = plt.subplots(nrows=1, ncols=2,  figsize=(19, 4.5), dpi=100, facecolor='#ABABAB', edgecolor='#727272', linewidth=10)
        # добавляем подписи к осям и заголовок диаграммы
    ax_r.set(title=r'$Блоков$ $считали$ $из$ $SWAP$ $SSD$ $диска$ $и$ $записали$ $в$ $RAM$')
    ax_r.set_xlabel(r' $Время$ ', fontsize=10)
    ax_r.set_ylabel(r' $блоков,$  $штук$ ', fontsize=12)  

    color = 'tab:red'
    ax_w.set(title=r'$Блоков$ $записали$ $из$ $RAM$ $на$ $SWAP$ $SSD$ $диск$')
    ax_w.set_xlabel(r' $Время$ ', fontsize=10)
    ax_w.set_ylabel(r' $блоков,$  $штук$ ', color=color, fontsize=5, visible=False)  

                    #get current axes
                #ax = plt.gca ()
                    #hide x-axis
                #ax.get_xaxis ().set_visible ( False )
                    #hide y-axis 
                #ax.get_yaxis ().set_visible ( False )
    ax_w.get_yaxis ().set_visible ( False )
    # ax2 = ax1.twinx()  # создаёт копию и сэтой копией можно делать независимые вещи на том же самом графике (две подписи к примеру)

    ax_w2 = ax_w.twinx()
    color = 'tab:blue'
    ax_w2.set_ylabel(r' $блоков,$  $штук$ ', color=color, fontsize=12)
    ax_w2.tick_params(axis='y', labelcolor=color)

        # сами графики        
    ax_r.step(p_x_время, p_ssd_read, label='Прочитано из SWAP в RAM блоков', color='#BABABA', linestyle='-') 
    ax_w.step(p_x_время, p_ssd_write, label='Записано из RAM в SWAP блоков', color='#BABABA', linestyle='-') 
        # выводим легенду
    ax_r.legend(loc='upper left', bbox_to_anchor=(0.01, 0.99), fontsize=9)
    ax_w.legend(loc='upper left', bbox_to_anchor=(0.01, 0.99), fontsize=9)
    #ax.set_yscale('log')
    
        # включаем основную сетку
    ax_r.grid(which='major', linewidth=1,  linestyle='-', drawstyle='steps', alpha=0.2) 
    ax_w.grid(which='major', linewidth=1,  linestyle='-', drawstyle='steps', alpha=0.2) 
        #  Устанавливаем интервал основных делений:
    ax_r.xaxis.set_major_locator(ticker.MultipleLocator(15)) 
    ax_w.xaxis.set_major_locator(ticker.MultipleLocator(15)) 
    ax_r.tick_params(axis='x', labelrotation=70) #ax_r.xticks(rotation=15)
    ax_w.tick_params(axis='x', labelrotation=70) 

        # Установка расстояния между таблицами
    plt.tight_layout(pad=0.60, w_pad=0.6, h_pad=0.7) # = поля до внешней оконтовки (до внешней рамки),  
    plt.subplots_adjust(wspace=0.06, hspace=0.0) #fig.subplots_adjust(right=0.85)     
                                #!!!! = поля между графиками (при 0, окна  накладываются! друг на друга)   hspace = между строк  wspace=между столбцов(по горизонтали)
    plt.show()

        # Вывод графика как b64encode
    tmpfile = BytesIO()
    plt.savefig(tmpfile, format='png')
    encoded = base64.b64encode(tmpfile.getvalue()).decode('utf-8')
    print('''
    <div class="display_data">
    <div class="output_subarea output_image">
    <img src="data:image/png;base64,{}" class="unconstrained">
    </div>
    </div>'''.format(encoded))











         # Очередь блоков для записи на диск и сколько сейчас блоков пишется на диск
    p_ssd_очередь=np.array(п_ответ_разбор['arr_ram_ssd_очередь'])
    p_ssd_write=np.array(п_ответ_разбор['arr_ram_ssd_запись'])

        # блок для отображения графиков
    fig, (ax_r, ax_w) = plt.subplots(nrows=1, ncols=2,  figsize=(19, 4.5), dpi=100, facecolor='#ABABAB', edgecolor='#727272', linewidth=10)
        # добавляем подписи к осям и заголовок диаграммы
    ax_r.set(title=r'$Блоков$ $ждёт$ $записи$ $на$ $SSD$ $диск$')
    ax_r.set_xlabel(r' $Время$ ', fontsize=10)
    ax_r.set_ylabel(r' $блоков,$  $штук$ ', fontsize=12)  

    color = 'tab:red'
    ax_w.set(title=r'$Блоков$ $сейчас$ $пишется$ $на$ $SSD$ $диск$')
    ax_w.set_xlabel(r' $Время$   В теории, мы НЕ должны видель значения на этом графике.', fontsize=10)
    ax_w.set_ylabel(r' $блоков,$  $штук$ ', color=color, fontsize=5, visible=False)  
                        #get current axes
                #ax = plt.gca ()
                    #hide x-axis
                #ax.get_xaxis ().set_visible ( False )
                    #hide y-axis 
                #ax.get_yaxis ().set_visible ( False )
    ax_w.get_yaxis ().set_visible ( False )
    # ax2 = ax1.twinx()  # создаёт копию и сэтой копией можно делать независимые вещи на том же самом графике (две подписи к примеру)

    ax_w2 = ax_w.twinx()
    color = 'tab:blue'
    ax_w2.set_ylabel(r' $блоков,$  $штук$ ', color=color, fontsize=12)
    ax_w2.tick_params(axis='y', labelcolor=color)

        # сами графики        
    ax_r.step(p_x_время, p_ssd_очередь, label='  Очереь на запись  ', color='#6C2DC7', linestyle='-', alpha=0.6) 
    ax_w.step(p_x_время, p_ssd_write, label='  В процессе записи  ', color='#C11B17', linestyle='-', alpha=0.6)  
        # выводим легенду
    ax_r.legend(loc='upper left', bbox_to_anchor=(0.00, 1.1), fontsize=9)
    ax_w.legend(loc='upper left', bbox_to_anchor=(0.001, 1.1), fontsize=9)
    ax_r.set_yscale('log')
    
        # включаем основную сетку
    ax_r.grid(which='major', linewidth=1,  linestyle='-', drawstyle='steps', alpha=0.2) 
    ax_w.grid(which='major', linewidth=1,  linestyle='-', drawstyle='steps', alpha=0.2) 
        #  Устанавливаем интервал основных делений:
    ax_r.xaxis.set_major_locator(ticker.MultipleLocator(15)) 
    ax_w.xaxis.set_major_locator(ticker.MultipleLocator(15)) 
    ax_r.tick_params(axis='x', labelrotation=70) #ax_r.xticks(rotation=15)
    ax_w.tick_params(axis='x', labelrotation=70) 


        # Установка расстояния между таблицами
    plt.tight_layout(pad=0.60, w_pad=0.6, h_pad=0.7) # = поля до внешней оконтовки (до внешней рамки),  
    plt.subplots_adjust(wspace=0.06, hspace=0.0) #fig.subplots_adjust(right=0.85)     
                                #!!!! = поля между графиками (при 0, окна  накладываются! друг на друга)   hspace = между строк  wspace=между столбцов(по горизонтали)
    plt.show()

        # Вывод графика как b64encode
    tmpfile = BytesIO()
    plt.savefig(tmpfile, format='png')
    encoded = base64.b64encode(tmpfile.getvalue()).decode('utf-8')
    print('''
    <div class="display_data">
    <div class="output_subarea output_image">
    <img src="data:image/png;base64,{}" class="unconstrained">
    </div>
    </div>'''.format(encoded))











        # Оперативная память. ДОСТУПНАЯ для использования
    plt.style.use('default')
    p_ram_min=np.array(п_ответ_разбор['arr_ram_доступно_min'])
    p_ram_max=np.array(п_ответ_разбор['arr_ram_доступно_max'])
    p_ram_midl=np.array(п_ответ_разбор['arr_ram_доступно_midle'])

        # блок для отображения графиков
    fig, ax = plt.subplots(1, 1, figsize=(19, 4), dpi=100, facecolor='#ABABAB', edgecolor='#727272', linewidth=10)
        # добавляем подписи к осям и заголовок диаграммы
    ax.set(title=r'Оперативная память. ДОСТУПНАЯ для использования')
    ax.set_xlabel(r'$Время$     Эта память НЕ равна "полностью свободной". Если не чистить КЭШ память, то отличия будут очень сильными (до 2-х раз)', fontsize=10)
    ax.set_ylabel(r'$Проценты$', fontsize=12)    
        # сами графики
    ax.fill_between(p_x_время, p_ram_min, p_ram_max, color='#C38EC7', label='Дельта MAX-MIN', alpha=0.2 ) # where=(y < 0)           
    ax.plot(p_x_время, p_ram_max, ':b',  label='максимум',  linewidth=1, alpha=0.9 )   # п_ответ_разбор['arr_cpu_max']
    ax.plot(p_x_время, p_ram_min, '--k', label='минимум',  linewidth=1) # visible=False
    ax.plot(p_x_время, p_ram_midl, color='#E4287C', label='математ.средняя', linewidth=1)
    ax.set_ylim([9, 83]) # Границы по оси У
        # выводим легенду
    ax.legend(loc='upper left', bbox_to_anchor=(0.0, 0.31), fontsize=9)     #'upper left', bbox_to_anchor=(0.5, 0.5)  'upper right'   'lower right'  
    plt.tight_layout(pad=1.0, w_pad=1.0, h_pad=1.0)
    #plt.tight_layout(rect=[None, None, 0.45, None])
        # включаем основную сетку
    ax.grid(which='major', linewidth=1,  linestyle='-', drawstyle='steps', alpha=0.2) # {'default', 'steps', 'steps-pre', 'steps-mid', 'steps-post'}, default: 'default'
        #  Устанавливаем интервал основных делений:
    ax.xaxis.set_major_locator(ticker.MultipleLocator(15))
        # Установка расстояния между таблицами
    plt.subplots_adjust(wspace=0, hspace=0.35)
    plt.show()

        # Вывод графика как b64encode
    tmpfile = BytesIO()
    plt.savefig(tmpfile, format='png')
    encoded = base64.b64encode(tmpfile.getvalue()).decode('utf-8')
    print('''
    <div class="display_data">
    <div class="output_subarea output_image">
    <img src="data:image/png;base64,{}" class="unconstrained">
    </div>
    </div>'''.format(encoded))















        # Оперативная память. Занятые КЭШ и БУФЕР оперативной памятью
    plt.style.use('default')
    p_ram_buf_min=np.array(п_ответ_разбор['arr_ram_buf_min'])
    p_ram_buf_max=np.array(п_ответ_разбор['arr_ram_buf_max'])
    p_ram_buf_midl=np.array(п_ответ_разбор['arr_ram_buf_midle'])
    p_ram_cach_min=np.array(п_ответ_разбор['arr_ram_cach_min'])
    p_ram_cach_max=np.array(п_ответ_разбор['arr_ram_cach_max'])
    p_ram_cach_midl=np.array(п_ответ_разбор['arr_ram_cach_midle'])

        # блок для отображения графиков
    fig, ax = plt.subplots(1, 1, figsize=(19, 4), dpi=100, facecolor='#ABABAB', edgecolor='#727272', linewidth=10)
        # добавляем подписи к осям и заголовок диаграммы
    ax.set(title=r'Оперативная память. Отведённая под КЭШ и под БУФЕРЫ')
    ax.set_xlabel(r'$Время$   Максимум RAM памяти пож КЭШ равен 8 GB или 50% от всей RAM памяти', fontsize=10)
    ax.set_ylabel(r'$Проценты$ $от$ $размера$ $всей$ $RAM$', fontsize=12)    
        # сами графики
    ax.plot(p_x_время, p_ram_buf_midl, color='#A23BEC', label='RAM BUFFER математ.средняя', linewidth=1)       
    ax.fill_between(p_x_время, p_ram_buf_min, p_ram_buf_max, color='#9E7BFF', label='RAM BUFFER Дельта MAX-MIN', alpha=0.4 ) 
    ax.plot(p_x_время, p_ram_cach_midl, color='#3EA055', label='RAM CACHE математ.средняя', linewidth=1)    
    ax.fill_between(p_x_время, p_ram_cach_min, p_ram_cach_max, color='#64E986', label='RAM CACHE Дельта MAX-MIN', alpha=0.4 )    
    ax.set_ylim([-1, 83]) # Границы по оси У

        # выводим легенду
    ax.legend(loc='upper left', bbox_to_anchor=(0.0, 1.0), fontsize=9)     #'upper left', bbox_to_anchor=(0.5, 0.5)  'upper right'   'lower right'  
    plt.tight_layout(pad=1.0, w_pad=1.0, h_pad=1.0)
    # plt.tight_layout(rect=[0.01, 0.01, 0.98, 0.98]) #None
        # включаем основную сетку
    ax.grid(which='major', linewidth=1,  linestyle='-', drawstyle='steps', alpha=0.2) 
        #  Устанавливаем интервал основных делений:
    ax.xaxis.set_major_locator(ticker.MultipleLocator(15))
        # Установка расстояния между таблицами
    plt.subplots_adjust(wspace=0, hspace=0.35)
    plt.show()

        # Вывод графика как b64encode
    tmpfile = BytesIO()
    plt.savefig(tmpfile, format='png')
    encoded = base64.b64encode(tmpfile.getvalue()).decode('utf-8')
    print('''
    <div class="display_data">
    <div class="output_subarea output_image">
    <img src="data:image/png;base64,{}" class="unconstrained">
    </div>
    </div>'''.format(encoded))










# ============ КОНЕЦ Вывод списка =======================================


print ('&nbsp;  &nbsp;<br>')


# *******************************************************************************
# *******************************************************************************
# *******************************************************************************

# Генерируем виджет сайта


# Генерируем footer сайта (подвал сайта)


# делаем замену виджета сайта и подвала сайта и выводим результат

низ_страницы="" #site_body_bottom(widget=правый_виджет, site_footer=footer)
print(низ_страницы)

# sys.exit()

      

