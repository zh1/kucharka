/* drop all tables in database */
if object_id(N'kucharka.dbo.recept_kategorie', N'U') is not null  
   drop table kucharka.dbo.recept_kategorie;
if object_id(N'kucharka.dbo.recept_nutricni_hodnota', N'U') is not null  
   drop table kucharka.dbo.recept_nutricni_hodnota;
if object_id(N'kucharka.dbo.recept_surovina', N'U') is not null  
   drop table kucharka.dbo.recept_surovina;
if object_id(N'kucharka.dbo.kategorie', N'U') is not null  
   drop table kucharka.dbo.kategorie;
if object_id(N'kucharka.dbo.nutricni_hodnota', N'U') is not null  
   drop table kucharka.dbo.nutricni_hodnota;
if object_id(N'kucharka.dbo.postup', N'U') is not null  
   drop table kucharka.dbo.postup;
if object_id(N'kucharka.dbo.komentar', N'U') is not null  
   drop table kucharka.dbo.komentar;
if object_id(N'kucharka.dbo.surovina', N'U') is not null  
   drop table kucharka.dbo.surovina;
if object_id(N'kucharka.dbo.recept', N'U') is not null  
   drop table kucharka.dbo.recept;

/* dbo.recept */
select
	convert(bigint, id) as id,
	cast(recipe_source_id as bigint) as zdroj_id,
	cast(recipe_name as nvarchar) as nazev,
	cast(recipe_link as ntext ) as url,
	cast(recipe_image as ntext) as url_obrazku,
	cast(recipe_batch_id as bigint) as stahovani_id,
	cast(replace(recipe_stars, ',', '.') as float) as hodnoceni,
	cast(REPLACE(SUBSTRING(recipe_rating_cnt, 2, 1), 'x', '0') as int) AS pocet_hodnoceni,
	cast(recipe_author as varchar) as autor,
	case when recipe_created like N'před%' then current_timestamp else TRY_CONVERT(datetime, recipe_created, 104) end as vytvoreno,
	cast(LEFT(recipe_comment_cnt, CHARINDEX(' ', recipe_comment_cnt) - 1) AS int) as pocet_komentaru,	
	try_cast(replace(left(trim(replace(replace(recipe_time, char(9), ''), char(10), '')), charindex('(', trim(replace(replace(recipe_time, char(9), ''), char(10), '')))), ' min (', '') as bigint) as celkovy_doba_pripravy,
	replace(right(trim(replace(replace(recipe_time, char(9), ''), char(10), '')), len(trim(replace(replace(recipe_time, char(9), ''), char(10), ''))) - charindex('(', trim(replace(replace(recipe_time, char(9), ''), char(10), '')))), ')', '') as detail_doby_pripravy,
	cast(serve_cnt as float) as pocet_porci,
	cast(serve_unit as nvarchar) as jednotky_porci,
	sections as sekce_receptu,
	cast(replace(replace(replace(replace(replace(replace(favourites_cnt, char(9), ''), char(10), ''), N'Přidat do oblíbených', ''), '(', ''), 'x)', ''), char(160), '') as int) as pocet_oblibenych,
	cast(ingredient_nutrition_url as varchar) as url_detail_receptu
into kucharka.dbo.recept
from
	top_recepty.dbo.recipe
;

alter table kucharka.dbo.recept alter column id bigint not null;
alter table kucharka.dbo.recept add primary key (id);

/* dbo.kategorie */
select
		row_number() over (order by name) as id,
		replace(name, char(160), '') as nazev,
		cast(main_category_ind as bit) as indikator_hlavni_kategorie
into kucharka.dbo.kategorie
from
	top_recepty.dbo.tag
group by 
		name,
		cast(main_category_ind as bit)
;

alter table kucharka.dbo.kategorie alter column id bigint not null;
alter table kucharka.dbo.kategorie add primary key (id);

/* dbo.recept_kategorie */
select
		row_number() over (order by t.name) as id,
		cast(r.id as bigint) as recept_id,
		cast(k.id as bigint) as kategorie_id
into kucharka.dbo.recept_kategorie
from
	top_recepty.dbo.tag t
left outer join
	kucharka.dbo.recept r
	on (t.recipe_id = r.id)
left outer join
	kucharka.dbo.kategorie k
	on (t.name = k.nazev)
;

alter table kucharka.dbo.recept_kategorie alter column id bigint not null;
alter table kucharka.dbo.recept_kategorie add primary key (id);

