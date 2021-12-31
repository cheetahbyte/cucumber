from fuchs.main import FuchsTemplate

template = FuchsTemplate("templates")
print(template.render("test.html", name="Fuchs"))