

insheet using data_output.csv, comma clear names
rename player playername
gen date = date(birthdate, "MDY")
drop birthdate
rename date birthdate
keep if birthdate != .
format birthdate %td
save birthdates, replace

insheet using data_boxscores_basic.csv, comma clear names
drop if playername == "Shawn Marion" & date == "2007-12-19"
save data_boxscores_basic, replace

insheet using data_boxscores_adv.csv, comma clear names
drop if playername == "Shawn Marion" & date == "2007-12-19"

merge 1:1 playername date using data_boxscores_basic

keep if _merge == 3
drop _merge

joinby playername using birthdates

destring tspct efgpct orb drb trbpct ast stl blkpct tov usgpct ortg drtg gamescore fg fga fgpct threepoint threepointatt threepointpct ft fta ftpct trb blk pf pts, replace force

gen date2 = date(date, "YMD")
format date2 %td

gen t = date2 - birthdate
gen t_sq = (date2 - birthdate)^2
gen t_cube = (date2 - birthdate)^3
gen t_quad = (date2 - birthdate)^4

egen birthid = group(playername birthdate)

gen season = year(date2)
replace season = season - 1 if month(date2) < 6

gen week = wofd(date2)
gen birthweek = wofd(birthdate)

gen tw = week - birthweek
gen tw_sq = tw^2

gen birthseason = year(birthdate)
replace birthseason = birthseason - 1 if month(birthdate) < 5

gen inseason = month(birthdate) > 10 | month(birthdate) < 5

gen days_from_begin = date2 - mdy(10,26, season)
gen days_from_end = mdy(5,5, season+1) - date2

gen dfb = days_from_begin / 191
gen dfe = days_from_end / 191

gen inplay = tw == 0

egen hasdata = max(inplay), by(birthid)

gen birth = t >= 0

split result, p(" ")

gen win = result1 == "W"

gen diff = subinstr(result2, "(", "", .)
replace diff = subinstr(diff, ")", "", .)
replace diff = subinstr(diff, "+", "", .)
destring diff, replace
egen playerid = group(playername)

gen pm = subinstr(plusminus, "+", "", .)
destring pm, replace force

