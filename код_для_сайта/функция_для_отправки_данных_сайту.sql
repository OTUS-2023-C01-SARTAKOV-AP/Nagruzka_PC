CREATE OR REPLACE FUNCTION site_html."f_отчет_нагрузка_пк"(in_json json, OUT out_json json)
 RETURNS json
 LANGUAGE plpgsql
AS $function$
declare 
-- функция выводит на сайт нагрузки ПК за указанный диапазон дат
--  select site_html.f_отчет_нагрузка_пк('{"дата_старт":"2023-11-07", "дата_конец":"2023-11-07" }'::json)

п_запрос_1 text;
п_jsonb jsonb;
п_jsonb_all jsonb;


p_stack text;
p_integer numeric;
p_func_name text;
p_sql_state text;
p_column_name text;
p_constraint_name text;
p_pg_datatype_name text;
p_message_text text;
p_table_name text;
p_schema_name text;
p_exception_detail text;
p_pr_exception_hint text;
p_pg_exception_context text;
p_sqlstate text;
p_current_database text;
p_zapros text :=current_query();
p_current_role text;
p_pg_backend_pid text;
p_pg_trigger_depth text;
p_session_user text;
p_out_jsonb_text jsonb;


p_start_time timestamp :=clock_timestamp();

begin

	/*
п_jsonb_all:=jsonb_build_object('ответ', 'ошибка', 'расшифровка_ответа', 'Не хватает прав для выполнения запроса или для просмотра страницы (данных).'); 	-- успешно   ошибка	

-- **************** проверяем права у пользователей (в запросах) для работы с БД ***********************
	-- по умолчанию роль = только чтение!!!!
set local role 'user_only_read';  

if (select имя_роли_вбд from пользователи.права_доступа  where id_уровня = (in_json ->> 'id_роли_в_бд')::integer) = 'user_unlogged'
then 
	out_json = п_jsonb_all;
	return;
end if;


	-- если в ключах есть 'id_роли_в_бд' то проверяем эту роль на права и переназначаем права!
if 'id_роли_в_бд' in (select json_object_keys(in_json))
then
	п_запрос_1 := 'set local role '||(select имя_роли_вбд from пользователи.права_доступа  where id_уровня = (in_json ->> 'id_роли_в_бд')::integer);
	execute п_запрос_1;
end if;
--raise notice '% %', (select current_user), (select session_user);
-- **************** проверяем права у пользователей (в запросах) для работы с БД ***********************
*/
	
п_jsonb_all:=jsonb_build_object('ответ', 'успешно', 'расшифровка_ответа', ''); 	-- успешно   ошибка





