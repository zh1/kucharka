/*
select
		*
from
	kucharka.dbo.recept
where
	zdroj_id = 53050
;

select * from kucharka.dbo.recept_surovina where recept_id in (10925, 10975, 11000, 11100, 11125);

*/

with dups as
	(
	select
		zdroj_id,
		count(1) as cnt
	from
		kucharka.dbo.recept
	group by
			zdroj_id
	having
			count(1) > 1
	),
	recept_id_dups as (
	select 
			row_number() over (partition by r.zdroj_id order by r.stahovani_id) as rn,
			r.*
	from
		kucharka.dbo.recept r
	inner join
		dups d
		on (r.zdroj_id = d.zdroj_id)
	)
select
		id
into kucharka.dbo.remove_dups
from
	recept_id_dups
where
	rn > 1
;

delete from kucharka.dbo.komentar where recept_id in (select id from kucharka.dbo.remove_dups);
delete from kucharka.dbo.postup where recept_id in (select id from kucharka.dbo.remove_dups);
delete from kucharka.dbo.recept_kategorie where recept_id in (select id from kucharka.dbo.remove_dups);
delete from kucharka.dbo.recept_nutricni_hodnota where recept_id in (select id from kucharka.dbo.remove_dups);
delete from kucharka.dbo.recept_surovina where recept_id in (select id from kucharka.dbo.remove_dups);

delete from kucharka.dbo.recept where id in (select id from kucharka.dbo.remove_dups);

drop table kucharka.dbo.remove_dups;