/* dbo.postup */
select
		row_number() over (order by name) as id,
		cast(recipe_id as bigint) as recept_id,
		replace(replace(name, char(9), ''), char(10), '') as popis,
		cast([order] as int) as krok
into kucharka.dbo.postup
from
	top_recepty.dbo.step
;

alter table kucharka.dbo.postup alter column id bigint not null;
alter table kucharka.dbo.postup add primary key (id);

/* dbo.surovina */
select
		row_number() over (order by name) as id,
		replace(name, char(160), '') as nazev
into kucharka.dbo.surovina
from
	top_recepty.dbo.ingredient
where
	name is not null
group by 
		name
;

alter table kucharka.dbo.surovina alter column id bigint not null;
alter table kucharka.dbo.surovina add primary key (id);

/* dbo.recept_surovina */
select
		row_number() over (order by i.name) as id,
		cast(r.id as bigint) as recept_id,
		cast(s.id as bigint) as surovina_id,
		amount as mnozstvi
into kucharka.dbo.recept_surovina
from
	top_recepty.dbo.ingredient i
left outer join
	kucharka.dbo.recept r
	on (i.recipe_id = r.id)
left outer join
	kucharka.dbo.surovina s
	on (i.name = s.nazev)
where
	name is not null
;

alter table kucharka.dbo.recept_surovina alter column id bigint not null;
alter table kucharka.dbo.recept_surovina add primary key (id);

/* dbo.nutricni_hodnota */
select
		row_number() over (order by name) as id,
		name as nazev
into kucharka.dbo.nutricni_hodnota
from
	top_recepty.dbo.nutrition
group by
		name
;

alter table kucharka.dbo.nutricni_hodnota alter column id bigint not null;
alter table kucharka.dbo.nutricni_hodnota add primary key (id);

/* dbo.recept_nutricni_hodnota */
select
		row_number() over (order by n.name) as id,
		cast(r.id as bigint) as recept_id,
		cast(nh.id as bigint) as nutricni_hodnota_id,
		value as mnozstvi,
		unit as mnozstvi_jednotky
into kucharka.dbo.recept_nutricni_hodnota
from
	top_recepty.dbo.nutrition n
left outer join
	kucharka.dbo.recept r
	on (n.recipe_id = r.id)
left outer join
	kucharka.dbo.nutricni_hodnota nh
	on (n.name = nh.nazev)
;

alter table kucharka.dbo.recept_nutricni_hodnota alter column id bigint not null;
alter table kucharka.dbo.recept_nutricni_hodnota add primary key (id);

/* dbo.komentar */
select
		row_number() over (order by recipe_id, date, text, author) as id,
		cast(recipe_id as bigint) as recept_id,
		case when [date] like N'před%' then current_timestamp else TRY_CONVERT(datetime, [date], 104) end as datum,
		text,
		author as autor
into kucharka.dbo.komentar
from
	top_recepty.dbo.comment
;

alter table kucharka.dbo.komentar alter column id bigint not null;
alter table kucharka.dbo.komentar add primary key (id);

/* Foreign keys */

alter table kucharka.dbo.komentar
   add constraint fk_recept_komentar foreign key (recept_id)
      references kucharka.dbo.recept (id)
;

alter table kucharka.dbo.postup
   add constraint fk_recept_postup foreign key (recept_id)
      references kucharka.dbo.recept (id)
;

alter table kucharka.dbo.recept_kategorie
   add constraint fk_recept_recept_kategorie foreign key (recept_id)
      references kucharka.dbo.recept (id)
;

alter table kucharka.dbo.recept_kategorie
   add constraint fk_kategorie_recept_kategorie foreign key (kategorie_id)
      references kucharka.dbo.kategorie (id)
;

alter table kucharka.dbo.recept_nutricni_hodnota
   add constraint fk_recept_recept_nutricni_hodnota foreign key (recept_id)
      references kucharka.dbo.recept (id)
;

alter table kucharka.dbo.recept_nutricni_hodnota
   add constraint fk_nutricni_hodnota_recept_nutricni_hodnota foreign key (nutricni_hodnota_id)
      references kucharka.dbo.nutricni_hodnota (id)
;

alter table kucharka.dbo.recept_surovina
   add constraint fk_recept_recept_surovina foreign key (recept_id)
      references kucharka.dbo.recept (id)
;

alter table kucharka.dbo.recept_surovina
   add constraint fk_surovina_recept_surovina foreign key (surovina_id)
      references kucharka.dbo.surovina (id)
;
