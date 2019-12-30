<html>
    <head>
        <link href='/static/style.css' rel='stylesheet' type='text/css'>
        <title>{{title or 'No title'}}</title>
    </head>
    <body>
        <div class="mainDiv">

            {{!base}}

            <br />
            <div class="indexDiv">
            %for r in index:
                <a class="indexLink" href={{r.path}}>{{r.name}}</a>
                <br/>
            %end
            </div>
        </div>
    </body>
</html> 
