# Templates

## Overriding the Built-in Templates 
`templates/admin/*` eg. (index, model/edit, model/create, model/list)

To override the default *edit* template with your own functionality, create a template in
`templates/admin/index.html` to look something like::
```jinja 2
{% extends 'admin/master.html' %}

{% block body %}
{% endblock %}
```
## Extending the Built-in Templates
Internally, the Flask-Admin templates are derived from the `admin/master.html` template.
The three most interesting templates for you to extend are probably:

* `admin/model/list.html`
* `admin/model/create.html`
* `admin/model/edit.html`

To extend the default *edit* template with your own functionality, create a template in
`templates/microblog_edit.html` to look something like::
```jinja 2
{% extends 'admin/model/edit.html' %}

{% block body %}
    <h1>MicroBlog Edit View</h1>
    {{ super() }}
{% endblock %}
```
Now, to make your view classes use this template, set the appropriate class property::
```python 3
class MicroBlogModelView(ModelView):
    edit_template = 'microblog_edit.html'
    # create_template = 'microblog_create.html'
    # list_template = 'microblog_list.html'
    # details_template = 'microblog_details.html'
    # edit_modal_template = 'microblog_edit_modal.html'
    # create_modal_template = 'microblog_create_modal.html'
    # details_modal_template = 'microblog_details_modal.html'
```

## Available Template Blocks

Flask-Admin defines one *base* template at `admin/master.html` that all other admin templates are derived from. This template is a proxy which points to `admin/base.html`, which defines the following blocks:

| Block Name       | Description                                                                  |
|------------------|------------------------------------------------------------------------------|
| `head_meta`      | Page metadata in the header                                                  |
| `title`          | Page title                                                                   |
| `head_css`       | Various CSS includes in the header                                           |
| `head`           | Empty block in HTML head, in case you want to put something there            |
| `page_body`      | Page layout                                                                  |
| `brand`          | Logo in the menu bar                                                         |
| `main_menu`      | Main menu                                                                    |
| `menu_links`     | Links menu                                                                   |
| `access_control` | Section to the right of the menu (can be used to add login/logout buttons)   |
| `messages`       | Alerts and various messages                                                  |
| `body`           | Content (that's where your view will be displayed)                           |
| `tail`           | Empty area below content                                                     |

In addition to all of the blocks that are inherited from `admin/master.html`, the `admin/model/list.html` template also contains the following blocks:

| Block Name                 | Description                                                 |
|----------------------------|-------------------------------------------------------------|
| `model_menu_bar`           | Menu bar                                                    |
| `model_list_table`         | Table container                                             |
| `list_header`              | Table header row                                            |
| `list_row_actions_header`  | Actions header                                              |
| `list_row`                 | Single row                                                  |
| `list_row_actions`         | Row action cell with edit/remove/etc buttons                |
| `empty_list_message`       | Message that will be displayed if there are no models found |

Have a look at the [layout example](https://github.com/flask-admin/flask-admin/tree/master/examples/custom-layout) to see how you can take full stylistic control over the admin interface.