with t0 as (
	select cpu_min, cpu_max, cpu_midle, 
	ram_used_min, ram_used_max, ram_used_midle, 
	swap_read_block, swap_write_block, 
	cpu_t_min, cpu_t_max, cpu_t_midle, 
	ssd_read_block, ssd_write_block, 
	время, 
	ram_full_free, ram_доступно_min, ram_доступно_max, ram_доступно_midle,
	ram_buf_min, ram_buf_max, ram_buf_midle,
	ram_cach_min, ram_cach_max, ram_cach_midle,
	ram_ssd_очередь, ram_ssd_запись,
	ram_user_min, ram_user_max, ram_user_midle
	from db_log.нагрузка_системы 
	where время::date  >= (in_json->>'дата_старт')::date  
	and время::date <= (in_json->>'дата_конец')::date  
	order by время asc  
),
t1 as (
	select array_agg(cpu_min order by время asc) as arr_cpu_min,
	array_agg(cpu_max order by время asc) as arr_cpu_max,
	array_agg(cpu_midle order by время asc) as arr_cpu_midle, 
	array_agg(ram_used_min order by время asc) as arr_ram_used_min, 
	array_agg(ram_used_max order by время asc) as arr_ram_used_max, 
	array_agg(ram_used_midle order by время asc) as arr_ram_used_midle, 
	array_agg(swap_read_block order by время asc) as arr_swap_read_block,  
	array_agg(swap_write_block order by время asc) as arr_swap_write_block, 
	array_agg(cpu_t_min order by время asc) as arr_cpu_t_min, 
	array_agg(cpu_t_max order by время asc) as arr_cpu_t_max,
	array_agg(cpu_t_midle order by время asc) as arr_cpu_t_midle,
	array_agg(ssd_read_block order by время asc) as arr_ssd_read_block,
	array_agg(ssd_write_block order by время asc) as arr_ssd_write_block,
	array_agg(время::time order by время asc) as arr_время,
	array_agg(ram_full_free order by время asc) as arr_ram_full_free,
	array_agg(ram_доступно_min order by время asc) as arr_ram_доступно_min,
	array_agg(ram_доступно_max order by время asc) as arr_ram_доступно_max,
	array_agg(ram_доступно_midle order by время asc) as arr_ram_доступно_midle,
	array_agg(ram_buf_min order by время asc) as arr_ram_buf_min,
	array_agg(ram_buf_max order by время asc) as arr_ram_buf_max,
	array_agg(ram_buf_midle order by время asc) as arr_ram_buf_midle,
	array_agg(ram_cach_min order by время asc) as arr_ram_cach_min,
	array_agg(ram_cach_max order by время asc) as arr_ram_cach_max,
	array_agg(ram_cach_midle order by время asc) as arr_ram_cach_midle, 
	array_agg(ram_ssd_очередь order by время asc) as arr_ram_ssd_очередь,
	array_agg(ram_ssd_запись order by время asc) as arr_ram_ssd_запись,
	
	array_agg(ram_user_min order by время asc) as arr_ram_user_min,
	array_agg(ram_user_max order by время asc) as arr_ram_user_max,
	array_agg(ram_user_midle order by время asc) as arr_ram_user_midle
	from t0
)
select jsonb_build_object('расшифровка_ответа', jsonb_build_object(
	'arr_cpu_min', arr_cpu_min,
	'arr_cpu_max', arr_cpu_max,
	'arr_cpu_midle', arr_cpu_midle,
	
	'arr_ram_used_min', arr_ram_used_min,
	'arr_ram_used_max', arr_ram_used_max,
	'arr_ram_used_midle', arr_ram_used_midle, 
	
	'arr_swap_read_block', arr_swap_read_block, 
	'arr_swap_write_block', arr_swap_write_block,
	
	'arr_cpu_t_min', arr_cpu_t_min, 
	'arr_cpu_t_max', arr_cpu_t_max, 
	'arr_cpu_t_midle', arr_cpu_t_midle, 
	
	'arr_ssd_read_block', arr_ssd_read_block, 
	'arr_ssd_write_block', arr_ssd_write_block, 
	
	'arr_время', arr_время, 
	'arr_ram_full_free', arr_ram_full_free, 
	
	'arr_ram_доступно_min', arr_ram_доступно_min, 
	'arr_ram_доступно_max', arr_ram_доступно_max, 
	'arr_ram_доступно_midle', arr_ram_доступно_midle, 
	
	'arr_ram_buf_min', arr_ram_buf_min, 
	'arr_ram_buf_max', arr_ram_buf_max, 
	'arr_ram_buf_midle', arr_ram_buf_midle, 
	
	'arr_ram_cach_min', arr_ram_cach_min, 
	'arr_ram_cach_max', arr_ram_cach_max, 
	'arr_ram_cach_midle', arr_ram_cach_midle, 
	
	'arr_ram_ssd_очередь', arr_ram_ssd_очередь, 
	'arr_ram_ssd_запись', arr_ram_ssd_запись, 
	
	'arr_ram_user_min', arr_ram_user_min, 
	'arr_ram_user_max', arr_ram_user_max, 
	'arr_ram_user_midle', arr_ram_user_midle 	)
	) from t1 into п_jsonb;
			

out_json:=п_jsonb_all||п_jsonb;
	
return;




