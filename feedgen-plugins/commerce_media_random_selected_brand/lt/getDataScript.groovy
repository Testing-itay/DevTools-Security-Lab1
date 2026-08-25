// Feed generator data script (fixture)
def brands = sql.rows('SELECT brand_id FROM brands WHERE active = 1')
return brands.collect { it.brand_id }
