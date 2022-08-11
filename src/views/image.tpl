% rebase('base.tpl', current_page = "image")

<div>
<img src= "{{ get_url('database', filename= image.id) }}" class="img-fluid" />
</div>
<div>
{{image.name}}
</div>
<div>
    <form action="/like/" method="POST">
    {{len(image.likes)}}
    <button class="icon">
      <i class="fa-regular fa-heart"></i>
    </button>
    </form>
    <form action="/dislike/" method="POST">
    {{len(image.dislikes)}}
    <button class="icon">
      <i class="fa-solid fa-xmark"></i>
    </button>
    </form>
</div>

%if len(image.comments) != 0:
<strong>Comments:</strong>
<div>
%for comment in image.comments:
<p>~“{{comment[1]}}”</i>   <sub>-{{comment[0]}}</sub>
%end
</p>
</div>
%end

<form action="/add_comment/" method="POST">
    <div class="field">
        <div class="control has-icons-left">
            <input class="input" name="comment" type="text" placeholder="comment">
            <span class="icon is-small is-left">
                <i class="fa fa-pencil"></i>
            </span>
        </div>
    </div>
    <div class="field is-grouped">
        <div class="control">
            <button class="button is-link">add comment</button>
        </div>
    </div>
</form>

