ZIM - Charite Wiki Generator
Summary
	Generate ZIM-Wiki-Database from Lernziele XLS, automatically using sane directory structure and adding relevant text

XLS-File Structure
	The lernziele xls file is retrieved from the charite website by the user. The workbook contains a single sheet of information regarding the relevant module and the event of the Lernziel. Some additional information is also available, but they are of no further concern at the moment.
	Header names are as follows (example):
		0-Modul (M5)
		1-akad. Periode (SoSe 2015)
		2-Woche
		3-Veranstaltung: Titel
		4-LZ-Dimension
		5-LZ-Kognitionsdimension
		6-Lernziel
		7-MC
		8-SMPP
		9-OSCE
	Interesting for Wiki-Building are:
		0-Modul
		2-Woche
		3-Veranstaltung: Titel
		6-Lernziel
		7-MC
		8-SMPP

ZIM-Wiki Structure
	Use zim 0.4 wiki structure

Importer Structure
	Information gathered in dictionary with following key
	Modul+Woche+Titelindex (eg M1W2Vorlesung 1) in 3d dict
	to the following list
		0 - Modul
		1 - Woche
		2 - Veranstaltungsindex
		3 - Veranstaltungstitel
		4 - Lernziel
		5 - MC
		6 - SMPP
	The strDict is a structure containing the necessary strings to build the Zim-Document data.
	the index version is:
		title - Page title
		subtitles - list of subtitles and list of index subpoints - the subpoints contain link to file and the title to be displayed
		the indexpoint function expects input as path and following name
	the event version is:
		title - Page title
		lernziele - list of lernziele to be put in bullet point list

New Structure for Semester 5
The lernziel file has gotten a lot simpler. We only have:
Modul - Period - Week - Event - LZ Dimension - Cognition - Lernziel
of which we need
Modul - Week - Event - Dimension - Lernziel
NOW even more awesome with classes (somehow)
