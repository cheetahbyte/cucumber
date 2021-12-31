# Fuchs Templates

<img  src="https://images.unsplash.com/photo-1605101479435-005f9c563944?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxzZWFyY2h8NXx8Zm94fGVufDB8fDB8fA%3D%3D&auto=format&fit=crop&w=500&q=60" style="width: 300px; margin-top: -50px;" align="right">

> Fuchs Templates is a simple template engine for HTML/XML written in Python.

Fuchs is the successor of [TEX](https://pypi.org/project/tex-engine) (Template Engine X)

## Inspiration

Fuchs was clearly influenced by template engines like Handlebars, Jinja and Genshi. And deliberately combines everything to ensure the best comfort with the highest quality.

## Functional references

Fuchs takes its cue from PHP, it has a syntax that allows to execute Python code.

```html
<!DOCTYPE html>
<html>
    <?fuchs 
        # valid python code inside here
        abc = "abc"
    ?>
    <p>{{abc}}</p>
</html>
```

```html
<!DOCTYPE html>
<html>
    <?fuchs 
        # valid python code inside here
        import random
        abc = random.randint(1,10)
    ?>
    <p>{{abc}}</p>
</html>
``` 

## Why not Jinja?

For my web framework Wire, I really wanted something that came from myself.  I mean, it's easy to add any dependency and be satisfied. But, I don't want that. 


# Note
Since Fuchs works exclusively on the server side, any security measures were removed when evaluating the code. Keywords like `quit()`, `exit()` etc. are therefore usable. 
Please avoid using them.