-- вставляем код ниже в самый конец ПОСЛЕ "return;"  но перед "END;" 
EXCEPTION WHEN OTHERS then
	p_out_jsonb_text:=jsonb_build_object('_операция', 'ошибка');

	GET STACKED diagnostics 
	p_sql_state:=RETURNED_SQLSTATE,
	p_column_name:=COLUMN_NAME, 
	p_constraint_name:=CONSTRAINT_NAME,
	p_pg_datatype_name:=PG_DATATYPE_NAME,
	p_message_text:=MESSAGE_TEXT,
	p_table_name:=TABLE_NAME,
	p_schema_name:=SCHEMA_NAME,
	p_exception_detail:=PG_EXCEPTION_DETAIL,
	p_pr_exception_hint:=PG_EXCEPTION_HINT,
	p_pg_exception_context:=PG_EXCEPTION_CONTEXT;

	p_sqlstate:=sqlstate;
	p_current_database:=current_database();
	p_zapros:=current_query();
	p_current_role:=(select current_role);
	p_pg_backend_pid:=(select pg_backend_pid());
	p_pg_trigger_depth :=	pg_trigger_depth ();
	p_session_user:=session_user;

	GET DIAGNOSTICS p_func_name = PG_CONTEXT;

	p_out_jsonb_text:=p_out_jsonb_text||jsonb_build_object('p_sql_state', coalesce(p_sql_state, '-') )||
	jsonb_build_object('p_column_name', coalesce(p_column_name, '-') )||
	jsonb_build_object('p_constraint_name', coalesce(p_constraint_name, '-') )||
	jsonb_build_object('p_pg_datatype_name', coalesce(p_pg_datatype_name, '-') )||
	jsonb_build_object('p_message_text', coalesce(p_message_text, '-') )||
	jsonb_build_object('p_table_name', coalesce(p_table_name, '-') )||
	jsonb_build_object('p_schema_name', coalesce(p_schema_name, '-') )||
	jsonb_build_object('p_exception_detail', coalesce(p_exception_detail, '-') )||
	jsonb_build_object('p_pg_exception_context', coalesce(p_pg_exception_context, '-') )||
	jsonb_build_object('Код ошибки PostgreSQL', coalesce(p_sqlstate, '-') )||
	jsonb_build_object('База Данных', coalesce(p_current_database, '-') )||
	jsonb_build_object('Запрос', coalesce(p_zapros, '-') )||
	jsonb_build_object('Роль', coalesce(p_current_role, '-') )|| 
	jsonb_build_object('Номер сервенного процесса', coalesce(p_pg_backend_pid, '-') )||
	jsonb_build_object('вложенности в триггерах', coalesce(p_pg_trigger_depth, '-') )||
	jsonb_build_object('имя пользователя сеанса', coalesce(p_session_user, '-') )||
	jsonb_build_object('код по вызову вложенной функции', coalesce(p_func_name, '-') )||
	jsonb_build_object('продолжительность выполнения', coalesce((clock_timestamp()-p_start_time)::text, '-') );
	
	raise notice 'Возникла ошибка при работе функции (site_html.f_отчет_нагрузка_пк). См отчет в <db_log.t_log_ошибки_вфункциях>';
	perform db_log.z_log_db_func(array['ошибка', p_out_jsonb_text::text]);

	out_json:=jsonb_build_object('ответ', 'ошибка', 'расшифровка_ответа', (p_out_jsonb_text-'имя пользователя сеанса')-'Роль' ); 
			--(select сообщение from site_html.t_сообщения_для_сайта where id=20));
	return ;
	
end;
$function$
;

-- Permissions

ALTER FUNCTION site_html.f_отчет_нагрузка_пк(in json, out json) OWNER TO postgres;
GRANT ALL ON FUNCTION site_html.f_отчет_нагрузка_пк(in json, out json) TO public;
GRANT ALL ON FUNCTION site_html.f_отчет_нагрузка_пк(in json, out json) TO postgres;