#RSS reader
 
##Command-line utility which receives RSS URL and prints results in human-readable format.

###Usage example: 
[python](https://www.python.org/) rss_reader.py [example_sourse](https://news.yahoo.com/rss/) [-h] [--version] [--json] [--verbose] [--limit LIMIT]
                     
positional arguments:
  source         RSS URL

optional arguments:

**-h**, **--help**     show this help message and exit

**--version**          Print version info

**--json**             Print result as JSON in stdout

**--verbose**          Outputs verbose status messages

**--limit LIMIT**      Limit news topics if this parameter provided

**--date DATE**      Takes a date in %Y%m%d format. The cashed news from the specified day will be printed out

###JSON output structure example:

<pre><code>{
    some_feed: {
        'Title': some_title,
        'Publication Date': some_date,
        'Link': some_link,
        'Content': [
            some_content
        ]
        'Source': some_source,
        'Images': some_images
    }
}
</code></pre>
