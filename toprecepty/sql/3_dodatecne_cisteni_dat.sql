update kucharka.dbo.recept_nutricni_hodnota
	set mnozstvi = cast(replace(replace(mnozstvi, ' ', ''), ',', '.') as float)
;

delete from kucharka.dbo.recept_surovina where mnozstvi = '';