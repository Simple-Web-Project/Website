# SimpleWeb Project Website
Website that holds an index for everything regarding the Simple Web Project, hosted at https://simple-web.org

## How to add your own Instance
If you want to make a PR/patch adding your own Instance to the list first you gotta add the domain to `instances/{project}` and then add it to the list in HTML at `projects/{project}.html` so for example if you'd want to add `example.translation.site` to SimplyTranslate then you'd do this:
```
instances/simplytranslate
+example.translation.site

projects/simplytranslate.html
+<li><a href="https://example.translation.site">example.translation.site</a></li>
```

This is only for the time being because I've been wanting to rework the site for quite a while now
