use top_recepty

select *
from
	recipe

select
		cast(column1 as bigint) as id,
		cast(recipe_source_id as varchar) as source_id,
		trim(cast(recipe_name as varchar)) as name,
		cast(replace(recipe_stars, ',', '.') as float) as rating,
		replace(replace(recipe_rating_cnt, '×)', ''), '(', '') as rating_cnt,
		trim(recipe_time) as recipe_time,
		--case when recipe_created = 'pred 20 hodinami'
		--	then dateadd(hour, -20, current_timestamp)
		--	else format(cast(recipe_created as varchar), 'dd. mm. yyyy hh24:mi')
		--end as created,
		cast(left(recipe_comment_cnt, charindex(' ', recipe_comment_cnt) -1) as int) as comment_cnt,
		cast(serve_cnt as int) as serve_cnt,
		cast(serve_unit as varchar) as serve_unit,
		cast(sections as varchar) as sections,
		cast(recipe_link as varchar) as url,
		cast(recipe_image as varchar) as image_url,
		cast(ingredient_nutrition_url as varchar) as ingredient_nutrition_url
from
	recipe