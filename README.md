# techcrunchsmallbite

Visual inspection of TechCrunch articles found the desired information tended to be in a Crunchbase tile.
As such, it may break if TechCrunch changes its web page design.

A more general approach could use NLP to determine primary subjects of each article, and then compare those
against a repository of company data. There is a Crunchbase API, for example.

I'm told just pulling recent articles is sufficient for this purpose, so RSS feeds were suitable.
If one wanted every article, a web spider should work, though appropriate validation to ensure the
links followed were TechCrunch articles and not other sorts of content would be needed in conjunction.

If the program requirements continued to grow, one would split out functions into separate modules
as appropriate (web io, processing, data storage, etc), though not necessary at the current level of complexity.
