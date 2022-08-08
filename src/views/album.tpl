% rebase('base.tpl', current_page=album.name)
<p>{{username.username}}</p>

<p>
{{album.name}}
</p>
<form action="/add_friend/" method="POST">
    <div class="field">
        <div class="control has-icons-left">
            <input class="input" name="friend" type="text" placeholder="friend's name">
            <span class="icon is-small is-left">
                <i class="fas fa-user"></i>
            </span>
        </div>
    </div>
    <div class="field is-grouped">
        <div class="control">
            <button class="button is-link">add friend</button>
        </div>
    </div>
%if friend:
<p class="help is-danger">{{friend}} has been added to the album.</p>
%end
</form>

%for image in album.images:
<form action="/image/" method="get">
    <div class="field is-grouped">
        <div class="control">
            <button class="button is-link">image</button>
        </div>
    </div>
</form>