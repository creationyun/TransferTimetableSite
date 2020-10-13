import os
replace_target = """<link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css" integrity="sha384-Vkoo8x4CGsO3+Hhxv8T/Q5PaXtkKtu6ug5TOeNV6gBiFeWPGFN9MuhOf23Q9Ifjh" crossorigin="anonymous">
<script src="https://code.jquery.com/jquery-3.4.1.slim.min.js" integrity="sha384-J6qa4849blE2+poT4WnyKhv5vZF5SrPo0iEjwBvKU7imGFAV0wwj1yYfoRSJoZ+n" crossorigin="anonymous"></script>
<script src="https://cdn.jsdelivr.net/npm/popper.js@1.16.0/dist/umd/popper.min.js" integrity="sha384-Q6E9RHvbIyZFJoft+2mJbHaEWldlvI9IOYy5n3zV9zzTtmI3UksdQRVvoxMfooAo" crossorigin="anonymous"></script>
<script src="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/js/bootstrap.min.js" integrity="sha384-wfSDF2E50Y2D1uUdj0O3uMBJnjuUD4Ih7YwaYd1iqfktj0Uod8GCExl3Og8ifwB6" crossorigin="anonymous"></script>"""
replacement = """<link rel="stylesheet" href="../../assets/bootstrap/css/bootstrap.min.css">
<script src="../../assets/web/assets/jquery/jquery.min.js"></script>
<script src="../../assets/popper/popper.min.js"></script>
<script src="../../assets/bootstrap/js/bootstrap.min.js"></script>"""

for dname, dirs, files in os.walk("imae"):
    for fname in files:
        fpath = os.path.join(dname, fname)
        print(fpath)
        with open(fpath, encoding='utf-8') as f:
            s = f.read()
        s = s.replace(replace_target, replacement)
        with open(fpath, "w", encoding='utf-8') as f:
            f.write(s)
