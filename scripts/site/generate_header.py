def get_header():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width">
    <title>Arktracker.info</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta1/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-giJF6kkoqNQ00vy+HMDP7azOuL0xtbfIcaT9wjKHr8RbDVddVHyTfAAsrekwKmP1" crossorigin="anonymous">
    </head>
    <body>
    <nav class="navbar navbar-expand-md navbar-light bg-light">
        <div class="container-fluid">
        <a class="navbar-brand" href="#">Arktracker.info</a>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNavAltMarkup" aria-controls="navbarNavAltMarkup" aria-expanded="false" aria-label="Toggle navigation">
            <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarNavAltMarkup">
            <div class="navbar-nav me-auto">
            <a class="nav-link" href="#">ETFs:</a>
            <a class="nav-link" aria-current="page" active href="./arkk.html">ARKK</a>
            <a class="nav-link" href="./arkf.html">ARKF</a>
            <a class="nav-link" href="./arkg.html">ARKG</a>
            <a class="nav-link" href="./arkq.html">ARKQ</a>
            <a class="nav-link" href="./arkw.html">ARKW</a>
            <a class="nav-link" href="./izrl.html">IZRL</a>
            <a class="nav-link" href="./prnt.html">PRNT</a>
            </div>
            <div class="navbar-nav">
            <a class="nav-link" id="privacy" href="#">Privacy</a>
            <a class="nav-link" href="https://github.com/ochsec/arktracker" target="_blank"><i class="fa fa-github" aria-hidden="true"></i> Github</a>
            </div>
        </div>    
        </div>
    </nav>
    """