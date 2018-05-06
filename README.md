# flask-via-nginx-http2-push
Recently, I upgrade my nginx reverse proxy to enable http2 pushes. While this can be done by sending certain files upon calling a location, you can also use the HTTP Link header to tell nginx which resources tp push. I am using flask as webserver and found [this](https://github.com/jdaroesti/flask-http2-push) flask extension which promised to do the trick. It did not work, so I decided to write this little snippet.

# Usage

Copy and paste the function or download the whole file and import it to your project. Put the decorator in front of the view function which should push. As arguments enter the relative paths to the resources. It should make no difference, in which order you apply the decorators.

```python
@http2push("/static/style.css", "/static/script.js")
@route("/")
def home():
  pass
``` 

In your nginx configuration add the line **http2_push_preload** like this.

```
location /
{
  proxy_pass http://192.168.X.X:8080/;
  http2_push_preload on;
}
```

Known to work with Python 3.6.3 and flask 1.0.2
